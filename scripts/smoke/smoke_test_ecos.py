"""한국은행 ECOS API 키 최소 호출 검증. 실행: python scripts/smoke_test_ecos.py

ECOS는 통계표코드/주기/기간을 URL 경로에 나열하는 고정 포맷:
  https://ecos.bok.or.kr/api/StatisticSearch/{키}/json/kr/1/5/{통계표코드}/{주기}/{시작}/{종료}/{항목코드}

통계표코드 731Y003(3.1.1.3. 원화의 대미달러, 원화의 대위안/대엔 환율)/항목코드 0000003(원/달러 종가 15:30)은
StatisticTableList·StatisticItemList API로 직접 조회해 확정함(포털 통계코드검색 UI가 렌더링 안 돼서 API로 우회 검증).
"""
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

STAT_CODE = "731Y003"  # 원화의 대미달러 환율
ITEM_CODE = "0000003"  # 원/달러(종가 15:30)
CYCLE = "D"  # 일별
START, END = "20260801", "20260806"


def main() -> None:
    key = os.environ["ECOS_API_KEY"]
    base = os.environ.get("ECOS_BASE_URL", "https://ecos.bok.or.kr/api")
    url = f"{base}/StatisticSearch/{key}/json/kr/1/5/{STAT_CODE}/{CYCLE}/{START}/{END}/{ITEM_CODE}"

    resp = httpx.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if "RESULT" in data:
        raise RuntimeError(f"ECOS 에러 응답: {data['RESULT']}")

    rows = data.get("StatisticSearch", {}).get("row", [])
    print(f"[OK] {len(rows)}건 수신, 첫 행: {rows[0] if rows else '없음'}")


if __name__ == "__main__":
    main()
