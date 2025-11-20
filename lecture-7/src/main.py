# src/main.py
from .run_backtest import run_backtests

print("[DEBUG] main.py imported")

def main():
    print("[DEBUG] main() started")
    res = run_backtests()

    # 결과 객체는 각 백테스트 이름으로 접근 가능
    strat_7_3 = res["7:3"]
    strat_3_7 = res["3:7"]

    # bt의 통계 값은 stats / display / plot 등으로 볼 수 있는데,
    # 여기서는 문제 조건대로 __dict__에서 직접 꺼내는 형태를 그대로 사용.
    # (버전에 따라 속성 이름이 다를 수 있으므로, 에러 나면 print(dir(strat_7_3))로 확인)

    print("샤프 비율:")
    print(f"[7:3] {round(strat_7_3.__dict__.get('daily_sharpe', float('nan')), 2)}")
    print(f"[3:7] {round(strat_3_7.__dict__.get('daily_sharpe', float('nan')), 2)}")

    # 소티노 비율은 버전에 따라 'daily_sortino' 또는 비슷한 이름일 수 있음
    print("\n소티노 비율 (가능하면):")
    sortino_7_3 = strat_7_3.__dict__.get("daily_sortino")
    sortino_3_7 = strat_3_7.__dict__.get("daily_sortino")
    print(f"[7:3] {round(sortino_7_3, 2) if sortino_7_3 is not None else 'N/A'}")
    print(f"[3:7] {round(sortino_3_7, 2) if sortino_3_7 is not None else 'N/A'}")

    print("\n최대 낙폭 (MDD):")
    print(f"[7:3] {round(strat_7_3.__dict__.get('max_drawdown', float('nan')), 2)}")
    print(f"[3:7] {round(strat_3_7.__dict__.get('max_drawdown', float('nan')), 2)}")

    # 필요하면 전체 stats 테이블도 같이 확인 가능
    # print(res.display())


if __name__ == "__main__":
    main()
