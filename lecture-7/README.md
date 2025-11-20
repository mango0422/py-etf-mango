# ETF 백테스팅 결과 분석

## 1. 개념 설명 (주식·ETF·위험지표)

### 1-1. ETF란?

- **ETF(Exchange Traded Fund)**

  - 주식처럼 거래소에 상장된 **인덱스/테마 추종 펀드**
  - 장중에 **주식처럼 실시간으로 매매** 가능
  - 여러 종목을 묶어놓았기 때문에 **분산투자 효과**를 제공

이번 실습에서 사용한 ETF:

- **SPY**

  - 미국 S&P 500 지수(대형주 500개)를 추종하는 **대표적인 주식형 ETF**
  - 미국·글로벌 주식시장 전체의 분위기를 대표한다고 보면 됨

- **AGG**

  - 미국 투자등급 채권들(국채, 회사채, MBS 등)로 구성된 **채권형 ETF**
  - 일반적으로 주식보다 변동성은 낮고, 주가가 흔들릴 때 **완충 역할(안전자산 성격)** 을 기대

---

### 1-2. 주식형 vs 채권형 ETF

- **주식형 ETF (SPY)**

  - 기대수익률 ↑
  - 변동성(위험) ↑
  - 경기 호황/위험자산 선호 시 성과가 좋음

- **채권형 ETF (AGG)**

  - 기대수익률 ↓ (주식 대비)
  - 변동성 ↓
  - 위기 상황에서 상대적으로 방어적

→ 그래서 흔히 **주식 : 채권 비율(예: 7:3, 6:4, 5:5)** 로 리스크 프로파일을 조절한다.

---

### 1-3. 일시투자 전략 (Lump-Sum Investing)

- **일시투자**:

  - 특정 시점에 **한 번에 자금을 투입**하는 전략
  - 예) 오늘 1,000만 원을 SPY:AGG = 7:3으로 맞춰서 전부 매수하고, 이후에는 추가 입·출금 없이 단순 보유

- 이번 백테스트 전략:

  - 전략 1: **SPY:AGG = 7:3**
  - 전략 2: **SPY:AGG = 3:7**
  - 둘 다 **시작 시점에 한 번만 리밸런싱**(RunOnce + Rebalance) 후 그대로 홀딩

---

### 1-4. Sharpe / Sortino / MDD 개념

1. **샤프 비율 (Sharpe Ratio)**

   - 정의:
     [
     \text{Sharpe} = \frac{R_p - R_f}{\sigma_p}
     ]

     - ( R_p ): 포트폴리오 수익률
     - ( R_f ): 무위험 수익률 (여기선 KOFR 기준 연 2.5%)
     - ( \sigma_p ): 포트폴리오 수익률의 표준편차(변동성)

   - 해석:

     - **“위험 한 단위(변동성 1)당 얼마나 초과 수익을 냈는가”**
     - 값이 클수록 **위험 대비 효율이 좋다**는 뜻

2. **소티노 비율 (Sortino Ratio)**

   - 샤프 비율과 비슷하지만,
     **전체 변동성 대신 “손실 구간(하방 변동성)”만 사용**하는 지표
   - “좋은 변동성(상승)은 벌점 주지 말고,
     **떨어질 때만 페널티를 주자**”라는 관점에서 설계된 지표
   - 값이 클수록 **하방 리스크 대비 수익 효율이 좋다.**

3. **최대 낙폭 (MDD, Maximum Drawdown)**

   - 백테스트 기간 동안 **고점 대비 얼마나 많이 떨어졌는지의 최대치**
   - 예: MDD = -0.26

     - “최고점에서부터 최악의 순간까지 **최대 26% 손실**을 경험했다”는 의미

   - 투자자의 체감 위험과 직결되는 지표라 실무에서도 매우 중요하게 본다.

---

## 2. 코드/라이브러리 사용법 정리

이번 프로젝트에서 사용한 핵심 라이브러리와 역할은 다음과 같다.

### 2-1. `bt.get` / `yfinance`: 가격 데이터 수집

```python
import bt

df = bt.get("spy, agg", start=START_DATE)
```

- `bt.get`은 내부적으로 **yfinance**를 사용해 **야후 파이낸스에서 종가 시계열 데이터를 가져옴**.
- `start` 파라미터로 **시작 날짜(여기서는 오늘 기준 10년 전)** 를 지정.
- 반환값은 **pandas DataFrame**:

  - index: 날짜(Date)
  - columns: 티커(`spy`, `agg`)
  - 값: 각 날짜의 종가

---

