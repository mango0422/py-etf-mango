from typing import Optional
import requests
from .config import PROJECT_ROOT, KIS_URL_BASE, KIS_APP_KEY, KIS_APP_SECRET, KIS_ACCESS_TOKEN_INIT

_KIS_ACCESS_TOKEN: Optional[str] = KIS_ACCESS_TOKEN_INIT


def get_api_headers(tr_id: str) -> dict[str, str]:
    auth = f"Bearer {_KIS_ACCESS_TOKEN}" if _KIS_ACCESS_TOKEN else ""
    return {
        "content-type": "application/json; charset=utf-8",
        "authorization": auth,
        "appkey": KIS_APP_KEY or "",
        "appsecret": KIS_APP_SECRET or "",
        "tr_id": tr_id,
        "custtype": "P",
    }


def refresh_access_token() -> Optional[str]:
    global _KIS_ACCESS_TOKEN

    if not KIS_URL_BASE or not KIS_APP_KEY or not KIS_APP_SECRET:
        print("❌ KIS 환경변수(KIS_URL_BASE / KIS_APP_KEY / KIS_APP_SECRET)를 확인하세요.")
        return None

    token_url = f"{KIS_URL_BASE}/oauth2/tokenP"
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": KIS_APP_KEY,
        "appsecret": KIS_APP_SECRET,
    }

    try:
        res = requests.post(token_url, headers=headers, json=body, timeout=5)
        data = res.json()
    except Exception as e:
        print(f"❌ 토큰 발급 요청 실패: {e}")
        return None

    access_token = data.get("access_token")
    if not access_token:
        print(f"❌ 토큰 발급 실패: {data}")
        return None

    _KIS_ACCESS_TOKEN = access_token
    print("✅ 토큰 발급 성공")

    # .env 동기화 (선택 기능)
    try:
        env_path = PROJECT_ROOT / ".env"
        lines: list[str] = []
        if env_path.exists():
            lines = env_path.read_text(encoding="utf-8").splitlines()

        new_lines = []
        token_updated = False
        for line in lines:
            if line.startswith("KIS_ACCESS_TOKEN="):
                new_lines.append(f"KIS_ACCESS_TOKEN={access_token}")
                token_updated = True
            else:
                new_lines.append(line)

        if not token_updated:
            new_lines.append(f"KIS_ACCESS_TOKEN={access_token}")

        env_path.write_text("\n".join(new_lines), encoding="utf-8")
        print("   📝 .env 파일 업데이트 완료")
    except Exception as e:
        print(f"   ⚠️ .env 업데이트 실패(무시 가능): {e}")

    return access_token

def validate_and_refresh_token() -> Optional[str]:
    global _KIS_ACCESS_TOKEN

    if not KIS_URL_BASE:
        print("❌ KIS_URL_BASE가 설정되지 않았습니다.")
        return None

    # 현재 토큰이 있으면 간단히 테스트
    if _KIS_ACCESS_TOKEN:
        test_url = f"{KIS_URL_BASE}/uapi/etfetn/v1/quotations/inquire-price"
        test_params = {"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": "069500"}

        test_headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {_KIS_ACCESS_TOKEN}",
            "appkey": KIS_APP_KEY or "",
            "appsecret": KIS_APP_SECRET or "",
            "tr_id": "FHPST02400000",
            "custtype": "P",
        }

        try:
            res = requests.get(test_url, headers=test_headers, params=test_params, timeout=3)
            data = res.json()
            # 응답 코드가 0이면 토큰은 유효한 것으로 간주
            if data.get("rt_cd") == "0":
                return _KIS_ACCESS_TOKEN
        except Exception:
            # 네트워크 오류 등은 그냥 새 토큰 발급으로 넘어간다
            pass

    # 여기까지 왔으면 토큰이 없거나/만료됨 → 새 토큰 발급
    return refresh_access_token()


def ensure_kis_token() -> Optional[str]:
    token = validate_and_refresh_token()
    if not token:
        print("❌ 토큰 발급/갱신 실패 - KIS 환경변수(.env) 설정을 확인하세요.")
    return token
