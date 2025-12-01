from typing import Optional

def to_float(value) -> Optional[float]:
    try:
        return float(str(value).replace(",", "").strip())
    except Exception:
        return None