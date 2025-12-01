from __future__ import annotations
from typing import Optional

import requests

from .config import KIS_URL_BASE
from .auth import validate_and_refresh_token, get_api_headers
from .mst import get_etf_name_from_mst

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