"""한국은행 ECOS — 원/달러 환율조회 tool."""
import os
from datetime import datetime, timedelta

import httpx
from langchain_core.tools import tool
from pydantic import BaseModel

from tools.fault_injection import with_fault_injection

_STAT_CODE = "731Y003"  # 3.1.1.3. 원화의 대미달러, 원화의 대위안/대엔 환율
_ITEM_CODE = "0000003"  # 원/달러(종가 15:30)


class ExchangeRateResult(BaseModel):
    currency_pair: str
    rate: float
    base_date: str


@tool
@with_fault_injection("inquire_exchange_rate")
def inquire_exchange_rate() -> dict:
    """가장 최근 원/달러 환율(종가)을 조회한다."""
    key = os.environ["ECOS_API_KEY"]
    base = os.environ["ECOS_BASE_URL"]

    end = datetime.now()
    start = end - timedelta(days=10)
    url = (
        f"{base}/StatisticSearch/{key}/json/kr/1/10/{_STAT_CODE}/D/"
        f"{start.strftime('%Y%m%d')}/{end.strftime('%Y%m%d')}/{_ITEM_CODE}"
    )

    resp = httpx.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if "RESULT" in data:
        raise RuntimeError(f"ECOS 에러: {data['RESULT']}")

    rows = data.get("StatisticSearch", {}).get("row", [])
    if not rows:
        raise RuntimeError("최근 10일간 환율 데이터 없음")

    latest = rows[-1]
    result = ExchangeRateResult(
        currency_pair="USD/KRW",
        rate=float(latest["DATA_VALUE"]),
        base_date=latest["TIME"],
    )
    return result.model_dump()
