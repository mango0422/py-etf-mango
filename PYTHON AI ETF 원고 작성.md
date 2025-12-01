# PYTHON AI ETF 원고 작성

## 9강

### 9강 역할 정리

- 10·11강에서 쓸 “재료(로우 데이터)”가 **어떤 종류인지 정의**하고
- **최소한의 스키마를 가진 CSV**를 만들어 두는 강의.
- 금융 지표 계산/해석은 전혀 안 하고,

  - `shape`, `columns`, `결측 비율`, `키 중복` 정도만 확인.

### 9강에서 **수집·저장**할 데이터 (지표 관점)

9강에서 “지표를 계산하지는 않지만”,
**이후 지표 계산에 필요한 최소 필드를 포함해서 저장**해두는 게 목표야.

#### 2-1. ETF 기본 정보 로우 (`data/raw/etf_info.csv`)

> **수집 방식(예시)**  
> KIS `search-stock-info` + `inquire-price` API 조합으로 한 번에 모아서 저장.

**컬럼 (후속 지표용 최소 필드)**

- 식별

  - `ticker` (6자리 코드)
  - `name_kor` (ETF 한글명, `get_etf_name_from_kis` 결과)
  - (선택) `name_eng`

- 상장/규모

  - `listing_date` (상장일)
  - `aum` (순자산총액, etf_ntas_ttam)
  - `total_shares` (상장좌수/주식수)

- 거래·유동성(원천 값만)

  - `last_price` (현재가)
  - `daily_volume` (금일 거래량)
  - `daily_tr_value` (금일 거래대금)
  - `prdy_volume` (전일 거래량, 있으면)

- NAV 관련 (원본값 그대로)

  - `nav`
  - `nav_prev`
  - `premium_rate_raw` or `dprt` (괴리율 원본)

- 구조/유형 (플래그는 10강에서 파싱 가능하게 “원본 텍스트” 위주)

  - `mbcr_name` (운용사명)
  - `etf_div_name` (ETF 구분명: 레버리지/인버스/기타 텍스트)
  - `etf_dvdn_cycl` (배당주기)
  - `etf_rprs_bstp_kor_isnm` (대표 지수/섹터명)

- 기타

  - `raw_json` (원하면 전체 응답 JSON을 문자열로 덤프해두는 컬럼 한 개 – 추후 필요시 개발자용)

> 9강에서는 이걸 **그대로만 저장**하고,
> “이 컬럼들을 가지고 10강에서 5·8강 이론에서 이야기한 기본 지표를 계산할 예정” 정도만 언급.

---

#### 2-2. ETF 구성 종목 로우 (`data/raw/holdings_{ticker}.csv`)

> **수집 API**  
> `/uapi/etfetn/v1/quotations/inquire-component-stock-price` (FHKST121600C0)

컬럼

- 기본 키

  - `as_of_date` (스냅샷 기준일, 보통 오늘)
  - `etf_code`
  - `stck_shrn_iscd` (종목 코드 6자리)
  - `hts_kor_isnm` (종목명)

- 평가·비중

  - `stck_prpr` (현재가)
  - `etf_vltn_amt` (ETF 내 평가금액)
  - `hts_avls` (시가총액 비슷한 값 있으면)
  - `weight` (9강에서는 굳이 재계산 안 해도 되지만, API에서 비중이 나올 경우 raw로 함께 저장)

- 나머지 숫자 필드도 가능하면 그대로 저장:

  - `acml_vol`, `acml_tr_pbmn`, `etf_cnfg_issu_rlim` 등
    → 10강에서 필요하면 쓰고, 필요 없으면 무시.

9강에서 하는 검증은:

- `holdings.shape, holdings.columns`
- `holdings.isna().mean()`
- `(etf_code, stck_shrn_iscd, as_of_date)` 중복 여부 체크 정도.

---

#### 2-3. ETF 가격 시계열 로우 (`data/raw/price_{ticker}.csv`)

**수집 API**

- `/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice` (FHKST03010100)

**컬럼**

- 키/시간축

  - `code`
  - `date` (YYYY-MM-DD)
  - `stck_bsop_date` (원본 날짜)

- 가격/거래

  - `stck_clpr` (종가)
  - `stck_oprc`, `stck_hgpr`, `stck_lwpr`
  - `acml_vol`, `acml_tr_pbmn`

- 9강에서 하는 것:

  - 기간 예시 (2015-01-01 ~ 오늘) 호출
  - `sort_values('date')`
  - `(code, date)` 중복 체크
  - 결측 비율 확인만.

> 벤치마크 지수(코스피/코스피200 등) 시계열은
> **11강에서 “위험·상대지표” 설명할 때 따로 처음 등장**시켜도 자연스럽고,
> 9강에서는 “앞으로 벤치마크 지수도 비슷한 방식으로 가져올 것” 정도만 언급하면 충분.

---

### 2-4. 9강에서 **하지 않는 것**

