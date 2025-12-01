from typing import Optional
import pandas as pd
from .config import OUT_DIR

def _extract_6digit_code(s: str) -> Optional[str]:
    if not isinstance(s, str):
        return None
    digits = "".join(ch for ch in s if ch.isdigit())
    if len(digits) < 6:
        return None
    return digits[-6:]

def load_equity_master() -> pd.DataFrame:
    eq_path_parquet = OUT_DIR / "equity_master.parquet"
    eq_path_csv = OUT_DIR / "equity_master.csv"

    if eq_path_parquet.exists():
        df = pd.read_parquet(eq_path_parquet)
    elif eq_path_csv.exists():
        df = pd.read_csv(eq_path_csv)
    else:
        raise FileNotFoundError(
            f"equity_master 파일을 찾을 수 없습니다: {eq_path_parquet} / {eq_path_csv}"
        )

    for col in ("name", "short_code", "std_code"):
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df

def get_etf_name_from_mst(etf_code: str) -> Optional[str]:
    df = load_equity_master()

    if "kis_code" not in df.columns:
        if "short_code" in df.columns:
            df["kis_code"] = df["short_code"].apply(_extract_6digit_code)
        elif "std_code" in df.columns:
            df["kis_code"] = df["std_code"].apply(_extract_6digit_code)

    if "kis_code" not in df.columns:
        return None

    m = df["kis_code"] == str(etf_code)
    hit = df[m]
    if hit.empty:
        return None

    name = str(hit.iloc[0]["name"]).strip()
    return name or None