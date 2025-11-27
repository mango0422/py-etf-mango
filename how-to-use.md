# %% [markdown]
# ## 1️⃣ 필수 라이브러리 설치 블록

# %%
# ETF 분석 및 시각화, 백테스팅 라이브러리 설치
!pip install pandas numpy plotly bt yfinance requests nbformat python-dotenv

# %% [markdown]
# ## 2️⃣ KIS 환경 설정 & 공통 헤더 생성 블록
# - **역할**: 이후 모든 API 호출에서 헤더/환경을 공통으로 쓰기 위한 준비.
# - **데이터 포맷**: 아직 응답 없음. 이후 `requests.get(...).json()` 형태로 딕셔너리 획득.

# %%
!pip install requests pandas python-dotenv numpy

import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')

# .env에서 KIS 설정 읽기
load_dotenv()
KIS_URL_BASE     = os.getenv("KIS_URL_BASE")
KIS_APP_KEY      = os.getenv("KIS_APP_KEY")
KIS_APP_SECRET   = os.getenv("KIS_APP_SECRET")
KIS_ACCESS_TOKEN = os.getenv("KIS_ACCESS_TOKEN")

ETF_CODE = "069500"  # 기본 분석 대상 (필요 시 변경)

def to_float(value, default=None):
    """문자열 숫자 → float 변환 (콤마/공백 안전 처리)"""
    try:
        return float(str(value).replace(",", "").strip())
    except Exception:
        return default

def get_api_headers(tr_id: str) -> dict:
    """
    KIS API 공통 헤더 생성

    Parameters
    ----------
    tr_id : str
        KIS 거래ID (예: FHPST02400000: ETF 시세조회)

    Returns
    -------
    dict : requests.get / post에 바로 넣을 수 있는 헤더
    """
    return {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {KIS_ACCESS_TOKEN}",
        "appkey": KIS_APP_KEY,
        "appsecret": KIS_APP_SECRET,
        "tr_id": tr_id,
        "custtype": "P",  # 개인: P, 법인: B
    }

print("✅ 환경 설정 완료")
print(f"📊 기본 분석 대상 ETF: {ETF_CODE}")

# %% [markdown]
# ## 3️⃣ 토큰 발급 & 검증 블록
# 
# - **이 블록에서 얻는 수치/정보**
# 
#   - `access_token` 문자열 (실제 인증에 사용)
#   - `expires_in`(초), `access_token_token_expired`(만료 시각 문자열)
#   - 실제 투자 지표는 아니고, **모든 KIS 호출의 기반**입니다.
# 
# - **테스트 호출 (`inquire-price`)에서는 `rt_cd`만 사용**하고, 나머지 시세 정보는 버립니다.

# %%
def refresh_access_token():
    """
    [API] POST /oauth2/tokenP
    - 역할: access_token 재발급
    - 요청 body (JSON):
        {
            "grant_type": "client_credentials",
            "appkey":    KIS_APP_KEY,
            "appsecret": KIS_APP_SECRET
        }
    - 응답 (JSON 주요 필드):
        access_token, expires_in, access_token_token_expired
    """
    token_url = f"{KIS_URL_BASE}/oauth2/tokenP"
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": KIS_APP_KEY,
        "appsecret": KIS_APP_SECRET
    }

    try:
        response = requests.post(token_url, headers=headers, json=body, timeout=5)
        data = response.json()
    except Exception as e:
        print(f"❌ 토큰 발급 중 오류: {e}")
        return None

    if response.status_code != 200 or not data.get("access_token"):
        print(f"❌ 토큰 발급 실패: {data}")
        return None

    new_token  = data["access_token"]
    expires_in = data.get("expires_in", 86400)
    expired_at = data.get("access_token_token_expired", "")

    print(f"✅ 토큰 재발급 성공")
    print(f"   만료 시각: {expired_at}")
    print(f"   유효 시간: {expires_in}초 ({expires_in/3600:.1f}시간)")

    # 메모리 상의 토큰 업데이트
    global KIS_ACCESS_TOKEN
    KIS_ACCESS_TOKEN = new_token

    # .env 파일도 업데이트 (선택)
    try:
        env_path = Path('.env')
        if env_path.exists():
            lines = env_path.read_text().splitlines()
        else:
            lines = []

        new_lines = []
        token_updated = False

        for line in lines:
            if line.startswith('KIS_ACCESS_TOKEN='):
                new_lines.append(f'KIS_ACCESS_TOKEN={new_token}')
                token_updated = True
            else:
                new_lines.append(line)

        if not token_updated:
            new_lines.append(f'KIS_ACCESS_TOKEN={new_token}')

        env_path.write_text('\n'.join(new_lines))
        print("   📝 .env 파일 .env 업데이트 완료")
    except Exception as e:
        print(f"   ⚠️ .env 파일 업데이트 실패 (무시 가능): {e}")

    return new_token


