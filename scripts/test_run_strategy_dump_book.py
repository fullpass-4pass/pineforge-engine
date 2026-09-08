#!/usr/bin/env python3
"""run_strategy.py reads the resting-order book through the runtime's OWN
field table (ABI v4 task 7): build_pending_order_struct turns the
strategy_pending_order_layout rows into a ctypes.Structure and refuses any
row it cannot place byte-exactly; pending_order_to_dict renders one record
JSON-ready (strings up to the NUL, NaN -> None, every uint64_t -> hex);
Strategy.read_pending_orders drives the len/get loop against a stub lib.

Pure-Python: no .so is loaded. The C++ side of the contract (the layout
table's offsets/sizes, strategy_pending_order_get's prefix-copy rule) is
pinned by tests/test_live_pending_order_mirror.cpp."""
from __future__ import annotations

import ctypes
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_strategy  # noqa: E402
from run_strategy import (  # noqa: E402
    PENDING_ORDER_STRUCT_VERSION,
    build_pending_order_struct,
    pending_order_to_dict,
)


def _layout_from_ctypes(fields: list[tuple[str, str, type]]) -> list[tuple[str, str, int, int]]:
    """Helper: natural-alignment layout for (name, type-spelling, ctype)."""
    cls = type("Ref", (ctypes.Structure,), {"_fields_": [(n, ct) for n, _, ct in fields]})
    return [(n, t, getattr(cls, n).offset, ctypes.sizeof(ct)) for n, t, ct in fields]


# A representative slice of the real pf_pending_order_v1_t: the two
# header fields, a string triple, an enum/int32, a bool byte, a double, an
# int64 and a uint64.
FIELDS = [
    ("struct_version", "uint32_t", ctypes.c_uint32),
    ("size", "uint32_t", ctypes.c_uint32),
    ("id", "char[64]", ctypes.c_char * 64),
    ("id_truncated", "uint8_t", ctypes.c_uint8),
    ("id_hash64", "uint64_t", ctypes.c_uint64),
    ("type", "int32_t", ctypes.c_int32),
    ("is_long", "uint8_t", ctypes.c_uint8),
    ("stop_price", "double", ctypes.c_double),
    ("created_seq", "int64_t", ctypes.c_int64),
    ("incarnation", "uint64_t", ctypes.c_uint64),
]
LAYOUT = _layout_from_ctypes(FIELDS)


class BuildStruct(unittest.TestCase):
    def test_builds_struct_matching_every_offset_and_size(self):
        cls = build_pending_order_struct(LAYOUT)
        self.assertEqual(cls.__name__, "PendingOrderV1")
        for name, _t, off, size in LAYOUT:
            self.assertEqual(getattr(cls, name).offset, off, name)
            self.assertEqual(getattr(cls, name).size, size, name)
        last = LAYOUT[-1]
        self.assertGreaterEqual(ctypes.sizeof(cls), last[2] + last[3])

    def test_unknown_type_spelling_is_refused(self):
        bad = LAYOUT + [("weird", "long double", LAYOUT[-1][2] + 8, 16)]
        with self.assertRaisesRegex(RuntimeError, "unknown C type 'long double'"):
            build_pending_order_struct(bad)

    def test_size_mismatch_is_refused(self):
        bad = [(n, t, o, (2 if n == "is_long" else s)) for n, t, o, s in LAYOUT]
        with self.assertRaisesRegex(RuntimeError, "is_long.*2 bytes in the runtime"):
            build_pending_order_struct(bad)

    def test_offset_mismatch_is_refused(self):
        # Shift one runtime offset by a byte: ctypes' natural placement can
        # no longer agree, and the reader must refuse rather than mis-read.
        bad = [(n, t, (o + 1 if n == "stop_price" else o), s) for n, t, o, s in LAYOUT]
        with self.assertRaisesRegex(RuntimeError, "stop_price.*ctypes placed it at"):
            build_pending_order_struct(bad)

    def test_header_fields_must_lead(self):
        swapped = [LAYOUT[1], LAYOUT[0]] + LAYOUT[2:]
        with self.assertRaisesRegex(RuntimeError, "must start with struct_version, size"):
            build_pending_order_struct(swapped)

    def test_empty_layout_is_refused(self):
        with self.assertRaisesRegex(RuntimeError, "no fields"):
            build_pending_order_struct([])