### 2-2. `pandas`: 시계열 전처리 & 정규화

```python
import pandas as pd

# NaN/0 제거
df = df.astype(float)
df = df.replace(0, np.nan).dropna(how="any")
df = df[(df > 0).all(axis=1)]

# 가격 정규화
def normalize_prices(df: pd.DataFrame) -> pd.DataFrame:
    return df / df.iloc[0]
```

- **전처리**

  - `dropna(how="any")`: 어느 종목이든 결측치가 있는 날짜 제거
  - `replace(0, np.nan)`: 0 가격 → 결측치로 취급
  - `(df > 0).all(axis=1)`: 모든 자산 가격이 0보다 큰 행만 남김

- **정규화(normalize)**

  - 첫 날 가격을 1로 맞춰서 **상대적 수익률을 시각적으로 비교**하기 쉽게 만듦
  - 예:

    - `spy_norm = df['spy'] / df['spy'].iloc[0]`

---

### 2-3. `numpy`: NaN 처리 등 수치 연산

```python
import numpy as np

df = df.replace(0, np.nan)
df = df.dropna(how="any")
```

- `np.nan`을 활용해 **이상치(0 가격)를 결측치로 치환**한 뒤 제거.
- 복잡한 수치 계산은 대부분 `pandas`/`bt`가 해주지만,
  **결측치 표현·필터링에 numpy가 기본 도구**로 쓰임.

---

### 2-4. `bt` 라이브러리: 전략 정의 + 백테스트 실행

#### 1) 전략 정의 (`bt.Strategy`)

```python
import bt

def make_strategy_7_3() -> bt.Strategy:
    return bt.Strategy(
        "7:3",
        [
            bt.algos.RunOnce(),
            bt.algos.SelectAll(),
            bt.algos.WeighSpecified(
                **{"spy": 0.7, "agg": 0.3}
            ),
            bt.algos.Rebalance(),
        ],
    )
```

- `bt.algos.RunOnce()`

  - 전략을 **시작 시점에 한 번만 실행**하도록 함 (일시투자)

- `bt.algos.SelectAll()`

  - 데이터에 포함된 모든 자산(`spy`, `agg`)을 선택

- `bt.algos.WeighSpecified(...)`

  - 티커별 **목표 비중** 지정
  - 여기서는 `"spy": 0.7, "agg": 0.3` / `"spy": 0.3, "agg": 0.7`

- `bt.algos.Rebalance()`

  - 현재 비중과 목표 비중이 다를 경우, **자산을 사고팔아 비중을 맞춤**

#### 2) 백테스트 실행 (`bt.Backtest`, `bt.run`)

```python
from .data_loader import load_price_data
from .strategies import make_strategy_7_3, make_strategy_3_7
from .config import RISK_FREE_RATE

df = load_price_data()
s1 = make_strategy_7_3()
s2 = make_strategy_3_7()

test1 = bt.Backtest(s1, df, name="7:3")
test2 = bt.Backtest(s2, df, name="3:7")

res = bt.run(test1, test2)
res.set_riskfree_rate(RISK_FREE_RATE)
```

- `bt.Backtest(strategy, data, name=...)`

  - 특정 전략 + 가격 데이터셋을 결합한 **백테스트 시나리오** 생성

- `bt.run(test1, test2)`

  - 여러 백테스트를 **한 번에 실행**하고 결과를 반환

- `set_riskfree_rate(0.025)`

  - **무위험 수익률(연 2.5%)**을 설정 → Sharpe/Sortino 계산에 사용

#### 3) 결과에서 지표 읽어오기

```python
strat_7_3 = res["7:3"]
strat_3_7 = res["3:7"]

sharpe_7_3 = strat_7_3.__dict__["daily_sharpe"]
mdd_7_3 = strat_7_3.__dict__["max_drawdown"]
```

- `res["7:3"]` / `res["3:7"]`
  → 각 전략의 결과 객체
- `daily_sharpe`, `daily_sortino`, `max_drawdown` 등의 속성을 통해
  **샤프/소티노/MDD 지표**를 읽어옴

---

### 2-5. `matplotlib`: ETF 데이터 시각화 (추가용 예시)

현재 프로젝트에 쉽게 붙일 수 있는 **시각화 예시**:

```python
import matplotlib.pyplot as plt
from .data_loader import load_price_data, normalize_prices

df = load_price_data()
df_norm = normalize_prices(df)

plt.figure(figsize=(10, 5))
plt.plot(df_norm.index, df_norm["spy"], label="SPY (주식형)")
plt.plot(df_norm.index, df_norm["agg"], label="AGG (채권형)")
plt.title("SPY vs AGG (정규화 가격 비교)")
plt.xlabel("Date")
plt.ylabel("Normalized Price (start = 1)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
```

