from __future__ import annotations
from functools import lru_cache
from typing import Optional
import pandas as pd
import requests

from .env import OUT_DIR, validate_and_refresh_token, KIS_URL_BASE, get_api_headers

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

    if "name" in df.columns:
        df["name"] = df["name"].astype(str).str.strip()
    if "short_code" in df.columns:
        df["short_code"] = df["short_code"].astype(str).str.strip()
    if "std_code" in df.columns:
        df["std_code"] = df["std_code"].astype(str).str.strip()

    return df

def find_code_by_name(kor_name: str) -> pd.DataFrame:
    df = load_equity_master()
    m = df["name"].str.contains(kor_name, case=False, na=False)
    candidates = df[m].copy()

    if candidates.empty:
        print(f"⚠️ 이름에 '{kor_name}' 이(가) 포함된 종목을 찾지 못했습니다.")
        return candidates

    if "kis_code" not in candidates.columns:
        if "short_code" in candidates.columns:
            candidates["kis_code"] = candidates["short_code"].apply(_extract_6digit_code)
        elif "std_code" in candidates.columns:
            candidates["kis_code"] = candidates["std_code"].apply(_extract_6digit_code)
        else:
            candidates["kis_code"] = None

    return candidates

def pick_single_code(kor_name: str) -> str:
    candidates = find_code_by_name(kor_name)
    if candidates.empty:
        raise ValueError(f"'{kor_name}' 에 해당하는 종목을 찾을 수 없습니다.")

    row = candidates.iloc[0]
    kis_code = row.get("kis_code")
    if not kis_code:
        raise ValueError(f"'{kor_name}' 후보에서 KIS 코드(6자리)를 추출하지 못했습니다.\n{row}")

    print(f"[INFO] '{kor_name}' → 선택된 종목: {row.get('name')} (kis_code={kis_code})")
    return str(kis_code)

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

def get_etf_name_from_kis(etf_code: str) -> Optional[str]:
    validate_and_refresh_token()
    if not KIS_URL_BASE:
        return None

    url = f"{KIS_URL_BASE}/uapi/domestic-stock/v1/quotations/search-stock-info"
    params = {"PRDT_TYPE_CD": "512", "PDNO": etf_code}
    headers = get_api_headers("CTPF1604R")

    try:
        res = requests.get(url, headers=headers, params=params, timeout=5)
        data = res.json()
    except Exception as e:
        print(f"⚠️ KIS ETF 이름 조회 실패: {e}")
        return None

    if data.get("rt_cd") != "0" or not data.get("output"):
        return None

    output = data["output"]
    row = output[0] if isinstance(output, list) else output
    name = row.get("prdt_name") or row.get("hts_kor_isnm")
    name = (name or "").strip()
    return name or None

def get_etf_name(etf_code: str) -> str:
    code = str(etf_code)

    name = get_etf_name_from_mst(code)
    if name:
        print(f"✅ ETF 이름(MST): {code} → {name}")
        return name

    name = get_etf_name_from_kis(code)
    if name:
        print(f"✅ ETF 이름(KIS): {code} → {name}")
        return name

    print(f"⚠️ ETF 이름 조회 실패 → 코드 사용 ({code})")
    return code
