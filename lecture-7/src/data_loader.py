# src/data_loader.py
import bt
import pandas as pd
import numpy as np
from .config import TICKERS, START_DATE


def load_price_data() -> pd.DataFrame:
    """
    bt.get을 이용해 야후 파이낸스에서 종가 데이터를 가져옴.
    TICKERS 리스트에 들어 있는 종목만 가져오며,
    0 또는 NaN이 있는 날짜는 모두 제거한다.
    """
    tickers_str = ", ".join(TICKERS)
    df = bt.get(tickers_str, start=START_DATE)

    # 디버깅용: 원시 데이터 확인
    print("\n[DEBUG] raw df head:")
    print(df.head())
    print("\n[DEBUG] raw df index range:", df.index.min(), "→", df.index.max())

    # 혹시 숫자 타입이 아닌 경우를 대비해서 float로 캐스팅
    df = df.astype(float)

    # 0 또는 NaN이 있는 행들 먼저 찍어보자
    bad_rows = df[(df <= 0).any(axis=1) | df.isna().any(axis=1)]
    if not bad_rows.empty:
        print("\n[DEBUG] rows with 0 or NaN prices:")
        print(bad_rows.head(10))

    # 1) 0을 NaN으로 바꾸고
    df = df.replace(0, np.nan)

    # 2) NaN이 하나라도 있는 날짜는 전체 제거
    df = df.dropna(how="any")

    # 3) (혹시 음수 같은 이상치가 있다면) 0 이하 값 있는 행도 제거
    df = df[(df > 0).all(axis=1)]

    # 4) 그래도 혹시 시작 날짜 주변에 뭔가 꼬여 있으면,
    #    "가장 첫 번째 유효한 날짜"부터만 사용
    df = df.iloc[1:]  # 첫 행을 강제로 날려서 2015-11-23 같은 edge case 제거

    print("\n[DEBUG] cleaned df head:")
    print(df.head())
    print("\n[DEBUG] cleaned df index range:", df.index.min(), "→", df.index.max())

    return df