def validate_and_refresh_token():
    """
    [API] GET /uapi/etfetn/v1/quotations/inquire-price (테스트용)
    - 역할: 현재 토큰이 유효한지 확인
    - 사용 필드: rt_cd (결과코드)만 사용
        rt_cd == "0"      → 정상
        rt_cd == EGW00123 → 토큰 만료/무효
    """
    test_url = f"{KIS_URL_BASE}/uapi/etfetn/v1/quotations/inquire-price"
    test_params = {"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": "069500"}
    test_headers = get_api_headers("FHPST02400000")

    try:
        response = requests.get(test_url, headers=test_headers, params=test_params, timeout=5)
        data = response.json()
    except requests.exceptions.Timeout:
        print("⚠️ API 응답 시간 초과 - 기존 토큰 사용")
        return KIS_ACCESS_TOKEN
    except Exception as e:
        print(f"⚠️ 토큰 검증 중 오류 - 기존 토큰 사용: {e}")
        return KIS_ACCESS_TOKEN

    rt_cd = data.get("rt_cd")

    if rt_cd == "0":
        print("✅ 기존 토큰 유효함")
        return KIS_ACCESS_TOKEN

    # 토큰 관련 에러 → 재발급
    if rt_cd in ["EGW00123", "EGW00121"]:
        print("⚠️ 토큰 만료/무효 감지, 재발급 시도...")
    else:
        print(f"⚠️ API 응답 오류({rt_cd}), 토큰 재발급 시도...")

    return refresh_access_token()


print("🔐 접근 토큰 검증 중...")
KIS_ACCESS_TOKEN = validate_and_refresh_token()

if not KIS_ACCESS_TOKEN:
    print("❌ 토큰 발급/갱신 실패 - API 키/시크릿 확인 필요")
else:
    print("✅ 토큰 준비 완료\n")


# %% [markdown]
# ## 1. ETF 현재가·NAV·AUM·TE API
# 
# `/uapi/etfetn/v1/quotations/inquire-price`

# %% [markdown]
# ### 1-1. ETF 기본 시세 + NAV + AUM + 추적오차
# 
# - **직접 제공값**
# 
#   - 시세·유동성: `stck_prpr`, `acml_vol`, `prdy_vol`
#   - NAV: `nav`, `nav_prdy_vrss`, `nav_prdy_ctrt`
#   - AUM(총·유통): `etf_ntas_ttam`, `etf_crcl_ntas_ttam` (※ 1억 원 단위)
#   - 유통주수: `etf_crcl_stcn`
#   - 설정일: `stck_lstn_date`
#   - 추적오차: `trc_errt` (보통 연간 TE %)
# 
# - **이걸로 계산한 파생 지표**
# 
#   - 운용 기간(년/일): `years_since`, `days_since`
#   - AUM(원/억원/조원): `aum_total`, `aum_billion`, `aum_trillion`
#   - 괴리율: `premium` (%)
#   - AUM 규모에 따른 분류: mega/large/medium/small 등 (3강 마지막 JSON에서 사용)

# %%
# 1) ETF 시세 및 기본 정보 조회
url = f"{KIS_URL_BASE}/uapi/etfetn/v1/quotations/inquire-price"
params = {
    "FID_COND_MRKT_DIV_CODE": "J",   # ETF/ETN 시장
    "FID_INPUT_ISCD": ETF_CODE       # 예: 069500
}
headers = get_api_headers("FHPST02400000")

response = requests.get(url, headers=headers, params=params, timeout=5)
data = response.json()

if data.get("rt_cd") != "0":
    raise RuntimeError(f"❌ ETF 시세 조회 실패: {data.get('msg1')}")

etf_data = data["output"]

# 2) 이 API로부터 얻는 '원시 필드'
current_price       = to_float(etf_data.get("stck_prpr"))        # 현재가
volume              = to_float(etf_data.get("acml_vol"))         # 금일 거래량
prev_volume         = to_float(etf_data.get("prdy_vol"))         # 전일 거래량
nav                 = to_float(etf_data.get("nav"))              # NAV
nav_change          = to_float(etf_data.get("nav_prdy_vrss"))    # NAV 전일대비
nav_change_pct      = to_float(etf_data.get("nav_prdy_ctrt"))    # NAV 전일대비 %
listing_date_raw    = etf_data.get("stck_lstn_date")             # 상장일(YYYYMMDD)
aum_from_api        = to_float(etf_data.get("etf_ntas_ttam"))    # 총 순자산 (1억원 단위)
aum_circulating_api = to_float(etf_data.get("etf_crcl_ntas_ttam"))  # 유통 순자산 (1억원 단위)
circulating_shares  = to_float(etf_data.get("etf_crcl_stcn"))    # 유통주수
tracking_error_api  = to_float(etf_data.get("trc_errt"))         # 추적오차 (%)

