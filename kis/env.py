from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import requests
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
KIS_ACCESS_TOKEN: Optional[str] = os.getenv("KIS_ACCESS_TOKEN")

def to_float(value) -> Optional[float]:
    try:
        return float(str(value).replace(",", "").strip())
    except Exception:
        return None



def get_api_headers(tr_id: str) -> dict[str, str]:
    from .env import KIS_ACCESS_TOKEN  # 전역 참조

    auth = f"Bearer {KIS_ACCESS_TOKEN}" if KIS_ACCESS_TOKEN else ""
    return {
        "content-type": "application/json; charset=utf-8",
        "authorization": auth,
        "appkey": KIS_APP_KEY or "",
        "appsecret": KIS_APP_SECRET or "",
        "tr_id": tr_id,
        "custtype": "P",
    }


def refresh_access_token() -> Optional[str]:
    global KIS_ACCESS_TOKEN

    if not KIS_URL_BASE:
        raise RuntimeError("KIS_URL_BASE 설정이 없습니다.")

    token_url = f"{KIS_URL_BASE}/oauth2/tokenP"

    headers = {
        "content-type": "application/json"
    }

    body = {
        "grant_type": "client_credentials",
        "appkey": KIS_APP_KEY,
        "appsecret": KIS_APP_SECRET
    }

    try:
        response = requests.post(token_url, headers=headers, json=body, timeout=5)
        data = response.json()

        if response.status_code == 200 and data.get("access_token"):
            new_token = data["access_token"]
            expires_in = data.get("expires_in", 86400)
            expired_at = data.get("access_token_token_expired", "")

            print(f"✅ 토큰 재발급 성공")
            if expired_at:
                print(f"   만료 시각: {expired_at}")
            print(f"   유효 시간: {expires_in}초 ({expires_in/3600:.1f}시간)")

            KIS_ACCESS_TOKEN = new_token

            try:
                env_path = PROJECT_ROOT / ".env"
                if env_path.exists():
                    lines = env_path.read_text(encoding="utf-8").split("\n")
                    new_lines = []
                    token_updated = False

                    for line in lines:
                        if line.startswith("KIS_ACCESS_TOKEN="):
                            new_lines.append(f"KIS_ACCESS_TOKEN={new_token}")
                            token_updated = True
                        else:
                            new_lines.append(line)

                    if not token_updated:
                        new_lines.append(f"KIS_ACCESS_TOKEN={new_token}")

                    env_path.write_text("\n".join(new_lines), encoding="utf-8")
                    print("   📝 .env 파일 업데이트 완료")
            except Exception as e:
                print(f"   ⚠️ .env 파일 업데이트 실패 (무시 가능): {e}")

            return new_token
        else:
            print(f"❌ 토큰 발급 실패: {data}")
            return None

    except Exception as e:
        print(f"❌ 토큰 발급 중 오류: {e}")
        return None


def validate_and_refresh_token() -> Optional[str]:
    global KIS_ACCESS_TOKEN

    if not KIS_URL_BASE:
        raise RuntimeError("KIS_URL_BASE 설정이 없습니다.")


    if not KIS_ACCESS_TOKEN:
        print("⚠️ 메모리에 토큰이 없어 재발급을 시도합니다.")
        return refresh_access_token()

    test_url = f"{KIS_URL_BASE}/uapi/etfetn/v1/quotations/inquire-price"
    test_params = {"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": "069500"}
    test_headers = get_api_headers("FHPST02400000")

    try:
        response = requests.get(test_url, headers=test_headers, params=test_params, timeout=5)
        data = response.json()

        if data.get("rt_cd") in ["EGW00123", "EGW00121"]:
            print("⚠️ 토큰 만료 감지, 재발급 시도...")
            return refresh_access_token()
        elif data.get("rt_cd") == "0":
            print("✅ 기존 토큰 유효함")
            return KIS_ACCESS_TOKEN
        else:
            print(f"⚠️ API 응답 오류 ({data.get('rt_cd')}), 토큰 재발급 시도...")
            return refresh_access_token()

    except requests.exceptions.Timeout:
        print("⚠️ API 응답 시간 초과 (네트워크 이슈일 수 있음)")
        return KIS_ACCESS_TOKEN
    except Exception as e:
        print(f"⚠️ 토큰 검증 중 오류: {e}")
        return KIS_ACCESS_TOKEN


def ensure_kis_token() -> Optional[str]:
    token = validate_and_refresh_token()
    if not token:
        print("❌ 토큰 발급/갱신 실패 - KIS 환경변수(.env) 설정을 확인하세요.")
    return token
