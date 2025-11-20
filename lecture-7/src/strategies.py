# src/strategies.py
import bt


def make_strategy_7_3() -> bt.Strategy:
    return bt.Strategy(
        "7:3",
        [
            bt.algos.RunOnce(),
            bt.algos.SelectAll(),
            bt.algos.WeighSpecified(
                **{
                    "spy": 0.7,
                    "agg": 0.3,
                }
            ),
            bt.algos.Rebalance(),
        ],
    )


def make_strategy_3_7() -> bt.Strategy:
    return bt.Strategy(
        "3:7",
        [
            bt.algos.RunOnce(),
            bt.algos.SelectAll(),
            bt.algos.WeighSpecified(
                **{
                    "spy": 0.3,
                    "agg": 0.7,
                }
            ),
            bt.algos.Rebalance(),
        ],
    )
