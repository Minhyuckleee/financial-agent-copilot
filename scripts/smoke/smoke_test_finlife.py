"""금감원 「금융상품한눈에」 정기예금 API 키 최소 호출 검증. 실행: python scripts/smoke_test_finlife.py

스펙 확인 완료(https://finlife.fss.or.kr/finlife/api/fdrmDpstApi/list.do?menuNo=700052):
GET http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json
  ?auth={인증키}&topFinGrpNo=020000(은행)&pageNo=1
"""
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = "/depositProductsSearch.json"
TOP_FIN_GRP_NO = "020000"  # 은행권


def main() -> None:
    key = os.environ["FINLIFE_API_KEY"]
    base = os.environ.get("FINLIFE_BASE_URL", "http://finlife.fss.or.kr/finlifeapi")
    url = f"{base}{ENDPOINT}"

    resp = httpx.get(
        url,
        params={"auth": key, "topFinGrpNo": TOP_FIN_GRP_NO, "pageNo": 1},
        timeout=10,
        follow_redirects=True,
    )
    resp.raise_for_status()
    result = resp.json()["result"]

    if result["err_cd"] != "000":
        raise RuntimeError(f"금감원 API 에러: {result['err_cd']} {result['err_msg']}")

    products = result.get("baseList") or result.get("products") or []
    print(
        f"[OK] 총 {result['total_count']}건, {len(products)}건 수신, "
        f"첫 상품: {products[0].get('fin_prdt_nm') if products else '없음'}"
    )


if __name__ == "__main__":
    main()