class ToDict(unittest.TestCase):
    def _record(self):
        cls = build_pending_order_struct(LAYOUT)
        rec = cls()
        rec.struct_version = PENDING_ORDER_STRUCT_VERSION
        rec.size = ctypes.sizeof(cls)
        rec.id = b"x" * 63           # char[64]: 63 payload bytes + NUL
        rec.id_truncated = 1
        rec.id_hash64 = 0x6540A31A8547B3BD
        rec.type = 2
        rec.is_long = 0
        rec.stop_price = 95.0
        rec.created_seq = -3
        rec.incarnation = 2 ** 63 + 5   # above the JS-safe range: stays an exact int
        return rec

    def test_renders_every_field_in_layout_order(self):
        d = pending_order_to_dict(self._record(), LAYOUT)
        self.assertEqual(list(d.keys()), [n for n, *_ in LAYOUT])
        self.assertEqual(d["struct_version"], PENDING_ORDER_STRUCT_VERSION)
        self.assertEqual(d["id"], "x" * 63)
        self.assertEqual(d["id_truncated"], 1)
        self.assertEqual(d["id_hash64"], "6540a31a8547b3bd")   # hex, not a JSON number
        self.assertEqual(d["type"], 2)
        self.assertEqual(d["is_long"], 0)
        self.assertEqual(d["stop_price"], 95.0)
        self.assertEqual(d["created_seq"], -3)
        # EVERY uint64_t field is hex (not only the *_hash64 digests): an
        # incarnation above 2**53 would otherwise be silently rounded by a
        # JS consumer.
        self.assertEqual(d["incarnation"], format(2 ** 63 + 5, "016x"))
        self.assertEqual(d["incarnation"], "8000000000000005")

    def test_nan_sentinel_becomes_none(self):
        rec = self._record()
        rec.stop_price = math.nan
        self.assertIsNone(pending_order_to_dict(rec, LAYOUT)["stop_price"])
        rec.stop_price = math.inf
        self.assertIsNone(pending_order_to_dict(rec, LAYOUT)["stop_price"])

    def test_string_stops_at_nul(self):
        rec = self._record()
        rec.id = b"L\0garbage"
        self.assertEqual(pending_order_to_dict(rec, LAYOUT)["id"], "L")

    def test_hash64_of_id_matches_fnv1a_of_full_string(self):
        # The runtime's id_hash64 is FNV-1a 64 of the FULL id; pin the
        # reference value observed from the tutorial MACD strategy's resting
        # "Long" order so a reader-side decode change cannot drift silently.
        h = 1469598103934665603
        for ch in b"Long":
            h = ((h ^ ch) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
        self.assertEqual(format(h, "016x"), "6540a31a8547b3bd")


class _StubLib:
    """Stand-in for the loaded .so: serves `records` (prepared PendingOrderV1
    instances) through the two book accessors exactly as c_abi.cpp does --
    min(size_in, sizeof) prefix copy, -1 on a bad index -- so
    Strategy.read_pending_orders' real loop (rc / struct_version / size
    checks, dict rendering) runs without a compiled strategy."""

    def __init__(self, records):
        self.records = records
        self.calls: list[tuple[int, int]] = []

    def strategy_pending_orders_len(self, state):
        return len(self.records)

    def strategy_pending_order_get(self, state, index, out, size_in):
        self.calls.append((index, int(size_in)))
        if index < 0 or index >= len(self.records):
            return -1
        rec = self.records[index]
        ctypes.memmove(out, ctypes.byref(rec), min(int(size_in), ctypes.sizeof(rec)))
        return 0


def _stub_strategy(records, cls):
    strat = run_strategy.Strategy.__new__(run_strategy.Strategy)
    strat.PendingOrderV1 = cls
    strat.pending_order_layout = LAYOUT
    strat.lib = _StubLib(records)
    return strat


class ReadPendingOrders(unittest.TestCase):
    """Strategy.read_pending_orders against a stub lib (Important 1)."""

    def _record(self, cls, **kw):
        rec = cls()
        rec.struct_version = PENDING_ORDER_STRUCT_VERSION
        rec.size = ctypes.sizeof(cls)
        for k, v in kw.items():
            setattr(rec, k, v)
        return rec

    def test_happy_path_reads_every_order_in_book_order(self):
        cls = build_pending_order_struct(LAYOUT)
        a = self._record(cls, id=b"Long", type=0, is_long=1, stop_price=math.nan,
                         created_seq=5, incarnation=5, id_hash64=0x6540A31A8547B3BD)
        b = self._record(cls, id=b"x" * 63, id_truncated=1, type=2, is_long=0,
                         stop_price=95.0, created_seq=6, incarnation=2 ** 63 + 5)
        strat = _stub_strategy([a, b], cls)
        book = strat.read_pending_orders(object())
        self.assertEqual(len(book), 2)
        self.assertEqual(book[0]["id"], "Long")
        self.assertEqual(book[0]["type"], 0)
        self.assertEqual(book[0]["is_long"], 1)
        self.assertIsNone(book[0]["stop_price"])
        self.assertEqual(book[0]["created_seq"], 5)
        self.assertEqual(book[0]["incarnation"], "0000000000000005")
        self.assertEqual(book[0]["id_hash64"], "6540a31a8547b3bd")
        self.assertEqual(book[1]["id"], "x" * 63)
        self.assertEqual(book[1]["id_truncated"], 1)
        self.assertEqual(book[1]["type"], 2)
        self.assertEqual(book[1]["stop_price"], 95.0)
        self.assertEqual(book[1]["incarnation"], "8000000000000005")
        self.assertEqual(book[1]["struct_version"], PENDING_ORDER_STRUCT_VERSION)
        self.assertEqual(book[1]["size"], ctypes.sizeof(cls))
        # One get per order, each with the full layout-built size.
        self.assertEqual(strat.lib.calls, [(0, ctypes.sizeof(cls)), (1, ctypes.sizeof(cls))])

    def test_empty_book(self):
        cls = build_pending_order_struct(LAYOUT)
        strat = _stub_strategy([], cls)
        self.assertEqual(strat.read_pending_orders(object()), [])
        self.assertEqual(strat.lib.calls, [])

    def test_struct_version_mismatch_is_refused(self):
        cls = build_pending_order_struct(LAYOUT)
        bad = self._record(cls, id=b"L")
        bad.struct_version = 2
        strat = _stub_strategy([bad], cls)
        with self.assertRaisesRegex(RuntimeError, r"pending order 0: struct_version 2 != 1"):
            strat.read_pending_orders(object())

    def test_size_mismatch_is_refused(self):
        cls = build_pending_order_struct(LAYOUT)
        bad = self._record(cls, id=b"L")
        bad.size = ctypes.sizeof(cls) + 8      # a newer producer's larger struct
        strat = _stub_strategy([bad], cls)
        with self.assertRaisesRegex(
                RuntimeError,
                rf"pending order 0: runtime size {ctypes.sizeof(cls) + 8} != layout-built sizeof {ctypes.sizeof(cls)}"):
            strat.read_pending_orders(object())

    def test_get_failure_is_refused(self):
        # len says 2 but get refuses index 1: the loop must surface it.
        cls = build_pending_order_struct(LAYOUT)
        strat = _stub_strategy([self._record(cls, id=b"L")], cls)
        strat.lib.strategy_pending_orders_len = lambda state: 2
        with self.assertRaisesRegex(RuntimeError, r"strategy_pending_order_get\(1\) returned -1 \(len=2\)"):
            strat.read_pending_orders(object())


class StrategyGuard(unittest.TestCase):
    def test_read_pending_orders_without_exports_is_empty(self):
        # A .so predating strategy_pending_order_layout: Strategy leaves
        # PendingOrderV1 None and read_pending_orders returns [] rather
        # than touching the missing symbols.
        strat = run_strategy.Strategy.__new__(run_strategy.Strategy)
        strat.PendingOrderV1 = None
        strat.pending_order_layout = None
        strat.lib = object()
        self.assertEqual(strat.read_pending_orders(object()), [])


if __name__ == "__main__":
    unittest.main()
