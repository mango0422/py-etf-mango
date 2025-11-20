# 📘 **LLM으로 ETF 이해하기 — 개념·코드·구현 정리**

이 프로젝트는 **국내 ETF 데이터(NAV)와 기본정보**,
그리고 **OpenAI LLM + 웹 검색 도구**를 활용하여
“ETF 분석 보고서를 자동으로 생성하는 시스템”을 만드는 실습이다.

핵심은 다음 세 가지다.

1. **ETF 개념을 이해하고**
2. **Python 도구(bt, pandas, yfinance 등)로 금융 데이터를 처리하고**
3. **LLM(OpenAI API)에게 금융 데이터를 입력하여 보고서를 자동 생성**

---

## 1️⃣ 금융 개념 설명 — ETF·채권·NAV·백테스트 등

### ■ ETF란?

ETF(Exchange Traded Fund)는 **주식처럼 거래되는 펀드**다.
여러 자산(주식, 채권, 원자재, 통화 등)을 묶어 지수를 추종한다.

ETF의 장점:

- **실시간 매수·매도 가능**
- **낮은 보수**
- **분산 투자 효과**
- **높은 투명성** (매일 구성 공개)

### ■ 국내 ETF의 특징

국내 ETF는 한국거래소(KRX)에 상장되며 다음 정보를 제공한다:

- 종목명, 표준코드(ISIN)
- 상장일
- 운용사
- 추종지수/복제방식(실물/합성/액티브)
- 총보수
- 과세유형
- 구성종목 / 보유채권 정보 (다만 무료 API로 직접 조회는 제한)

이 프로젝트는 국내 ETF 중 **329750(미래에셋 TIGER 미국달러단기채권액티브)**를 다룬다.

---

### ■ 채권형 ETF란?

채권형 ETF는 채권(국채/회사채)을 묶은 상품이다.

특징:

- **가격 변동성 ↓**
- **이자 수익(쿠폰) ↑**
- **금리와 반대 방향으로 움직임**
- **환율 리스크 존재** (해외 채권일 경우)

329750 ETF는:

- 미국 단기 국채(T-Bill) + 회사채 + 금융채
- **만기 1개월 ~ 1년**
- 금리 민감도 매우 낮음 (단기채 특성)

---

### ■ NAV란? (순자산가치)

ETF 1좌(주식 1주와 동일)의 실질적 가치를 의미한다.

```text
NAV = (보유 자산 전체 가치 - 부채) / 발행증권수
```

NAV는 펀드의 **내재 가치**, 시장 가격은 ETF의 **거래 가격**
보통 크게 차이나지 않지만, 장 중에는 약간의 괴리가 발생할 수 있다.

이 프로젝트는 NAV.csv를 읽어 백테스트에 사용한다.

---

### ■ 백테스트란?

과거 데이터를 기준으로 특정 전략으로 투자했을 때 성과가 어떠했는지 시뮬레이션해보는 것.

본 프로젝트의 전략은 단순함:

> **Buy & Hold 전략**
> (전체 기간 동안 100% 보유)

성과 지표:

- 총수익률 (Total Return)
- CAGR (연평균복리수익률)
- 최대낙폭 (MDD)
- 샤프지수 (Sharpe Ratio)
- 변동성

---

## 2️⃣ 코드 사용 기술 — bt, pandas, numpy, yfinance 활용법

아래는 프로젝트에서 실제로 사용한 도구와 그 역할 설명이다.

---

### ■ pandas (데이터 분석)

CSV 읽기/전처리:

```python
df = pd.read_csv(nav_path, index_col=0, parse_dates=True)
df = df.replace(0, pd.NA).dropna(how="any")
```

pandas는 금융 시계열 분석의 핵심이다:

- 날짜 파싱 (`parse_dates=True`)
- 결측치 처리
- 슬라이싱
- 연산(정규화, 수익률 변환)

---

### ■ numpy (수치 연산)

numpy는 내부적으로 pandas와 bt 라이브러리가 사용한다.

프로젝트에서는 직접 numpy 연산을 최소한으로 사용했지만,
수익률 계산, 배열 변환, 통계 분석에서 핵심적으로 관여한다.

---

### ■ bt 라이브러리 (백테스트 프레임워크)

전략 정의:

