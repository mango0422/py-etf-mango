# Step 0. MST 마스터 파일 구조 이해

ETF 분석에 들어가기 전에,  
우리가 실제로 사용할 **KRX MST 마스터 파일들**의 관계를 먼저 정리해 두겠습니다.

이번 강의에서 다루는 파일은 딱 네 가지입니다.

- `kospi_code.mst` → `kospi_code.(csv|parquet)`
- `kosdaq_code.mst` → `kosdaq_code.(csv|parquet)`
- `konex_code.mst` → `konex_code.(csv|parquet)`
- 이 세 개를 합친 `equity_master.(csv|parquet)`

추가로 KRX 쪽에서 더 많은 MST 파일을 제공하지만  
**이번 ETF 데이터 파이프라인에서는 이 네 가지만 사용**합니다.

---

## 0-1. 파일들 간 관계 요약

- **`kospi_code`**
  - 유가증권시장(KOSPI) 상장 종목 마스터
- **`kosdaq_code`**
  - 코스닥(KOSDAQ) 상장 종목 마스터
- **`konex_code`**
  - 코넥스(KONEX) 상장 종목 마스터
- **`equity_master`**
  - 위 세 개(`kospi_code`, `kosdaq_code`, `konex_code`)를
    **단순 concat**해서 만든 통합 주식 마스터

즉:

> `equity_master = kospi_code ∪ kosdaq_code ∪ konex_code`  
> (열 구조는 동일, 행만 모두 합쳐놓은 테이블)

ETF 구성종목/상위보유 종목/섹터 ETF 분석에서  
“이 코드가 어떤 종목 이름인지”를 빠르게 알고 싶을 때  
**가장 먼저 참조하는 기본 마스터**가 바로 `equity_master`입니다.

---

## 1. `kospi_code.csv` / `kospi_code.parquet`

### kospi_code 역할

- **유가증권시장(KOSPI)** 상장 종목(주식, ETF, ETN 포함)의 코드 마스터.
- 한 줄에 **KOSPI 상장 종목 1개**가 대응됩니다.

### kospi_code 컬럼

- `short_code`

  - KRX 단축코드 (9바이트)
  - 예: `A005930`, `A069500` 등
  - 실무에서 “티커”처럼 자주 쓰는 코드

- `std_code`

  - 표준코드 (12자리)
  - ISIN 또는 KRX 표준코드 계열
  - 다른 시스템/브로커와 연동할 때 기준이 되는 식별자

- `name`
  - 종목 한글명 (40바이트)
  - 예: `삼성전자`, `KODEX 200` 등

> 요약: “**KOSPI 종목코드 → 한글 이름**” 매핑 테이블.

---

## 2. `kosdaq_code.csv` / `kosdaq_code.parquet`

### kosdaq_code 역할

- **코스닥(KOSDAQ)** 상장 종목 마스터.
- 한 줄에 KOSDAQ 상장 종목 1개.

### kosdaq_code 컬럼

- `short_code`
- `std_code`
- `name`

구조는 `kospi_code`와 완전히 동일합니다.  
**차이점은 시장만 KOSDAQ**이라는 점뿐입니다.

---

## 3. `konex_code.csv` / `konex_code.parquet`

### konex 역할

- **코넥스(KONEX)** 시장 상장 종목 마스터.

### konex 컬럼

- `short_code`
- `std_code`
- `name`

역시 `kospi_code`, `kosdaq_code`와 구조가 동일하고  
시장만 KONEX인 버전이라고 보면 됩니다.

---

## 4. `equity_master.csv` / `equity_master.parquet`

### equity_master 역할

- **KOSPI + KOSDAQ + KONEX**를 한 번에 합친 **통합 주식 마스터**.
- 강의 코드에서는 대략 아래와 같이 생성합니다.

  ```python
  dfs = []
  for fname in ("kospi_code.mst", "kosdaq_code.mst", "konex_code.mst"):
      # MST 파싱 → (short_code, std_code, name)만 추출
      df = parse_fixed_width_lines(..., EQUITY_SCHEMA)
      dfs.append(df)

  merged = pd.concat(dfs, ignore_index=True)
  merged.to_csv("mst_fixed/equity_master.csv", ...)
  ```

- 이후에는 매번 개별 MST를 다시 읽는 대신
  **`equity_master`만 로딩해서** 코드/이름을 조회하게 됩니다.

### equity_master 컬럼

- `short_code`
- `std_code`
- `name`

### 사용 패턴

- 구성종목 코드 리스트 → `equity_master`와 join해서 한글 이름 붙이기
- “이 ETF 구성에 포함된 주식들 이름”을 빠르게 보고 싶을 때
- 특정 단축코드/표준코드가 KRX 어디에 상장된 종목인지 확인할 때

> 참고:
>
> - `equity_master`에는 `market`(KOSPI/KOSDAQ/KONEX 구분) 컬럼이 기본적으로 없습니다.
> - 시장 구분이 필요하면:
>
>   - 생성 단계에서 `market` 컬럼을 추가해서 저장하거나,
>   - 나중에 `kospi_code`/`kosdaq_code`/`konex_code`와 다시 조인해서 시장 정보를 붙이면 됩니다.

---

## 5. CSV vs Parquet (공통)

모든 마스터 파일에 대해 두 가지 버전을 함께 둘 수 있습니다.

- `xxx.csv`

  - 사람이 바로 열어볼 수 있는 텍스트 포맷
  - 엑셀/노트북에서 구조 확인용으로 편리

- `xxx.parquet`

  - **컬럼 지향 바이너리 포맷**
  - pandas, PyArrow 등에서 읽고 쓰는 속도가 빠르고, 메모리 효율이 좋음
  - 실제 분석/백테스트 코드에서는 parquet를 우선 사용하는 것이 일반적

이번 강의에서는:

- **원본 MST → CSV로 1차 저장**
- 필요하다면 이후에 `equity_master.parquet`로도 변환해서
  고속 로딩에 활용하는 패턴을 사용할 수 있습니다.
