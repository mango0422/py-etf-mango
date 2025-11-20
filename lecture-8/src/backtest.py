import bt

def run_buy_and_hold(df, ticker: str, risk_free=0.025):
    s = bt.Strategy(
        "Buy&Hold",
        [
            bt.algos.RunOnce(),
            bt.algos.SelectAll(),
            bt.algos.WeighEqually(),
            bt.algos.Rebalance(),
        ],
    )
    test = bt.Backtest(s, df, name=f"[{ticker}] NAV Backtest")
    res = bt.run(test)
    res.set_riskfree_rate(risk_free)
    return res.__dict__["stats"]
