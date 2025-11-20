# src/config.py
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

# 프로젝트 루트 경로
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
ETF_LIST_PATH = DATA_DIR / "filtered_etf_list.json"
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=API_KEY)
