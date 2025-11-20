# src/run_backtest.py
import bt
from .config import RISK_FREE_RATE
from .data_loader import load_price_data
from .strategies import make_strategy_7_3, make_strategy_3_7


def run_backtests():
    # 1) 데이터 로드
    df = load_price_data()

    # 2) 전략 정의
    s1 = make_strategy_7_3()
    s2 = make_strategy_3_7()

    # 3) 백테스트 객체 생성
    test1 = bt.Backtest(s1, df, name="7:3")
    test2 = bt.Backtest(s2, df, name="3:7")

    # 4) 실행
    res = bt.run(test1, test2)

    # 5) 무위험 수익률 설정 (연간 2.5%)
    res.set_riskfree_rate(RISK_FREE_RATE)

    return res