# 3) 파생 지표 계산 (코드 그대로 활용)
#    - 설정일/운용기간
listing_date = None
years_since = None
days_since = None
if listing_date_raw:
    listing_date = datetime.strptime(listing_date_raw, "%Y%m%d")
    days_since = (datetime.now() - listing_date).days
    years_since = days_since / 365.25

#    - AUM: NAV × 유통주수 (원 단위)
aum_from_calc = None
if nav and circulating_shares:
    aum_from_calc = nav * circulating_shares   # 원 단위

#    - AUM 최종값/단위 변환
if aum_from_calc:
    aum_total   = aum_from_calc
    aum_billion = aum_total / 100_000_000      # 억원
    aum_trillion = aum_billion / 10_000        # 조원
else:
    # 계산 불가 시 API 제공값(1억원 단위)을 원으로 변환
    aum_total = aum_from_api * 100_000_000 if aum_from_api else None
    aum_billion = aum_total / 100_000_000 if aum_total else None
    aum_trillion = aum_billion / 10_000 if aum_billion else None

#    - 괴리율: (현재가 - NAV) / NAV
premium = None
if current_price and nav and nav > 0:
    premium = (current_price - nav) / nav * 100

print(f"📌 현재가: {current_price:,.0f}원")
print(f"📌 NAV: {nav:,.0f}원, 전일대비 {nav_change:+,.0f}원 ({nav_change_pct:+.2f}%)")
print(f"📌 괴리율: {premium:+.3f}%")
print(f"📌 총 순자산(AUM): {aum_trillion:.2f}조원" if aum_trillion and aum_trillion >= 1
      else f"📌 총 순자산(AUM): {aum_billion:,.0f}억원" if aum_billion else "📌 AUM: 데이터 없음")
print(f"📌 추적오차(API): {tracking_error_api:.4f}%" if tracking_error_api is not None else "📌 추적오차(API): 없음")


# %% [markdown]
# ### 1-2. 동일 API에서 ETF 분류/테마 정보 읽기
# 
# > 같은 `inquire-price`지만, 4강에서는 **“분류/테마 정보”** 필드를 추가로 활용합니다.
# 
# **이 필드들로 할 수 있는 일**
# 
# - 동일한 `etf_div_name`을 가진 ETF끼리 **동일 카테고리 비교**
# - 대표업종·목표지수업종을 기준으로 **테마별 ETF 묶기**

# %%
url = f"{KIS_URL_BASE}/uapi/etfetn/v1/quotations/inquire-price"
params = {
    "fid_cond_mrkt_div_code": "J",
    "fid_input_iscd": ETF_CODE
}
headers = get_api_headers("FHPST02400000")

response = requests.get(url, headers=headers, params=params, timeout=5)
info = response.json()

if info.get("rt_cd") == "0":
    output = info.get("output", {})
    etf_div_name   = output.get("etf_div_name", "-")               # ETF 분류명
    etf_rprs_bstp  = output.get("etf_rprs_bstp_kor_isnm", "-")     # 대표업종
    etf_trgt_nmix  = output.get("etf_trgt_nmix_bstp_code", "-")    # 목표지수업종 코드

    print("📊 ETF 분류 정보")
    print(f"   - 분류: {etf_div_name}")
    print(f"   - 대표업종: {etf_rprs_bstp}")
    print(f"   - 목표지수업종코드: {etf_trgt_nmix}")
else:
    print(f"❌ ETF 분류 정보 조회 실패: {info.get('msg1')}")

# %% [markdown]
# ## 2. 종목/ETF 메타 정보 API
# 
# `/uapi/domestic-stock/v1/quotations/search-stock-info`

# %% [markdown]
# ### 2-1. ETF 이름 조회 (PRDT_TYPE_CD=512)
# 
# - **얻는 수치/정보**
# 
#   - `prdt_name`, `hts_kor_isnm` : ETF 한글명
# 
# - **범위**
# 
#   - ETF에 한정 (`PRDT_TYPE_CD="512"`).
#   - 보통 “ETF 이름만 필요할 때”는 KIS+네이버를 조합해서 사용.