- 상위 10종목 비중, 섹터/시가총액 분포 계산 ❌
- 가중평균 PER/PBR 계산 ❌
- MDD, Sharpe, Beta 등 리스크 지표 계산 ❌
- 레버리지/인버스 플래그 파싱도 “텍스트만 저장” 수준까지만.

9강의 메시지는:

> “우리가 앞으로 쓸 데이터는 이런 **세 가지 테이블**이고,
> 이걸 안전하게 CSV로 저장해 뒀으니
> 10·11강에서는 이 파일들만 읽고 지표 계산에 집중할 수 있다.”

로 깔끔하게 정리.

## 10강

### 10강 역할 정리

- 9강에서 저장한 로우 데이터를 읽어서,

  - 5강(기본 지표), 6강(포트폴리오 지표) 내용을 **숫자로 구현**하는 강의.

- 추가로 필요한 메타는 **여기서 API를 더 호출해서 확장**해도 됨

  - 예: 종목별 섹터, 시가총액, PER/PBR 등.

### 10강에서 **읽는 데이터**

- `data/raw/etf_info.csv`
- `data/raw/holdings_{ticker}.csv`
- (필요하면) `data/raw/price_{ticker}.csv` 에서 “평균 거래량” 정도만 추가 활용 가능

### 10강에서 **추가로 수집할 메타 데이터**

(9강에서 안 가져온 것들)

- 종목 단위 기본 정보 (`search-stock-info`):

  - `std_idst_clsf_cd_name` (표준 산업 분류 – 섹터)
  - `idx_bztp_lcls_cd_name` / `mcls` (업종 대/중분류)
  - `lstg_stqt` (상장주수)

- 종목 단위 현재가/밸류 (`inquire-price`):

  - `hts_avls` (시가총액)
  - `per`, `pbr`, `eps`, `bps`

- ETF 상품 정보 (`search-info` / `search-stock-info` 활용):

  - `prdt_risk_grad_cd` (위험등급)
  - `prdt_clsf_name` (상품분류명)
  - `ivst_prdt_type_cd_name` (투자상품유형)
  - → 이건 8강(특수 ETF)와 연결용

이들 결과는 **10강에서 로컬 변수로만 써도 되고**,
재사용성을 높이려면:

- `data/etf_portfolio_summary/{ticker}_{date}_components_enriched.csv`
- `data/etf_portfolio_summary/{ticker}_{date}_meta.csv`

같은 형태로 “가공 요약” 파일로 저장.

---

### 10강에서 **계산·정리할 지표**

#### 3-1. 5강 연계 – 기본 정보 지표

입력: `etf_info.csv` (+ NAV 스냅샷, 상품 정보)

- (가능하면) 총보수 / 운용보수

  - KIS에서 직접 안 나오면, 여기서는 “AUM/거래량 중심으로 예시”로 가도 됨

- `aum` 기준 AUM 티어

  - `MICRO/SMALL/MEDIUM/LARGE`

- 설정일(상장일) 기준 운용 기간 (년수)
- 최근 20·60일 평균 거래량 (ETF 자체)

  - `price_{ticker}.csv`에서 rolling mean

- 괴리율/추적오차 준비

  - 이 강의에서는 **괴리율(dprt, premium_rate)** 원시값만 보여주고
    “본격적인 추적오차는 11강에서 계산” 정도로 선 긋기.

**10강에서 실제로 하는 일:**

- `etf_info`에서 필요한 컬럼만 뽑아서

  - “5강에서 설명했떤 AUM/규모/설정일/유동성/비용 관련 지표들이 이런 데이터에서 나온다”
    를 **숫자로 한 번 보여주기** (평가/판단은 나중).

---

#### 3-2. 6강 연계 – 포트폴리오 지표

입력:

- `holdings_{ticker}.csv`
- - 종목별 기본정보/현재가 정보 (섹터, 시총, PER 등)

**여기서 계산하는 것들:**

1. **집중도**

   - `top5_concentration`, `top10_concentration`
   - `herfindahl_index`, `effective_n`

2. **섹터/시총 분포**

   - `sector_summary`: 섹터별 `weight` 합
   - `size_summary`: `market_cap` 기반 Large/Mid/Small 비중
   - (선택) 국가별 분포는 해외 ETF 다룰 때 확장

3. **가중평균 밸류에이션**

   - `weighted_avg_per`
   - `weighted_avg_pbr`
   - `weighted_avg_market_cap`

4. **비중 합 확인**

   - `holdings['weight'].sum()`

     - 100%가 아닌 경우:

       - 반올림/NA/현금·파생/기타(ETN·현금 등) 이유를 코드로 확인만 해줌
       - “이게 맞는지” 판단은 10강 후반에 설명,
         리스크/추적오차는 여전히 11강에서.

