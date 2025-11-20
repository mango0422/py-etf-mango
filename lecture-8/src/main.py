from .loader import load_etf_list, load_nav
from .backtest import run_buy_and_hold
from .prompt import DEV_PROMPT, build_user_prompt
from .report import generate_report


def main():
    ticker = "329750"

    etf_list = load_etf_list()
    etf_info = etf_list[ticker]
    name = etf_info["한글종목약명"]

    df = load_nav(ticker)
    bt_stats = run_buy_and_hold(df, ticker)

    user_prompt = build_user_prompt(etf_info, ticker, name, bt_stats)

    out_path = generate_report(DEV_PROMPT, user_prompt, ticker)
    print(f"보고서 생성 완료: {out_path}")


if __name__ == "__main__":
    main()