# %%
def get_etf_name_from_kis(etf_code: str):
    """
    [API] GET /uapi/domestic-stock/v1/quotations/search-stock-info
    - ETF 이름 조회용 사용 예
    - PRDT_TYPE_CD = "512" (ETF)
    """
    url = f"{KIS_URL_BASE}/uapi/domestic-stock/v1/quotations/search-stock-info"
    params = {
        "PRDT_TYPE_CD": "512",  # ETF
        "PDNO": etf_code
    }
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
    if isinstance(output, list) and output:
        row = output[0]
    else:
        row = output

    # prdt_name 또는 hts_kor_isnm 중 하나 사용
    return row.get("prdt_name") or row.get("hts_kor_isnm")


name_kis = get_etf_name_from_kis(ETF_CODE)
print("📌 KIS에서 조회한 ETF 이름:", name_kis)

# %% [markdown]
# ### 2-2. 구성 종목 상세 정보 (섹터·시총) (PRDT_TYPE_CD=300)
# 
# 4강에서 **구성 종목별 섹터·시총·상장일**을 얻을 때 사용하는 호출입니다.
# 
# **이 API로 얻는 수치 → 4강에서의 활용**
# 
# - `sector`, `sector_code`
#   → **섹터별 비중/종목 수 집계** (섹터 집중도 분석)
# - `market_cap` (억 단위)
#   → **대형주(10조↑) / 중형주(1~10조) / 소형주(1조↓)** 비중 계산
# - `listing_date`, `listing_shares`, `par_value`
#   → 필요 시 “신규 상장/구주 비중/액면분할” 등 추가 분석에 활용 가능

# %%
def get_stock_detail(stock_code: str):
    """
    [API] GET /uapi/domestic-stock/v1/quotations/search-stock-info
    - PRDT_TYPE_CD = "300" (주식/ETF/ETN 전체)
    - 여기서는 국내 개별주 상세 정보용
    """
    url = f"{KIS_URL_BASE}/uapi/domestic-stock/v1/quotations/search-stock-info"
    params = {
        "PRDT_TYPE_CD": "300",
        "PDNO": stock_code
    }
    headers = get_api_headers("CTPF1002R")

    try:
        res = requests.get(url, headers=headers, params=params, timeout=5)
        data = res.json()
    except Exception as e:
        print(f"⚠️ {stock_code} 조회 실패: {e}")
        return None

    if data.get("rt_cd") != "0":
        return None

    output = data.get("output", {})

    # 이 API로부터 추출하는 주요 필드
    detail = {
        "sector":        output.get("std_idst_clsf_cd_name", "-"),  # 섹터명
        "sector_code":   output.get("std_idst_clsf_cd", "-"),       # 섹터 코드
        "market_cap":    to_float(output.get("cpta", 0)),           # 시가총액(억)
        "listing_date":  output.get("scts_mket_lstg_dt", "-"),      # 상장일
        "listing_shares":to_float(output.get("lstg_stqt", 0)),      # 상장주식수
        "par_value":     to_float(output.get("papr", 0)),           # 액면가
    }
    return detail

# 예: 구성종목 중 한 종목 조회
example_code = "005930"  # 삼성전자
detail = get_stock_detail(example_code)
print("📌 종목 상세 정보:", detail)

# %% [markdown]
# ## 3. 네이버 ETF 리스트 API
# 
# `https://finance.naver.com/api/sise/etfItemList.nhn`

# %% [markdown]
# ### 3-1. ETF 이름 조회 (KIS 실패 시 폴백)
# 
# - **이 API로 얻는 정보**
# 
#   - `itemcode`, `itemname` 등 **ETF 기본 리스트 및 이름**
# 
# - **범위**
# 
#   - **모든 상장 ETF 전체 리스트**를 한 번에 가져오기 때문에,
#     나중에 “국내 ETF 전체 스크리닝”에도 활용 가능.

# %%
def get_etf_name_from_naver(etf_code: str):
    """
    [API] GET https://finance.naver.com/api/sise/etfItemList.nhn
    - 모든 상장 ETF 리스트 JSON
    - 여기서는 itemcode == etf_code 인 항목의 itemname 사용
    """
    try:
        url = "https://finance.naver.com/api/sise/etfItemList.nhn"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        data = res.json()
    except Exception as e:
        print(f"⚠️ 네이버 ETF 리스트 조회 실패: {e}")
        return None

    for item in data.get("result", {}).get("etfItemList", []):
        if str(item.get("itemcode")) == etf_code:
            # 주요 필드 예: itemname, itemcode, ...
            return item.get("itemname")

    return None


