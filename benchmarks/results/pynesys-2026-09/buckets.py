"""Feature-bucket parser for Pine sources (regex, comments stripped). Shared by the sampler and the report."""
import re
_LINE = re.compile(r"//.*?$", re.MULTILINE)
_BLOCK = re.compile(r"/\*.*?\*/", re.DOTALL)
RULES = {
    "trail":        re.compile(r"\btrail_(points|offset|price)\s*=", re.I),
    "brackets":     re.compile(r"strategy\.exit\s*\([^)]*\b(stop|limit|loss|profit)\s*=", re.I | re.S),
    "partial":      re.compile(r"\bqty_percent\s*=", re.I),
    "pyramiding":   re.compile(r"\bpyramiding\s*=\s*([2-9]|[1-9]\d+)\b"),
    "calc_on_fills": re.compile(r"\bcalc_on_order_fills\s*=\s*true\b"),
    "pooc":         re.compile(r"\bprocess_orders_on_close\s*=\s*true\b"),
    "margin_lt100": re.compile(r"\bmargin_(long|short)\s*=\s*(\d+(\.\d+)?)"),
    "security":     re.compile(r"\brequest\.security(_lower_tf)?\s*\("),
    "magnifier":    re.compile(r"\buse_bar_magnifier\s*=\s*true\b"),
    "varip":        re.compile(r"\bvarip\b"),
    "var_state":    re.compile(r"(^|[^\w.])var\s+(\w+\s+)?\w+\s*="),
    "arrays":       re.compile(r"\b(array|matrix|map)\.\w+\s*\("),
    "udt":          re.compile(r"^\s*type\s+\w+\s*$", re.M),
}
# stratification bucket, first match wins
PRIMARY = ["trail", "partial", "brackets", "security", "plain"]

def strip(src: str) -> str:
    return _LINE.sub("", _BLOCK.sub("", src))

def features(src: str) -> dict:
    s = strip(src)
    out = {}
    for k, rx in RULES.items():
        if k == "margin_lt100":
            out[k] = any(float(m.group(2)) < 100 for m in rx.finditer(s))
        else:
            out[k] = bool(rx.search(s))
    return out

def primary(feat: dict) -> str:
    for k in PRIMARY:
        if k == "plain" or feat.get(k):
            return k
    return "plain"
