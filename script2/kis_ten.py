"""
kis_ten.py

Step 10에서 사용하는 KIS ETF 포트폴리오/리스크 유틸 모듈.
- 다른 주피터 노트북에서 import 해서 재사용하는 용도.

필요 전제:
- 같은 디렉터리에 kis_env.py 가 존재하고,
  그 안에 다음 심볼이 정의되어 있어야 함:
    - DATA_DIR
    - KIS_URL_BASE
    - ensure_kis_token()
    - get_api_headers()
    - to_float()
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, List

from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd
import requests

from kis_nine import (
    DATA_DIR,
    KIS_URL_BASE,
    ensure_kis_token,
    get_api_headers,
    to_float,
)

# =============================================================================
# 0. Step 10: 포트폴리오(구성종목/섹터/시가총액) 관련 디렉터리
# =============================================================================

ETF_COMPONENT_DIR = DATA_DIR / "etf_components"
ETF_SUMMARY_DIR = DATA_DIR / "etf_portfolio_summary"

ETF_COMPONENT_DIR.mkdir(parents=True, exist_ok=True)
ETF_SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# 1. 공통 KIS GET 호출 유틸
# =============================================================================


def call_kis_get(
    path: str,
    tr_id: str,
    params: Dict[str, Any],
    *,
    max_retry: int = 1,
) -> Dict[str, Any]:
    """
    KIS GET 공통 헬퍼.

    - path: 'uapi/...' 형태의 엔드포인트 경로
    - tr_id: KIS 문서 상의 TR ID (예: FHKST121600C0)
    - params: 쿼리 파라미터 dict
    - max_retry: 토큰 만료 시 재시도 횟수

    반환:
    - KIS 응답 JSON(dict). rt_cd != "0"인 경우 RuntimeError 발생.
    """
    if not KIS_URL_BASE:
        raise RuntimeError("KIS_URL_BASE가 설정되어 있지 않습니다. .env를 확인하세요.")

    # 0) 토큰이 하나는 존재하도록 보장
    ensure_kis_token()

    url = f"{KIS_URL_BASE.rstrip('/')}/{path.lstrip('/')}"

    for attempt in range(max_retry + 1):
        headers = get_api_headers(tr_id)

        try:
            res = requests.get(url, headers=headers, params=params, timeout=5)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            raise RuntimeError(f"KIS GET 실패 ({path}, 시도={attempt+1}): {e}") from e

        rt_cd = data.get("rt_cd")
        if rt_cd == "0":
            return data

        # 토큰 만료 코드인 경우, 토큰 재발급 후 재시도
        if rt_cd in ("EGW00123", "EGW00121") and attempt < max_retry:
            print(f"[INFO] 토큰 만료(rt_cd={rt_cd}), refresh 후 재시도...")
            from kis_env import refresh_access_token  # 순환 import 방지용 지역 import

            refresh_access_token()
            continue

        # 여기까지 왔다는 것은 재시도 후에도 실패한 경우
        msg = data.get("msg1") or data.get("msg_cd") or "알 수 없는 오류"
        raise RuntimeError(f"KIS API 오류 (path={path}, rt_cd={rt_cd}, msg={msg})")

    # 논리상 도달하지 않지만, 안전망
    raise RuntimeError(f"KIS GET 실패: 최대 재시도({max_retry})를 초과했습니다. path={path}")