def get_etf_name(etf_code: str):
    """KIS 우선, 실패 시 네이버 폴백"""
    name = get_etf_name_from_kis(etf_code)
    if name:
        print("✅ ETF 이름 조회 성공 (KIS)")
        return name

    name = get_etf_name_from_naver(etf_code)
    if name:
        print("✅ ETF 이름 조회 성공 (네이버)")
        return name

    print("⚠️ ETF 이름 조회 실패 → 종목코드 사용")
    return etf_code


etf_name = get_etf_name(ETF_CODE)
print(f"📌 최종 ETF 이름: {etf_name} ({ETF_CODE})")

# %% [markdown]
# ## 4. ETF 구성 종목 API
# 
# `/uapi/etfetn/v1/quotations/inquire-component-stock-price`

# %% [markdown]
# ### 4-1. 구성 종목 리스트 + 비중/평가액/시총
# 
# **이 API로 얻는 수치 → 4강에서의 활용**
# 
# - 종목 단위
# 
#   - `code`, `name`
#   - ETF 내 비중: `weight_pct`
#   - ETF 내 평가액: `valuation`
#   - 현재가: `price`
#   - 시총 정보 (`hts_avls` 존재 시 사용 가능)
#   - 국내/해외 구분 플래그 `is_domestic`
# 
# - 포트폴리오 단위로 파생 계산
# 
#   - **Top 5/10/20 집중도**: 상위 N개 `weight_pct` 합
#   - **국내/해외 비중**: `is_domestic` 기준 비중·종목 수
#   - **(search-stock-info와 결합하여)** 시가총액별·섹터별 분포

# %%
components = []

url = f"{KIS_URL_BASE}/uapi/etfetn/v1/quotations/inquire-component-stock-price"
params = {
    "FID_COND_MRKT_DIV_CODE": "J",     # ETF/ETN
    "FID_INPUT_ISCD": ETF_CODE,
    "FID_COND_SCR_DIV_CODE": "11216"   # 표준 스크리닝 코드
}
headers = get_api_headers("FHKST121600C0")

res = requests.get(url, headers=headers, params=params, timeout=5)
data = res.json()

if data.get("rt_cd") != "0":
    raise RuntimeError(f"❌ 구성 종목 조회 실패: {data.get('msg1')}")

raw_components = data.get("output2", [])
print(f"✅ 구성 종목 {len(raw_components)}개 조회")

for row in raw_components:
    code      = row.get("stck_shrn_iscd")          # 종목코드
    name      = row.get("hts_kor_isnm")            # 종목명
    weight    = to_float(row.get("etf_cnfg_issu_rlim"))  # ETF 내 비중(%)
    price     = to_float(row.get("stck_prpr"))     # 현재가
    valuation = to_float(row.get("etf_vltn_amt"))  # ETF 내 평가액
    mcap_etf  = to_float(row.get("hts_avls"))      # (KIS 제공 시가총액 정보)

    if code and weight:
        components.append({
            "code": code,
            "name": name,
            "weight_pct": weight,
            "price": price,
            "valuation": valuation,
            "market_cap": mcap_etf,
            "is_domestic": code.isdigit() and len(code) == 6
        })

components.sort(key=lambda x: x["weight_pct"], reverse=True)

print("📌 상위 3개 예시:")
for c in components[:3]:
    print(f"  - {c['name']} ({c['code']}): {c['weight_pct']:.2f}%")

# %% [markdown]
# ## 5. 시계열 가격 API
# 
# `/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice`
# 
# 동일 API를 **주기(D/M)와 기간 설정에 따라 다른 분석**에 씁니다.

# %% [markdown]
# ### 5-1. [3강] 일봉으로 20일 평균 거래대금 계산
# 
# - **이 호출에서 사용하는 원시 필드**
# 
#   - `stck_bsop_date` : 날짜
#   - `stck_clpr` : 종가
#   - `acml_vol` : 거래량
# 
# - **파생 지표**
# 
#   - 20일 평균 거래량, 20일 평균 거래대금
#   - “오늘 거래대금 vs 20일 평균” 비율 → 유동성 평가

# %%
print("\n📊 최근 20거래일 일평균 거래대금")

daily_url = f"{KIS_URL_BASE}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
daily_params = {
    "FID_COND_MRKT_DIV_CODE": "J",
    "FID_INPUT_ISCD": ETF_CODE,
    "FID_INPUT_DATE_1": (datetime.now() - timedelta(days=60)).strftime("%Y%m%d"),  # 60일 범위 내
    "FID_INPUT_DATE_2": datetime.now().strftime("%Y%m%d"),
    "FID_PERIOD_DIV_CODE": "D",   # D = 일봉
    "FID_ORG_ADJ_PRC": "0"
}
daily_headers = get_api_headers("FHKST03010100")

