#!/usr/bin/env python3
"""Generate the POD mirror of pineforge::PendingOrder (spec §3.6, ABI v4).

Parses ``struct PendingOrder { ... };`` in include/pineforge/engine.hpp and
emits

  * include/pineforge/pending_order_mirror.hpp -- the C-compatible
    ``pf_pending_order_v1_t`` typedef (``uint32_t struct_version`` = 1,
    ``uint32_t size``, then every PendingOrder member in declaration order:
    scalars by value -- ``bool``->``uint8_t``, ``int``/``int8_t``/enums->
    ``int32_t``, ``int64_t``/``uint64_t``/``double`` as-is -- and every
    ``std::string`` as ``char name[64]; uint8_t name_truncated; uint64_t
    name_hash64;`` where the hash is FNV-1a 64 of the FULL string) plus the
    ``pf_field_desc_t`` {name, type, offset, size} descriptor type;
  * src/pending_order_mirror.cpp -- ``pineforge::fill_pending_order_mirror``
    and ``pineforge::pending_order_layout`` (the self-describing field table
    a ctypes/FFI consumer builds its struct from).

Every member of PendingOrder must be either mapped by TYPE_MAP / a
``std::string``, or listed in scripts/pending_order_mirror_waivers.txt
(``name  # reason``) -- otherwise generation FAILS. A declaration the parser
cannot classify (two names on one line, a method, a template type, a static
member, ...) also fails: the point of this generator is that PendingOrder
cannot silently grow a member nobody mirrored.

Run with --check to verify the committed files are byte-identical to what
the current engine.hpp generates (CI, and a ctest). The parser is also
imported by scripts/check_broker_state_hash_coverage.py (``members()``).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HPP = ROOT / "include/pineforge/engine.hpp"
OUT_H = ROOT / "include/pineforge/pending_order_mirror.hpp"
OUT_C = ROOT / "src/pending_order_mirror.cpp"
WAIVERS = ROOT / "scripts/pending_order_mirror_waivers.txt"
STRUCT_NAME = "PendingOrder"
STR_CAP = 64
STRUCT_VERSION = 1

# C++ member type -> (C field type, copy expression template).
TYPE_MAP: dict[str, tuple[str, str]] = {
    "bool": ("uint8_t", "src.{m} ? 1 : 0"),
    "int": ("int32_t", "(int32_t)src.{m}"),
    "int8_t": ("int32_t", "(int32_t)src.{m}"),
    "int32_t": ("int32_t", "src.{m}"),
    "int64_t": ("int64_t", "src.{m}"),
    "uint64_t": ("uint64_t", "src.{m}"),
    "double": ("double", "src.{m}"),
    # Enums: value-cast to int32 (the enumerator order is the ABI).
    "OrderType": ("int32_t", "(int32_t)src.{m}"),
    "PositionSide": ("int32_t", "(int32_t)src.{m}"),
    "ShortSeedCollisionRole": ("int32_t", "(int32_t)src.{m}"),
}
STRING_TYPES = frozenset({"std::string"})

BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
LINE_COMMENT_RE = re.compile(r"//[^\n]*")
# One declaration, comments stripped and whitespace collapsed:
#   TYPE NAME [= initialiser]
# TYPE is a single (optionally std::-qualified) identifier; anything else
# (template args, two names, cv-qualifiers, `static`, a method's `(`) fails
# to match and the caller reports it.
DECL_RE = re.compile(r"^((?:std::)?[A-Za-z_]\w*) ([A-Za-z_]\w*)(?: = .+)?$", re.S)


def _fail(msg: str) -> "NoReturn":  # noqa: F821
    sys.exit(f"gen_pending_order_mirror: {msg}")


def struct_body(text: str, name: str = STRUCT_NAME) -> str:
    """Return the text between the braces of ``struct <name> { ... };``.
    Comments are stripped BEFORE anchoring, so a prose mention of
    ``struct PendingOrder {`` in a comment cannot mis-anchor the parser, and
    the anchor must occur exactly once in what remains."""
    text = LINE_COMMENT_RE.sub("", BLOCK_COMMENT_RE.sub("", text))
    anchors = list(re.finditer(rf"\bstruct\s+{re.escape(name)}\s*\{{", text))
    if not anchors:
        _fail(f"struct {name} not found in {HPP}")
    if len(anchors) > 1:
        _fail(f"struct {name} {{ appears {len(anchors)} times in {HPP} (outside comments); "
              "expected exactly one definition")
    start = anchors[0].end()
    depth = 1
    for i in range(start, len(text)):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i]
    _fail(f"struct {name}: unbalanced braces")


def members(text: str | None = None) -> list[tuple[str, str]]:
    """Return [(cpp_type, name)] for every data member of PendingOrder, in
    declaration order. Comments are stripped and multi-line declarations
    (a member whose initialiser wraps onto the next line) are joined before
    parsing. Any declaration that is not exactly ``TYPE NAME [= init];``
    aborts."""
    if text is None:
        text = HPP.read_text(encoding="utf-8")
    body = struct_body(text)   # already comment-stripped
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for raw in body.split(";"):
        decl = " ".join(raw.split())
        if not decl:
            continue
        m = DECL_RE.match(decl)
        if not m:
            _fail(f"cannot classify declaration in struct {STRUCT_NAME}: {decl!r} "
                  "(expected exactly `TYPE NAME [= init];`; split multi-name "
                  "declarations, and mirror-waive methods/templates explicitly)")
        t, n = m.group(1), m.group(2)
        if n in seen:
            _fail(f"duplicate member name {n}")
        seen.add(n)
        out.append((t, n))
    if not out:
        _fail(f"struct {STRUCT_NAME} has no members?")
    return out


def load_waivers(path: Path = WAIVERS) -> dict[str, str]:
    waivers: dict[str, str] = {}
    if not path.is_file():
        return waivers
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "#" not in raw:
            _fail(f"waiver line {lineno} has no '# reason': {raw!r}")
        name, reason = raw.split("#", 1)
        name, reason = name.strip(), reason.strip()
        if not name:
            continue
        if not reason:
            _fail(f"waiver for {name!r} (line {lineno}) has no reason after '#'")
        waivers[name] = reason
    return waivers


def classify(ms: list[tuple[str, str]], waivers: dict[str, str]):
    """Return (mirrored, waived) where mirrored = [(cpp_type, name)] kept in
    the POD and waived = [(cpp_type, name, reason)]. Aborts on an unmapped,
    unwaived type or a waiver naming a non-member."""
    names = {n for _, n in ms}
    orphans = sorted(w for w in waivers if w not in names)
    if orphans:
        _fail(f"waiver(s) naming a member not in struct {STRUCT_NAME}: {orphans}")
    mirrored, waived = [], []
    for t, n in ms:
        if n in waivers:
            waived.append((t, n, waivers[n]))
        elif t in STRING_TYPES or t in TYPE_MAP:
            mirrored.append((t, n))
        else:
            _fail(f"member {n} has unmapped type {t}; add it to TYPE_MAP or "
                  f"waive it in {WAIVERS.relative_to(ROOT)}")
    return mirrored, waived


def generate() -> tuple[str, str]:
    mirrored, waived = classify(members(), load_waivers())
    fields: list[str] = []
    copies: list[str] = []
    descs: list[tuple[str, str]] = [("struct_version", "uint32_t"), ("size", "uint32_t")]
    for t, m in mirrored:
        if t in STRING_TYPES:
            fields += [f"    char {m}[{STR_CAP}];",
                       f"    uint8_t {m}_truncated;",
                       f"    uint64_t {m}_hash64;"]
            copies.append(f"    copy_str(src.{m}, out->{m}, &out->{m}_truncated, &out->{m}_hash64);")
            descs += [(m, f"char[{STR_CAP}]"), (f"{m}_truncated", "uint8_t"), (f"{m}_hash64", "uint64_t")]
        else:
            ct, expr = TYPE_MAP[t]
            fields.append(f"    {ct} {m};")
            copies.append(f"    out->{m} = {expr.format(m=m)};")
            descs.append((m, ct))

    banner = "// GENERATED by scripts/gen_pending_order_mirror.py from include/pineforge/engine.hpp -- do not edit."
    waived_note = ([f"// Not mirrored (scripts/pending_order_mirror_waivers.txt): "
                    + ", ".join(f"{n} ({r})" for _, n, r in waived)]
                   if waived else [])
    h = [
        banner,
        f"// {len(mirrored)} PendingOrder members mirrored ({len(descs)} POD fields incl. struct_version/size).",
        *waived_note,
        "#pragma once",
        "#include <stdint.h>",
        "",
        "/* C-compatible value snapshot of one resting pineforge::PendingOrder",
        " * (spec 3.6). struct_version identifies the field set (this file:",
        f" * {STRUCT_VERSION}); size is sizeof(pf_pending_order_v1_t) as the producer",
        " * compiled it. Strings are copied into a NUL-terminated char[64]",
        " * (name_truncated = 1 when the source was longer than 63 bytes) with",
        " * name_hash64 = FNV-1a 64 of the FULL source string. Enums are their",
        " * int32 value; bool is 0/1 in a uint8_t. Append-only, like every",
        " * pineforge.h POD. */",
        "typedef struct pf_pending_order_v1_s {",
        "    uint32_t struct_version;",
        "    uint32_t size;",
        *fields,
        "} pf_pending_order_v1_t;",
        "",
        "/* One row of the self-describing layout table returned by",
        " * strategy_pending_order_layout(): field name, C type spelling",
        f' * ("uint8_t", "int32_t", "int64_t", "uint64_t", "double", "char[{STR_CAP}]",',
        ' * "uint32_t"), byte offset inside pf_pending_order_v1_t, byte size. */',
        "typedef struct pf_field_desc_s {",
        "    const char* name;",
        "    const char* type;",
        "    uint32_t offset;",
        "    uint32_t size;",
        "} pf_field_desc_t;",
        f"#define PF_PENDING_ORDER_STRUCT_VERSION {STRUCT_VERSION}",
        f"#define PF_PENDING_ORDER_STR_CAP {STR_CAP}",
        "",
    ]
    c = [
        banner,
        "#include <pineforge/engine.hpp>",
        "#include <pineforge/pending_order_mirror.hpp>",
        "",
        "#include <cstddef>",
        "#include <cstring>",
        "#include <type_traits>",
        "",
        "static_assert(std::is_standard_layout<pf_pending_order_v1_t>::value,",
        '              "pf_pending_order_v1_t must be standard-layout");',
        "static_assert(std::is_trivial<pf_pending_order_v1_t>::value,",
        '              "pf_pending_order_v1_t must be trivial (memcpy-able across the C ABI)");',
        "",
        "namespace pineforge {",
        "namespace {",
        "",
        "// NUL-terminated copy of the first STR_CAP-1 bytes + FNV-1a 64 of the",
        "// whole string, so a consumer can still match an over-long id exactly.",
        "void copy_str(const std::string& s, char* dst, uint8_t* truncated, uint64_t* hash) {",
        "    uint64_t h = 1469598103934665603ULL;",
        "    for (unsigned char ch : s) { h ^= ch; h *= 1099511628211ULL; }",
        "    *hash = h;",
        f"    const size_t n = s.size() < {STR_CAP - 1} ? s.size() : {STR_CAP - 1};",
        "    std::memcpy(dst, s.data(), n);",
        "    dst[n] = 0;",
        f"    *truncated = s.size() > {STR_CAP - 1} ? 1 : 0;",
        "}",
        "",
        "}  // namespace",
        "",
        "void fill_pending_order_mirror(const PendingOrder& src, pf_pending_order_v1_t* out) {",
        "    std::memset(out, 0, sizeof(*out));",
        f"    out->struct_version = {STRUCT_VERSION};",
        "    out->size = (uint32_t)sizeof(*out);",
        *copies,
        "}",
        "",
        "namespace {",
        "",
        "#define PF_PO_FIELD(name, type) \\",
        "    { #name, type, (uint32_t)offsetof(pf_pending_order_v1_t, name), \\",
        "      (uint32_t)sizeof(((pf_pending_order_v1_t*)0)->name) }",
        "",
        "const pf_field_desc_t kLayout[] = {",
        *[f'    PF_PO_FIELD({n}, "{t}"),' for n, t in descs],
        "};",
        "",
        "#undef PF_PO_FIELD",
        "",
        "}  // namespace",
        "",
        "const pf_field_desc_t* pending_order_layout(int* count) {",
        "    if (count) *count = (int)(sizeof(kLayout) / sizeof(kLayout[0]));",
        "    return kLayout;",
        "}",
        "",
        "}  // namespace pineforge",
        "",
    ]
    return "\n".join(h), "\n".join(c)


def census() -> str:
    ms = members()
    mirrored, waived = classify(ms, load_waivers())
    by_type: dict[str, int] = {}
    for t, _ in ms:
        by_type[t] = by_type.get(t, 0) + 1
    lines = [f"{STRUCT_NAME}: {len(ms)} members, {len(mirrored)} mirrored, {len(waived)} waived"]
    lines += [f"  {t:<24} {c}" for t, c in sorted(by_type.items(), key=lambda kv: (-kv[1], kv[0]))]
    lines += [f"  waived: {n} ({r})" for _, n, r in waived]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if "--census" in argv:
        print(census())
        return 0
    h, c = generate()
    if "--check" in argv:
        cur_h = OUT_H.read_text(encoding="utf-8") if OUT_H.is_file() else None
        cur_c = OUT_C.read_text(encoding="utf-8") if OUT_C.is_file() else None
        ok = cur_h == h and cur_c == c
        print("pending_order_mirror: up to date" if ok else
              "pending_order_mirror: STALE -- run python3 scripts/gen_pending_order_mirror.py "
              "and commit include/pineforge/pending_order_mirror.hpp + src/pending_order_mirror.cpp")
        return 0 if ok else 1
    OUT_H.write_text(h, encoding="utf-8")
    OUT_C.write_text(c, encoding="utf-8")
    print(f"wrote {OUT_H.relative_to(ROOT)}, {OUT_C.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
