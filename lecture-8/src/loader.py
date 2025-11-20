from .config import DATA_DIR, ETF_LIST_PATH
import pandas as pd
import json
import yfinance as yf

def load_etf_list():
    with ETF_LIST_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def ensure_nav_file(ticker: str):
    """
    NAV.csv 파일이 없으면 yfinance의 SHY 데이터를 기반으로 생성한다.
    (한국 ETF NAV 데이터가 무료 API로 없기 때문에 대체)
    """
    etf_dir = DATA_DIR / ticker
    nav_path = etf_dir / "NAV.csv"

    # 이미 파일 있으면 생성할 필요 없음
    if nav_path.exists():
        return nav_path
    print(f"[INFO] NAV.csv 없음 → 자동 생성 시작 ({ticker})")
    etf_dir.mkdir(exist_ok=True)

    # SHY 데이터 다운로드
    df = yf.download("SHY", start="2019-07-24")["Adj Close"]

    # pandas Series → DataFrame 변환
    df = df.to_frame(name=ticker)

    # 저장
    df.to_csv(nav_path, index_label="date")
    print(f"[INFO] NAV.csv 자동 생성 완료 → {nav_path}")

    return nav_path



def load_nav(ticker: str) -> pd.DataFrame:
    """
    NAV.csv 로드. 파일이 없으면 자동 생성.
    """
    nav_path = ensure_nav_file(ticker)
    df = pd.read_csv(nav_path, index_col=0, parse_dates=True)

    # 컬럼 이름이 1개라면 ticker로 강제 세팅
    if df.shape[1] == 1:
        df.columns = [ticker]

    # 0 / NaN 제거
    df = df.replace(0, pd.NA).dropna(how="any")

    return df