```python
s = bt.Strategy(
    "Buy&Hold",
    [
        bt.algos.RunOnce(),
        bt.algos.SelectAll(),
        bt.algos.WeighEqually(),
        bt.algos.Rebalance(),
    ],
)
```

핵심 알고:

- `RunOnce()` : 시작 시점에 한 번 실행
- `SelectAll()` : 모든 자산 선택
- `WeighEqually()` : 100% 비중 부여
- `Rebalance()` : 비중 적용

실행:

```python
test = bt.Backtest(s, df, name="NAV Backtest")
res = bt.run(test)
res.set_riskfree_rate(0.025)
```

통계 추출:

```python
stats = res.__dict__["stats"]
```

`bt`의 장점:

- 단순한 구성으로 전략 작성 가능
- CAGR, MDD, 샤프지수를 자동 계산
- pandas 기반의 유연한 시계열 처리

---

### ■ yfinance (SHY 데이터 다운로드)

NAV 파일이 없을 경우 자동으로 SHY 데이터를 기반으로 생성:

```python
df = yf.download("SHY", start="2019-07-24")["Adj Close"]
df = df.to_frame(name=ticker)
df.to_csv(nav_path, index_label="date")
```

yfinance 장점:

- 무료 API
- 미국 ETF/주식 데이터에 강함
- pandas로 바로 연동 가능

---

### ■ dotenv + OpenAI API

`.env` 파일에서 API 키 로드:

```python
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
```

OpenAI LLM 클라이언트 생성:

```python
openai_client = OpenAI(api_key=API_KEY)
```

---

### ■ 웹 검색 tool 사용

OpenAI Responses API에서:

```python
tools=[
    {
        "type": "web_search_preview",
        "user_location": {"type": "approximate", "country": "KR"},
    }
]
```

효과:

- 최신 뉴스/시장 정보 자동 검색
- ETF 관련 뉴스 요약
- 최신 시세, 보도자료, 금리 뉴스 반영

이게 이 프로젝트의 핵심 차별점이다.

---

## 3️⃣ 전체 구현 설명 — 데이터 → 백테스트 → LLM → 보고서 자동 생성

이제 프로젝트 전체 흐름을 개념 + 코드를 연결해서 설명해보자.

---

### ■ (1) ETF 기본 정보 로드

```python
etf_list = load_etf_list()
etf_info = etf_list[ticker]
```

→ 국내 ETF JSON에서 종목 정보 로드
→ 운용사, 상장일, 기초지수 등은 보고서의 기본 설명에 사용

---

### ■ (2) NAV.csv 로드 (없으면 SHY로 자동 생성)

```python
df = load_nav(ticker)
```

처리 흐름:

1. NAV.csv 존재 여부 확인
2. 없다 → `yfinance`에서 SHY 데이터를 받아 NAV.csv 생성
3. 있다 → 그대로 로드

→ 백테스트 시계열 데이터 확보 완료

---

### ■ (3) 백테스트 수행

```python
bt_stats = run_buy_and_hold(df, ticker)
```

- Buy & Hold 전략 정의
- bt 백테스트 실행
- 일간 샤프, 변동성, CAGR 등 통계 출력

이 분석 결과는 LLM에게 그대로 전달된다.

---

### ■ (4) LLM 프롬프트 구성

```python
user_prompt = build_user_prompt(etf_info, ticker, name, bt_stats)
```

LLM에게 전달되는 정보:

- ETF 기본 정보(JSON)
- 백테스트 결과(markdown)
- 오늘 날짜
- 종목 코드 + 이름

이 정보는 보고서를 작성하기 위한 컨텍스트가 된다.

---

### ■ (5) OpenAI LLM + 웹 검색 → 보고서 생성

```python
response = openai_client.responses.create(...)
```

LLM은 다음을 수행:

1. ETF 기본정보 기반 정적 분석
2. NAV 기반 백테스트 결과 해석
3. 웹 검색으로:

   - ETF 뉴스
   - 구성종목 정보
   - 금리·환율 시황
   - AUM 업데이트

4. Markdown 기반 보고서 작성

이게 바로 **데이터 기반 LLM 분석의 핵심 메커니즘**이다.

---

### ■ (6) 보고서 저장

```python
out = REPORT_DIR / f"{ticker}.md"
out.write_text(response.output_text)
```
