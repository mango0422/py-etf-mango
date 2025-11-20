# src/config.py
from datetime import datetime, timedelta

# bt.get이 spy, agg 로 컬럼을 만들고 있으니, 아예 소문자로 통일
TICKERS = ["spy", "agg"]

TODAY = datetime.today().date()
START_DATE = (TODAY - timedelta(days=365 * 10)).strftime("%Y-%m-%d")

RISK_FREE_RATE = 0.025
