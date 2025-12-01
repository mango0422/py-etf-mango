import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

RAW_MST_DIR = PROJECT_ROOT / "mst_raw"
OUT_DIR = PROJECT_ROOT / "mst_fixed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(PROJECT_ROOT / ".env")

KIS_URL_BASE: Optional[str] = os.getenv("KIS_URL_BASE")
KIS_APP_KEY: Optional[str] = os.getenv("KIS_APP_KEY")
KIS_APP_SECRET: Optional[str] = os.getenv("KIS_APP_SECRET")
KIS_ACCESS_TOKEN_INIT: Optional[str] = os.getenv("KIS_ACCESS_TOKEN")
