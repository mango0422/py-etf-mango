import os
import requests
import pandas as pd

KIS_BASE_URL = os.getenv(
    "KIS_BASE_URL",
    "https://openapi.koreainvestment.com:9443"
)

class KISClient:
    """
    KIS REST API 공통 클라이언트.
    - 토큰/키와 base url 관리
    - 공통 헤더 생성
    - 응답 에러 처리
    - JSON → dict 반환
    """
    def __init__(self, appkey: str, appsecret: str, access_token: str, custtype: str = "P"):
        self.appkey = appkey
        self.appsecret = appsecret
        self.access_token = access_token
        self.custtype = custtype

    def _build_headers(self, tr_id: str, **extra_headers) -> dict:
        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self.access_token}",
            "appkey": self.appkey,
            "appsecret": self.appsecret,
            "tr_id": tr_id,
            "custtype": self.custtype,
        }
        headers.update(extra_headers)
        return headers

    def _request(self, method: str, path: str, tr_id: str, *, params=None) -> dict:
        """
        KIS API 공통 호출 메서드.
        - method: "GET"/"POST"
        - path: /uapi/.... 형태 (앞에 /는 붙여도 되고 안 붙여도 됨)
        - tr_id: 각 API별 거래 ID (예: FHKST03010100 등)
        - params: query string 혹은 body에 들어갈 dict

        반환:
            응답 JSON(dict)
        """
        url = f"{KIS_BASE_URL}/{path.lstrip('/')}"
        headers = self._build_headers(tr_id=tr_id)

        resp = requests.request(method, url, headers=headers, params=params)
        # HTTP 레벨 에러 체크
        resp.raise_for_status()

        data = resp.json()

        # KIS 응답 코드 체크 (rt_cd / msg_cd / msg1)
        # 대부분의 KIS API에서 rt_cd == "0" 이면 성공이라고 문서에 나와 있음.
        rt_cd = data.get("rt_cd")
        if rt_cd not in (None, "0", "0000"):
            msg_cd = data.get("msg_cd")
            msg1 = data.get("msg1")
            raise RuntimeError(f"KIS API Error (rt_cd={rt_cd}, msg_cd={msg_cd}): {msg1}")

        return data