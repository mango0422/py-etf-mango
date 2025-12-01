"""
KIS 공통 유틸 + KRX MST 처리 유틸 모듈
- 다른 주피터 노트북에서 import 해서 사용하는 용도.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Dict, Any, List

import requests
import pandas as pd
from dotenv import load_dotenv

# =============================================================================
# 0. 프로젝트 경로 및 폴더 구조
#    - __file__ 기준으로 루트 계산 (노트북 위치와 상관없이 동작하도록)
# =============================================================================
PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

RAW_MST_DIR = PROJECT_ROOT / "mst_raw"
OUT_DIR     = PROJECT_ROOT / "mst_fixed"
RAW_MST_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# 1. .env 로부터 KIS 환경 변수 로딩
# =============================================================================
load_dotenv(PROJECT_ROOT / ".env")

KIS_APP_KEY: Optional[str] = os.getenv("KIS_APP_KEY")
KIS_APP_SECRET: Optional[str] = os.getenv("KIS_APP_SECRET")
KIS_ACCESS_TOKEN: Optional[str] = os.getenv("KIS_ACCESS_TOKEN")
KIS_URL_BASE: str = os.getenv(
    "KIS_URL_BASE",
    "https://openapivts.koreainvestment.com:29443",  # 기본값: 모의투자
)
#   - 실전: https://openapi.koreainvestment.com:9443
#   - 모의: https://openapivts.koreainvestment.com:29443

# =============================================================================
# 2. 문자열 → float 변환 유틸
# =============================================================================
def to_float(value) -> Optional[float]:
    """
    쉼표/공백이 섞인 문자열을 float로 변환하는 유틸 함수.
    - 예: "12,345 " → 12345.0
    - KIS 응답에서 금액/수치 필드 처리에 재사용.
    """
    try:
        return float(str(value).replace(",", "").strip())
    except Exception:
        return None


# =============================================================================
# 3. KIS 공통 헤더 생성 함수
# =============================================================================
def get_api_headers(tr_id: str) -> Dict[str, str]:
    """
    KIS 공통 헤더 생성 (접근토큰 포함).
    - tr_id: KIS 문서에 나오는 TR ID (예: FHKST03010100)
    """
    global KIS_ACCESS_TOKEN

    auth = f"Bearer {KIS_ACCESS_TOKEN}" if KIS_ACCESS_TOKEN else ""

    return {
        "content-type": "application/json",
        "authorization": auth,
        "appkey": KIS_APP_KEY or "",
        "appsecret": KIS_APP_SECRET or "",
        "tr_id": tr_id,
        "custtype": "P",  # 개인
    }


# =============================================================================
# 4. KIS OAuth 토큰 발급/갱신
# =============================================================================
def refresh_access_token() -> Optional[str]:
    """
    KIS OAuth 토큰 재발급.
    1) PATH, URL 정의
    2) headers, body 정의
    3) requests.post 호출
    4) access_token 추출 → 전역 변수 + .env에 반영
    """
    global KIS_ACCESS_TOKEN

    if not (KIS_APP_KEY and KIS_APP_SECRET and KIS_URL_BASE):
        raise RuntimeError("KIS_APP_KEY / KIS_APP_SECRET / KIS_URL_BASE 환경변수가 필요합니다.")

    TOKEN_PATH = "oauth2/tokenP"
    TOKEN_URL  = f"{KIS_URL_BASE}/{TOKEN_PATH}"

    headers = {
        "content-type": "application/json",
    }
    body = {
        "grant_type": "client_credentials",
        "appkey": KIS_APP_KEY,
        "appsecret": KIS_APP_SECRET,
    }

    res = requests.post(TOKEN_URL, headers=headers, json=body, timeout=5)
    res.raise_for_status()

    data = res.json()
    access_token = data.get("access_token")
    if not access_token:
        raise RuntimeError(f"KIS 토큰 발급 실패: {data}")

    KIS_ACCESS_TOKEN = access_token

    # .env에 토큰 갱신 (편의용)
    env_path = PROJECT_ROOT / ".env"
    try:
        lines: List[str] = []
        if env_path.exists():
            lines = env_path.read_text(encoding="utf-8").splitlines()

        new_lines: List[str] = []
        token_written = False
        for line in lines:
            if line.startswith("KIS_ACCESS_TOKEN="):
                new_lines.append(f"KIS_ACCESS_TOKEN={access_token}")
                token_written = True
            else:
                new_lines.append(line)

        if not token_written:
            new_lines.append(f"KIS_ACCESS_TOKEN={access_token}")

        env_path.write_text("\n".join(new_lines), encoding="utf-8")
    except Exception:
        # 강의용: .env 업데이트 실패는 치명적 에러로 보지 않는다.
        pass

    return access_token


def ensure_kis_token() -> Optional[str]:
    """
    '토큰이 하나는 있어야 한다'는 전제만 맞추고 싶을 때 사용하는 함수.

    - 메모리에 토큰이 없으면: refresh_access_token() 호출
    - 이미 있으면: 그대로 사용
    - 토큰 만료 여부는 각 API 호출 응답(rt_cd)에서 판단
    """
    global KIS_ACCESS_TOKEN

    if not KIS_ACCESS_TOKEN:
        return refresh_access_token()
    return KIS_ACCESS_TOKEN


# =============================================================================
# 5. MST 파싱: 고정폭 레코드 → DataFrame
# =============================================================================
SZ_SHRNCODE  = 9   # 단축코드 길이
SZ_STNDCODE  = 12  # 표준코드 길이
SZ_KORNAME   = 40  # 한글 종목명
SZ_KORNAME20 = 20  # 짧은 한글명/회원명

EQUITY_SCHEMA = [
    ("short_code", SZ_SHRNCODE),  # 예: A005930 형태
    ("std_code",   SZ_STNDCODE),
    ("name",       SZ_KORNAME),
]


def read_mst_lines(path: Path) -> List[bytes]:
    """
    MST 파일 한 줄은 '고정 길이 레코드'이기 때문에
    텍스트가 아니라 '바이트 단위'로 읽어오는 것이 안전합니다.
    """
    lines: List[bytes] = []
    with path.open("rb") as f:
        for raw in f:
            line = raw.rstrip(b"\r\n")
            if line:
                lines.append(line)
    if not lines:
        raise ValueError(f"{path} is empty")
    return lines


def parse_fixed_width_lines(
    lines: List[bytes],
    schema,
    *,
    encoding: str = "cp949",
) -> pd.DataFrame:
    """
    MST와 같이 '한 줄이 고정폭 레코드'인 바이너리 파일을
    schema 정보를 사용해 잘라서 DataFrame으로 변환.
    """
    record_len = max(len(l) for l in lines)

    offsets: List[tuple[str, int, int]] = []
    offset = 0
    for name, length in schema:
        offsets.append((name, offset, length))
        offset += length

    columns = {name: [] for name, _ in schema}

    for line in lines:
        if len(line) < record_len:
            line = line.ljust(record_len, b" ")

        for name, start, length in offsets:
            raw = line[start:start + length]
            columns[name].append(
                raw.decode(encoding, errors="ignore").rstrip()
            )

    return pd.DataFrame(columns)


def build_equity_master() -> pd.DataFrame:
    """
    - kospi/kosdaq/konex MST 파일을 모두 읽어서
    - (short_code, std_code, name)만 추출한 뒤
    - 하나의 통합 테이블(equity_master.csv)을 생성.
    """
    dfs: List[pd.DataFrame] = []

    for fname in ("kospi_code.mst", "kosdaq_code.mst", "konex_code.mst"):
        path = RAW_MST_DIR / fname
        if not path.exists():
            print(f"⚠️ {path} 없음, 스킵")
            continue

        lines = read_mst_lines(path)
        df = parse_fixed_width_lines(lines, EQUITY_SCHEMA)
        dfs.append(df)

    if not dfs:
        raise RuntimeError("MST 원본을 찾지 못했습니다. mst_raw 폴더를 확인하세요.")

    merged = pd.concat(dfs, ignore_index=True)

    out_csv = OUT_DIR / "equity_master.csv"
    merged.to_csv(out_csv, index=False, encoding="utf-8-sig")
    print(f"[SAVE] equity_master.csv → {out_csv}")

    return merged


# =============================================================================
# 6. equity_master 로딩 & 코드/이름 조회 유틸
# =============================================================================
def load_equity_master() -> pd.DataFrame:
    """
    mst_fixed/equity_master.(parquet|csv)를 읽어서 DataFrame으로 반환.
    """
    eq_path_parquet = OUT_DIR / "equity_master.parquet"
    eq_path_csv     = OUT_DIR / "equity_master.csv"

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


def _extract_6digit_code(s: str) -> Optional[str]:
    """
    'A005930' 같은 문자열에서 숫자만 모아서
    마지막 6자리를 KIS 종목코드로 사용.
    """
    if not isinstance(s, str):
        return None

    digits = "".join(ch for ch in s if ch.isdigit())
    if len(digits) < 6:
        return None

    return digits[-6:]


def find_code_by_name(kor_name: str) -> pd.DataFrame:
    """
    한글 종목명에 특정 문자열이 포함된 종목 리스트를 반환.
    예: find_code_by_name("KODEX 200")
    """
    df = load_equity_master()

    mask = df["name"].str.contains(kor_name, case=False, na=False)
    candidates = df[mask].copy()

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
    """
    검색 결과 중 첫 번째 종목을 선택하여
    - 종목명
    - KIS 코드(6자리)
    를 출력하고, 코드만 반환.
    """
    candidates = find_code_by_name(kor_name)
    if candidates.empty:
        raise ValueError(f"'{kor_name}' 에 해당하는 종목을 찾을 수 없습니다.")

    row = candidates.iloc[0]
    kis_code = row.get("kis_code")
    if not kis_code:
        raise ValueError(
            f"'{kor_name}' 후보에서 KIS 코드(6자리)를 추출하지 못했습니다.\n{row}"
        )

    print(f"[INFO] '{kor_name}' → 선택된 종목: {row.get('name')} (kis_code={kis_code})")
    return str(kis_code)


# =============================================================================
# 7. ETF 코드 → 한글 이름 조회 (MST + KIS)
# =============================================================================
def get_etf_name_from_mst(etf_code: str) -> Optional[str]:
    """
    equity_master에서 KIS 6자리 코드로 ETF 이름을 찾는다.
    (없으면 None)
    """
    df = load_equity_master()

    if "kis_code" not in df.columns:
        if "short_code" in df.columns:
            df["kis_code"] = df["short_code"].apply(_extract_6digit_code)
        elif "std_code" in df.columns:
            df["kis_code"] = df["std_code"].apply(_extract_6digit_code)

    if "kis_code" not in df.columns:
        return None

    mask = df["kis_code"] == str(etf_code)
    hit = df[mask]
    if hit.empty:
        return None

    name = str(hit.iloc[0]["name"]).strip()
    return name or None


def get_etf_name_from_kis(etf_code: str) -> Optional[str]:
    """
    KIS '종목검색' API를 사용해 ETF 이름을 조회.
    (MST에서 못 찾았을 때 보완용)
    """
    if not KIS_URL_BASE:
        return None

    PATH = "uapi/domestic-stock/v1/quotations/search-stock-info"
    URL  = f"{KIS_URL_BASE}/{PATH}"

    params = {
        "PRDT_TYPE_CD": "512",   # 512: ETF/ETN 상품코드 (문서 기준)
        "PDNO": etf_code,
    }
    headers = get_api_headers("CTPF1604R")

    try:
        res = requests.get(URL, headers=headers, params=params, timeout=5)
        data = res.json()
    except Exception as e:
        print(f"⚠️ KIS ETF 이름 조회 실패: {e}")
        return None

    rt_cd = data.get("rt_cd")

    # 토큰 만료 처리
    if rt_cd in ["EGW00123", "EGW00121"]:
        refresh_access_token()
        headers = get_api_headers("CTPF1604R")
        try:
            res = requests.get(URL, headers=headers, params=params, timeout=5)
            data = res.json()
        except Exception:
            return None
        rt_cd = data.get("rt_cd")

    if rt_cd != "0" or not data.get("output"):
        return None

    output = data["output"]
    row = output[0] if isinstance(output, list) else output

    name = row.get("prdt_name") or row.get("hts_kor_isnm")
    name = (name or "").strip()

    return name or None


def get_etf_name(etf_code: str) -> str:
    """
    ETF 코드(6자리)를 넣으면
    - MST → 없으면 KIS 순으로 이름을 찾고
    - 둘 다 실패하면 코드 자체를 반환.
    """
    code = str(etf_code)

    name = get_etf_name_from_mst(code)
    if name:
        print(f"ETF 이름(MST): {code} → {name}")
        return name

    name = get_etf_name_from_kis(code)
    if name:
        print(f"ETF 이름(KIS): {code} → {name}")
        return name

    print(f"ETF 이름 조회 실패 → 코드 사용 ({code})")
    return code


# =============================================================================
# 8. 외부로 공개할 심볼 정리 (선택)
# =============================================================================
__all__ = [
    # 경로 관련
    "PROJECT_ROOT",
    "DATA_DIR",
    "RAW_MST_DIR",
    "OUT_DIR",

    # KIS 환경 변수
    "KIS_APP_KEY",
    "KIS_APP_SECRET",
    "KIS_ACCESS_TOKEN",
    "KIS_URL_BASE",

    # MST 고정폭 스키마 상수
    "SZ_SHRNCODE",
    "SZ_STNDCODE",
    "SZ_KORNAME",
    "SZ_KORNAME20",
    "EQUITY_SCHEMA",

    # 유틸 함수들
    "to_float",
    "get_api_headers",
    "refresh_access_token",
    "ensure_kis_token",

    "read_mst_lines",
    "parse_fixed_width_lines",
    "build_equity_master",
    "load_equity_master",
    "find_code_by_name",
    "pick_single_code",

    "get_etf_name_from_mst",
    "get_etf_name_from_kis",
    "get_etf_name",
]


if __name__ == "__main__":
    # 모듈 단독 실행 시 간단한 테스트용
    print("== kis_env self test ==")
    try:
        eq_master = build_equity_master()
        print("equity_master preview:")
        print(eq_master.head())
    except Exception as e:
        print("⚠️ equity_master 생성/로딩 테스트 실패:", e)

    try:
        ensure_kis_token()
        print("KIS_ACCESS_TOKEN:", bool(KIS_ACCESS_TOKEN))
    except Exception as e:
        print("⚠️ 토큰 테스트 실패:", e)
