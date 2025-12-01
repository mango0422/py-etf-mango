# kis_utils.py

import os
import requests
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from typing import Dict, Any

# 1. 환경 설정 및 상수
PROJECT_ROOT = Path.cwd()
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# .env 로드
load_dotenv(PROJECT_ROOT / ".env")
KIS_APP_KEY: Optional[str] = os.getenv("KIS_APP_KEY")
KIS_APP_SECRET: Optional[str] = os.getenv("KIS_APP_SECRET")
KIS_ACCESS_TOKEN: Optional[str] = os.getenv("KIS_ACCESS_TOKEN")
KIS_URL_BASE: str = os.getenv(
    "KIS_URL_BASE",
    "https://openapivts.koreainvestment.com:29443",  # 기본값: 모의투자(설정에 따라 변경)
)


# 2. 기초 유틸리티
def to_float(value) -> Optional[float]:
    """쉼표/공백이 섞인 문자열을 float로 변환"""
    try:
        return float(str(value).replace(",", "").strip())
    except Exception:
        return None

# 3. KIS 인증 및 헤더 관리
def get_api_headers(tr_id: str) -> dict[str, str]:
    """KIS 공통 헤더 생성"""
    global KIS_ACCESS_TOKEN
    auth = f"Bearer {KIS_ACCESS_TOKEN}" if KIS_ACCESS_TOKEN else ""
    return {
        "content-type": "application/json",
        "authorization": auth,
        "appkey": KIS_APP_KEY or "",
        "appsecret": KIS_APP_SECRET or "",
        "tr_id": tr_id,
        "custtype": "P",
    }

def refresh_access_token() -> Optional[str]:
    """토큰 재발급 및 .env 업데이트"""
    global KIS_ACCESS_TOKEN

    if not (KIS_APP_KEY and KIS_APP_SECRET and KIS_URL_BASE):
        raise RuntimeError("KIS 환경변수(APP_KEY/SECRET/URL_BASE)가 누락되었습니다.")

    TOKEN_PATH = "oauth2/tokenP"
    TOKEN_URL = f"{KIS_URL_BASE}/{TOKEN_PATH}"

    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": KIS_APP_KEY,
        "appsecret": KIS_APP_SECRET,
    }

    try:
        response = requests.post(TOKEN_URL, headers=headers, json=body, timeout=10)
        response.raise_for_status()
        data = response.json()
        access_token = data.get("access_token")

        if not access_token:
            raise RuntimeError(f"토큰 응답 오류: {data}")

        # 메모리 갱신
        KIS_ACCESS_TOKEN = access_token

        # 파일 갱신 (선택 사항)
        env_path = PROJECT_ROOT / ".env"
        if env_path.exists():
            _update_env_file(env_path, "KIS_ACCESS_TOKEN", access_token)

        return access_token

    except Exception as e:
        print(f"Token Refresh Failed: {e}")
        raise

def _update_env_file(path: Path, key: str, value: str):
    """(내부용) .env 파일 내용 갱신"""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        new_lines = []
        written = False
        for line in lines:
            if line.startswith(f"{key}="):
                new_lines.append(f"{key}={value}")
                written = True
            else:
                new_lines.append(line)
        if not written:
            new_lines.append(f"{key}={value}")
        path.write_text("\n".join(new_lines), encoding="utf-8")
    except Exception:
        pass

def ensure_kis_token() -> Optional[str]:
    """토큰 존재 보장 (없으면 발급)"""
    global KIS_ACCESS_TOKEN
    if not KIS_ACCESS_TOKEN:
        return refresh_access_token()
    return KIS_ACCESS_TOKEN

def call_kis_get(
    path: str,
    tr_id: str,
    params: Dict[str, Any],
    *,
    max_retry: int = 1,
) -> Dict[str, Any]:
    """
    KIS GET 공통 헬퍼 (Step 10, 11 공용).

    기능:
    1. ensure_kis_token() 호출
    2. requests.get 호출
    3. rt_cd가 만료 코드(EGW00123 등)인 경우 토큰 갱신 후 재시도
    4. 실패 시 RuntimeError 발생

    Args:
        path: '/uapi/...' 경로
        tr_id: API TR ID
        params: Query Parameters
        max_retry: 토큰 만료 시 재시도 횟수
    """
    if not KIS_URL_BASE:
        raise RuntimeError("KIS_URL_BASE가 설정되어 있지 않습니다.")

    # 1. 토큰 존재 확인 (유효성 검사는 API 호출 결과로 판단)
    ensure_kis_token()

    url = f"{KIS_URL_BASE.rstrip('/')}/{path.lstrip('/')}"

    for attempt in range(max_retry + 1):
        headers = get_api_headers(tr_id)

        try:
            res = requests.get(url, headers=headers, params=params, timeout=10)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            raise RuntimeError(f"KIS GET 통신 실패 ({path}, 시도={attempt+1}): {e}") from e

        rt_cd = data.get("rt_cd")

        # 성공
        if rt_cd == "0":
            return data

        # 토큰 만료 코드가 발생하면 갱신 후 재시도
        if rt_cd in ("EGW00123", "EGW00121") and attempt < max_retry:
            print(f"[INFO] 토큰 만료(rt_cd={rt_cd}), refresh 후 재시도...")
            refresh_access_token()
            continue

        # 그 외 API 에러
        msg = data.get("msg1") or data.get("msg_cd") or "알 수 없는 오류"
        raise RuntimeError(f"KIS API 오류 (path={path}, rt_cd={rt_cd}, msg={msg})")

    raise RuntimeError(f"KIS GET 실패: 최대 재시도({max_retry}) 초과. path={path}")

def get_product_basic_info(
    pdno: str,
    prdt_type_cd: str = "300",  # 국내 주식/ETF
) -> Dict[str, Any]:
    """
    상품기본조회(search-info)를 호출해서
    코드/유형 기준으로 상품 메타 정보를 가져옵니다.
    """
    path = "/uapi/domestic-stock/v1/quotations/search-info"
    tr_id = "CTPF1604R"

    code = str(pdno).strip().zfill(6)

    params = {
        "PDNO": code,
        "PRDT_TYPE_CD": prdt_type_cd,
    }

    data = call_kis_get(path, tr_id, params)
    output = data.get("output") or {}

    if not output:
        raise RuntimeError(f"상품기본조회 실패: PDNO={code}, PRDT_TYPE_CD={prdt_type_cd}")

    return output


def get_etf_name_from_kis(etf_code: str, *, prdt_type_cd: str = "300") -> Optional[str]:
    """
    KIS 상품기본조회(search-info)를 이용한 ETF 한글명 조회.
    - mst가 없을 때 백업용으로 사용.
    - 실패 시 None 리턴.
    """
    code = str(etf_code).strip().zfill(6)

    try:
        info = get_product_basic_info(code, prdt_type_cd=prdt_type_cd)
    except Exception:
        # 백업 함수라 여기서는 조용히 None으로 돌려보냅니다.
        return None

    # 상품명 쪽 우선순위: prdt_name → prdt_name120
    name = (info.get("prdt_name") or info.get("prdt_name120") or "").strip()
    return name or None