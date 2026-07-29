import re

def slug(s: str) -> str:
    s = str(s or "")
    s = s.strip().lower()
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^a-z0-9_]+", "", s)
    return s[:80]

def file_size_bytes(f):
    if f is None:
        return 0
    size = getattr(f, "size", None)
    return size if size is not None else len(f.getbuffer())

def required_ok(val) -> bool:
    if val is None:
        return False
    if isinstance(val, str):
        return val.strip() != ""
    return True