5. **회전율(포트폴리오 turnover)**

   - 이전 스냅샷 vs 현재 스냅샷 비교
   - `Turnover = Σ |w_t - w_(t-1)| / 2`
   - 회전율이 “어떤 의미를 갖는지” 해석은 살짝 언급하되,
     본격 리스크/비용 영향은 11강/이론에서 다뤄도 됨.

> 10강의 핵심 메시지:
> “6강에서 말한 포트폴리오 관점 지표(상위비중, 섹터/시총 분포, 회전율 등)를
> 실제 ETF `holdings` 데이터와 종목 메타를 가지고 코드로 만들어봤다.”

## 11강

### 11강 역할 정리

- 7강(성과·위험 지표), 8강(레버리지/인버스 특성)을
  **ETF + 벤치마크 시계열**로 구현.
- 9강의 `price_{ticker}.csv`를 그대로 재사용해도 되고,
  필요하다면 11강에서 별도로 다시 호출해 저장해도 됨
  (지금 구조상 `DAILY_PRICE_DIR` 따로 있으니, 11강 전용 저장소로 보는 것도 자연스럽고).

### 11강에서 **추가로 수집할 데이터**

- 벤치마크 지수 일봉 (KOSPI, KOSPI200 등)

  - `/inquire-daily-indexchartprice` (FHKUP03500100)
  - `code` (0001/2001 등), `date`, `bstp_nmix_prpr` → `stck_clpr_float`로 변환

- (필요하다면) ETF 가격도 11강 전용 디렉터리에 다시 저장

  - `data/daily_prices/{code}_daily_{start}_{end}.csv`

---

### 11강에서 **계산할 지표**

입력:

- ETF 일봉: `df_etf` (date, close, volume…)
- BM 일봉: `df_bm` (date, index close…)

1. **수익률 관련**

   - 일간 수익률: `daily_ret`
   - 기간 수익률:

     - `return_1M`, `return_3M`, `return_6M`, `return_1Y`, `return_3Y`, `return_5Y`

   - YTD: `return_YTD`
   - 설정일 이후: `return_since_inception` (설정일은 10강/etf_info에서 가져오거나 매개변수)

2. **리스크 관련**

   - 연환산 변동성: `vol_annual`
   - 전체 구간 MDD: `mdd`
   - `mdd_3Y`, `mdd_5Y`, `mdd_since_inception`
   - 드로다운 통계:

     - `dd_mdd`, `dd_avg_drawdown`, `dd_time_underwater_pct`, `dd_current_drawdown`

   - MDD 구간:

     - `dd_mdd_peak_date`, `dd_mdd_trough_date`, `dd_mdd_recovery_date`

       - `days_to_trough`, `days_to_recovery`

3. **위험조정수익률**

   - Sharpe, Sortino (`calc_sharpe_sortino`)

4. **시장 대비**

   - Beta, Alpha (`calc_beta_alpha`)
   - Tracking Error (`calc_tracking_error`)
   - 상대수익률:

     - `relative_return_1M`, … `relative_return_5Y`
     - `relative_return_series` (일별 시계열이지만 파일로 저장은 옵션)

5. **유동성 (보강 지표)**

   - `avg_volume_20d` (최근 20거래일 평균 거래량)

11강의 메시지:

> “7강에서 이론으로 설명한 수익률/리스크 지표(변동성, MDD, Sharpe, Beta, Alpha, TE 등)를
> ETF와 벤치마크 시계열 데이터로 실제로 계산해봤다.
> 이 값들이 의미하는 투자 해석은 이론 강의(7강, 8강)에서 이미 이야기한 내용과 연결된다.”

---

## 요약 – 9·10·11강 지표 역할 분담 한눈에

### 9강 – 원재료 정의 & 저장

- **무엇?**

  - `etf_info`, `holdings`, `etf_price` 3종류 로우 데이터

- **역할?**

  - “앞으로 쓸 데이터의 종류와 출처를 정의하고 안전하게 저장”

- **지표 수준?**

  - 지표 계산 X, 최소 검증만 O

---

### 10강 – 기본 & 포트폴리오 지표

- **무엇?**

  - 5강: AUM/규모/설정일/유동성 등 기본지표
  - 6강: Top10, 섹터·시총 분포, HHI, Effective N, 가중평균 PER/PBR, 회전율

- **입력?**

  - 9강에서 저장한 CSV + 종목/상품 메타 API 추가 조회

- **지표 수준?**

  - “포트폴리오 구성과 상품 특성을 정량화”
  - 리스크/성과 지표는 아직 X

---

### 11강 – 성과 & 리스크 지표

- **무엇?**

  - 7강/8강: 수익률, 변동성, MDD, Sharpe, Sortino, Beta, Alpha, TE, 상대수익률, 드로다운

- **입력?**

  - ETF 일봉 + 벤치마크 지수 일봉
  - 설정일(10강에서 가져오거나 별도 입력)

- **지표 수준?**

  - “성과/위험 & 시장 대비 성과까지 한 번에 계산”