daily_res = requests.get(daily_url, headers=daily_headers, params=daily_params, timeout=5)
daily_data = daily_res.json()

avg_turnover_billion = None

if daily_data.get("rt_cd") == "0" and daily_data.get("output2"):
    daily_list = daily_data["output2"][:20]  # 최근 20거래일
    turnovers = []
    volumes = []

    for row in daily_list:
        close = to_float(row.get("stck_clpr"))   # 종가
        vol   = to_float(row.get("acml_vol"))    # 거래량
        if close and vol:
            turnovers.append(close * vol)
            volumes.append(vol)

    if turnovers:
        avg_turnover_20d = np.mean(turnovers)
        avg_turnover_billion = avg_turnover_20d / 100_000_000
        avg_volume_20d = np.mean(volumes)

        print(f"20일 평균 거래량: {avg_volume_20d:,.0f}주")
        print(f"20일 평균 거래대금: {avg_turnover_billion:,.1f}억원")
else:
    print(f"⚠️ 일봉 데이터 조회 실패: {daily_data.get('msg1')}")

# %% [markdown]
# ### 5-2. [5강] 일봉으로 변동성·MDD·샤프·소르티노 계산
# 
# - **동일 API, 다른 “분석 범위”**
# 
#   - 3강: **최근 20일**만 잘라서 **평균 거래대금** 중심
#   - 5강: **최대 5년**을 합쳐서 **장기 변동성·MDD·위험조정 성과** 계산

# %%
# 최근 5년치 일봉을 여러 번(최대 100개씩) 조회하여 합치기
daily_prices_list = []

for year_offset in range(5):
    end = datetime.now() - timedelta(days=365 * year_offset)
    start = end - timedelta(days=365)

    url = f"{KIS_URL_BASE}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": ETF_CODE,
        "FID_INPUT_DATE_1": start.strftime("%Y%m%d"),
        "FID_INPUT_DATE_2": end.strftime("%Y%m%d"),
        "FID_PERIOD_DIV_CODE": "D",  # 일봉
        "FID_ORG_ADJ_PRC": "0"
    }
    headers = get_api_headers("FHKST03010100")

    res = requests.get(url, headers=headers, params=params, timeout=5)
    data = res.json()

    if data.get("rt_cd") == "0":
        for row in data.get("output2", []):
            date_str = row.get("stck_bsop_date")
            close    = to_float(row.get("stck_clpr"))
            if date_str and close:
                date = pd.to_datetime(date_str, format="%Y%m%d")
                daily_prices_list.append({"date": date, "close": close})

# DataFrame 정리
if daily_prices_list:
    daily_df = (pd.DataFrame(daily_prices_list)
                  .drop_duplicates(subset=["date"])
                  .sort_values("date")
                  .set_index("date"))
    daily_prices = daily_df["close"]
else:
    daily_prices = pd.Series(dtype=float)

# 변동성 / MDD / 샤프 / 소르티노 예시
if not daily_prices.empty:
    daily_returns = daily_prices.pct_change().dropna()

    # 변동성
    daily_vol = daily_returns.std() * 100
    annual_vol = daily_vol * np.sqrt(252)
    print(f"연율 변동성: {annual_vol:.2f}%")

    # MDD
    import quantstats as qs
    qs.extend_pandas()

    mdd = qs.stats.max_drawdown(daily_returns) * 100
    print(f"MDD: {mdd:.2f}%")

    # 샤프/소르티노
    RISK_FREE_RATE = 0.035
    sharpe_ratio  = qs.stats.sharpe(daily_returns, rf=RISK_FREE_RATE)
    sortino_ratio = qs.stats.sortino(daily_returns, rf=RISK_FREE_RATE)
    print(f"샤프 비율: {sharpe_ratio:.3f}")
    print(f"소르티노 비율: {sortino_ratio:.3f}")

# %% [markdown]
# ### 5-3. [5강] 월봉으로 기간별 수익률·CAGR·베타/알파 계산
# 
# - **동일 API, 다른 period**
# 
#   - `"D"`: 단기 리스크(MDD, 변동성, 샤프, 소르티노)
#   - `"M"`: 장기 성과(기간별 수익률, CAGR, 베타/알파)