- **ETF 데이터 시각화하기** 파트에서

  - SPY/AGG 가격을 정규화해 같은 차트에서 보여주면,
  - “10년 동안 주식형 vs 채권형 ETF의 성장/방어 패턴”을 직관적으로 설명 가능

---

## 3. 개념 + 코드로 결과 설명

이제 실제 실행 결과를 개념과 연결해서 정리해보자.

실행 결과:

```text
샤프 비율:
[7:3] 0.67
[3:7] 0.56

소티노 비율 (가능하면):
[7:3] 1.03
[3:7] 0.85

최대 낙폭 (MDD):
[7:3] -0.26
[3:7] -0.2
```

---

### 3-1. ETF 데이터 시각화하기

1. **정규화 가격 차트** (spy/agg)

   - 첫 날 가격을 1로 맞춘 뒤, SPY/AGG의 궤적을 한 차트에 표시
   - 관찰 포인트:

     - **SPY(주식형)**: 장기적으로 더 크게 우상향하지만,
       **중간중간 낙폭(변동성)이 크다.**
     - **AGG(채권형)**: 수익률은 낮지만,
       **충격 구간에서 낙폭이 상대적으로 작고 흔들림이 덜하다.**

2. 이 시각화를 통해:

   - **“주식형 ETF는 성장성, 채권형 ETF는 안정성을 담당한다”**는 기본 직관을 시각적으로 설명 가능
   - 이후 **7:3 / 3:7 포트폴리오**가 이 둘을 어떻게 섞는지 자연스럽게 이어갈 수 있음

---

### 3-2. ETF 백테스팅 결과 분석

#### (1) 샤프 비율 비교

- [7:3] **0.67**
- [3:7] **0.56**

→ 해석:

- 두 전략 모두 **위험 대비 초과수익이 양(+)** 이고,
  그중 **주식 비중이 더 높은 7:3 전략의 샤프 비율이 더 높음**.
- 즉,

  - **더 공격적인 7:3 전략이 장기적으로 “위험 1단위당 초과 수익” 측면에서 더 효율적**이었다.
  - 단순히 수익률만 높은 게 아니라, 변동성을 감안해도 괜찮은 성과.

#### (2) 소티노 비율 비교

- [7:3] **1.03**
- [3:7] **0.85**

→ 해석:

- 하락 구간(손실)의 변동성만 고려해도,
  **7:3 전략이 3:7 전략보다 효율적**이었다는 의미.
- 즉,

  - “떨어질 때를 기준으로 봐도, SPY 비중을 더 많이 가져간 포트폴리오가
    하방 위험 대비 보상을 더 잘 줬다”는 결과.

#### (3) 최대 낙폭(MDD) 비교

- [7:3] **-0.26** → 최대 약 **26% 손실**
- [3:7] **-0.20** → 최대 약 **20% 손실**

→ 해석:

- 예상대로, **주식 비중이 높은 7:3 전략이 더 깊은 낙폭을 경험**
- 3:7 전략은 **채권 비중이 높아 방어력이 좋지만**, 그만큼 성장성/초과 수익 측면에서는 약간 뒤처짐

---

### 3-3. 종합 해석

1. **수익·위험 관점**

   - 7:3 전략:

     - 더 높은 샤프(0.67), 더 높은 소티노(1.03), 더 큰 MDD(-26%)
     - → “장기적으로는 더 효율적인 성과, 대신 최대 손실 폭이 더 크다”

   - 3:7 전략:

     - 샤프/소티노가 약간 떨어지지만, MDD가 더 작음(-20%)
     - → “방어적인 포트폴리오, 심리적으로 버티기에는 조금 더 편한 구조”

2. **투자 성향에 따른 선택**

   - **공격적 성향 / 장기 투자자**

     - 7:3처럼 **주식 비중을 높인 전략**이 더 적합

   - **변동성이 부담되는 투자자**

     - 3:7처럼 **채권 비중을 더 높여 낙폭을 줄이는 전략**이 적합

3. **백테스트 결과를 통해 말할 수 있는 것**

   - “지난 10년간 데이터 기준으로 보면,
     SPY:AGG 7:3 전략이
     **위험 대비 수익(샤프/소티노) 측면에서는 우위**,
     **최대 낙폭 측면에서는 불리**했다.”
   - 이 차이는 ETF 구조(주식 vs 채권)의 특성에서 자연스럽게 설명 가능.