# %%
def fetch_price_data(etf_code: str, years: int = 5, period: str = "M") -> pd.Series:
    """
    [API] GET /uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice
    - FID_PERIOD_DIV_CODE = "M" → 월봉
    - 최대 100개까지만 반환 (보통 8년 이내)
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * years)

    url = f"{KIS_URL_BASE}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": etf_code,
        "FID_INPUT_DATE_1": start_date.strftime("%Y%m%d"),
        "FID_INPUT_DATE_2": end_date.strftime("%Y%m%d"),
        "FID_PERIOD_DIV_CODE": period,  # "M" = 월봉
        "FID_ORG_ADJ_PRC": "0"
    }
    headers = get_api_headers("FHKST03010100")

    res = requests.get(url, headers=headers, params=params, timeout=5)
    data = res.json()
    if data.get("rt_cd") != "0":
        print(f"❌ 월봉 조회 실패: {data.get('msg1')}")
        return pd.Series(dtype=float)

    rows = []
    for row in data.get("output2", []):
        date_str = row.get("stck_bsop_date")
        close    = to_float(row.get("stck_clpr"))
        if date_str and close:
            date = pd.to_datetime(date_str, format="%Y%m%d")
            rows.append({"date": date, "close": close})

    if not rows:
        return pd.Series(dtype=float)

    df = pd.DataFrame(rows).sort_values("date").set_index("date")
    return df["close"]

# ETF 월봉
monthly_prices = fetch_price_data(ETF_CODE, years=5, period="M")

# ① 기간별 수익률 (1M,3M,6M,1Y,3Y,5Y,YTD)
import quantstats as qs
qs.extend_pandas()

def calculate_period_returns_monthly(prices: pd.Series):
    rets = prices.pct_change().dropna()
    total_months = len(rets)
    result = {}

    # YTD
    year_start = pd.Timestamp(f"{datetime.now().year}-01-01")
    ytd = rets[rets.index >= year_start]
    if len(ytd) > 0:
        result["YTD"] = qs.stats.comp(ytd) * 100

    if total_months >= 1:
        result["1개월"] = qs.stats.comp(rets.tail(1)) * 100
    if total_months >= 3:
        result["3개월"] = qs.stats.comp(rets.tail(3)) * 100
    if total_months >= 6:
        result["6개월"] = qs.stats.comp(rets.tail(6)) * 100
    if total_months >= 12:
        result["1년"] = qs.stats.comp(rets.tail(12)) * 100
    if total_months >= 36:
        result["3년"] = qs.stats.comp(rets.tail(36)) * 100
    if total_months >= 60:
        result["5년"] = qs.stats.comp(rets.tail(60)) * 100
    return result

period_returns = calculate_period_returns_monthly(monthly_prices)
print("📊 기간별 수익률:", period_returns)

# ② CAGR
if len(monthly_prices) >= 12:
    monthly_rets = monthly_prices.pct_change().dropna()
    years = len(monthly_rets) / 12
    total_ret = (monthly_prices.iloc[-1] / monthly_prices.iloc[0]) - 1
    cagr = ((1 + total_ret) ** (1/years) - 1) * 100
    print(f"CAGR: {cagr:.2f}%")

# ③ (옵션) 벤치마크 월봉과 베타/알파
MARKET_CODE = "069500"  # 예시
if MARKET_CODE != ETF_CODE:
    benchmark_monthly = fetch_price_data(MARKET_CODE, years=5, period="M")

    common = monthly_prices.index.intersection(benchmark_monthly.index)
    if len(common) >= 12:
        etf_ret = monthly_prices.loc[common].pct_change().dropna()
        bmk_ret = benchmark_monthly.loc[common].pct_change().dropna()
        cov = etf_ret.cov(bmk_ret)
        var = bmk_ret.var()
        beta = cov / var

        RISK_FREE_RATE = 0.035
        etf_total = qs.stats.comp(etf_ret)
        bmk_total = qs.stats.comp(bmk_ret)
        years = len(etf_ret) / 12
        etf_annual = (1 + etf_total)**(1/years) - 1
        bmk_annual = (1 + bmk_total)**(1/years) - 1
        expected = RISK_FREE_RATE + beta * (bmk_annual - RISK_FREE_RATE)
        alpha = (etf_annual - expected) * 100

        print(f"베타: {beta:.3f}, 알파: {alpha:.3f}%")

# %% [markdown]
# ## 6. 호가·스프레드 API
# 
# `/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn`
# 
# - **직접 제공값**
# 
#   - `askp1`, `bidp1` : 최우선 매도/매수호가
# 
# - **파생 지표**
# 
#   - 절대 스프레드: `askp1 - bidp1`
#   - 상대 스프레드(%): `(askp1 - bidp1) / ((askp1+bidp1)/2) * 100`
#   - 3강에서 **유동성 품질 평가(0.1/0.2/0.3%) 기준**에 활용

# %%
orderbook_url = f"{KIS_URL_BASE}/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn"
orderbook_params = {
    "FID_COND_MRKT_DIV_CODE": "J",
    "FID_INPUT_ISCD": ETF_CODE
}
orderbook_headers = get_api_headers("FHKST01010200")

res = requests.get(orderbook_url, headers=orderbook_headers, params=orderbook_params, timeout=5)
data = res.json()

if data.get("rt_cd") == "0" and data.get("output1"):
    ob = data["output1"]
    ask_price = to_float(ob.get("askp1"))  # 매도1호가
    bid_price = to_float(ob.get("bidp1"))  # 매수1호가

    if ask_price and bid_price and bid_price > 0:
        mid_price   = (ask_price + bid_price) / 2
        spread_abs  = ask_price - bid_price
        spread_pct  = spread_abs / mid_price * 100

        print(f"매수1호가: {bid_price:,.0f}원")
        print(f"매도1호가: {ask_price:,.0f}원")
        print(f"스프레드: {spread_abs:,.0f}원 ({spread_pct:.3f}%)")
else:
    print(f"⚠️ 호가 조회 실패: {data.get('msg1')}")

# %% [markdown]
# ## 7. 분석 결과 저장 포맷 (JSON & CSV)
# 
# API는 아니지만, **“어떤 포맷으로 저장해서 다음 분석/백테스팅에 쓰는지”** 도 정리해두면 좋습니다.

# %% [markdown]
# ### 7-1. etf_metrics JSON (3강 핵심 지표 스냅샷)
# 
# - **역할**
# 
#   - 하나의 ETF에 대한 **“정적 스냅샷 리포트”** 포맷.
#   - API에서 가져온 값 + 파생 지표 모두 정리 → 대시보드/리포트에 바로 사용.

# %%
import json

etf_metrics = {
    "metadata": {
        "as_of": datetime.now().isoformat(),
        "etf_code": ETF_CODE,
        "etf_name": etf_name,
        "data_source": "KIS API + Calculations"
    },
    "basic_info": {
        "listing_date": listing_date.strftime('%Y-%m-%d') if listing_date else None,
        "days_since_listing": days_since,
        "years_since_listing": round(years_since, 2) if years_since else None
    },
    "price": {
        "current_price": current_price,
        "nav": nav,
        "nav_change": nav_change,
        "nav_change_pct": nav_change_pct
    },
    "premium_discount": {
        "value_pct": premium,
        "status": "premium" if premium and premium > 0
                  else "discount" if premium and premium < 0
                  else "neutral",
        "within_normal_range": abs(premium) <= 0.5 if premium is not None else None
    },
    "liquidity": {
        "today_volume": volume,
        "previous_volume": prev_volume,
        "today_turnover_billion": turnover_billion,
        "avg_20d_turnover_billion": avg_turnover_billion,
    },
    # ... (spread, AUM, tracking_error, quality_scores 등 계속)
}

output_path = f"../data/etf_metrics_{ETF_CODE}_latest.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(etf_metrics, f, ensure_ascii=False, indent=2)

print("✅ etf_metrics JSON 저장 완료:", output_path)

# %% [markdown]
# ### 7-2. 백테스팅/시계열용 CSV (5강 + 3강 결합)
# 
# - **역할**
# 
#   - 동일 ETF에 대해 **매일/주기적으로 같은 구조의 행을 append**
#     → `bt`, `pandas`, 기타 백테스트 도구들이 바로 읽어서 사용 가능.

# %%
bt_data_row = {
    "date": datetime.now().strftime('%Y-%m-%d'),
    "time": datetime.now().strftime('%H:%M:%S'),
    "etf_code": ETF_CODE,
    "price": current_price,
    "nav": nav,
    "premium_pct": premium,
    "volume": volume,
    "turnover_billion": turnover_billion,
    "spread_pct": spread_pct if 'spread_pct' in locals() else None,
    "aum_trillion": aum_trillion if 'aum_trillion' in locals() else None,
    "te_pct": tracking_error_api
}

bt_csv_path = f"../data/etf_timeseries_{ETF_CODE}.csv"

if os.path.exists(bt_csv_path):
    df_existing = pd.read_csv(bt_csv_path)
    df_out = pd.concat([df_existing, pd.DataFrame([bt_data_row])], ignore_index=True)
else:
    df_out = pd.DataFrame([bt_data_row])

df_out.to_csv(bt_csv_path, index=False, encoding="utf-8-sig")
print("✅ 시계열 CSV 저장:", bt_csv_path)


