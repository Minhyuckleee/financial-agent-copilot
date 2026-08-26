"""금융감독원 「금융상품한눈에」 예금·대출 상품추천 tool.

개인신용대출 API는 공시된 신용점수구간별 금리표만 반환한다 — 실제 대출 승인·한도
심사(신용평가)는 하지 않는다. 심사는 고영향AI 규제 대상(설명가능성 의무)이라 이
프로젝트 스코프 밖이고, 이 tool은 정기예금 tool과 동일한 위험도의 정보조회일 뿐이다.
"""
import os

import httpx
from langchain_core.tools import tool
from pydantic import BaseModel

from tools.fault_injection import with_fault_injection

_TOP_FIN_GRP_NO = "020000"  # 은행권

_CREDIT_GRADE_LABELS = {
    "crdt_grad_1": "900점 초과",
    "crdt_grad_4": "801~900점",
    "crdt_grad_5": "701~800점",
    "crdt_grad_6": "601~700점",
    "crdt_grad_10": "501~600점",
    "crdt_grad_11": "401~500점",
    "crdt_grad_12": "301~400점",
    "crdt_grad_13": "300점 이하",
}


_NH_KEYWORD = "농협"


def _pick_with_nh_priority(sorted_recommendations: list[dict], top_n: int = 3) -> list[dict]:
    """선호순으로 정렬된 추천 리스트에서 상위 top_n을 뽑되, NH(농협) 상품이 그
    안에 없으면 NH 최고조건 1건을 맨 앞에 끼워넣는다 — "NH 상담원용 도구인데
    전은행권 무작위 top3라 NH 상품이 후보에 아예 안 뜬다"는 문제(세션 논의,
    페르소나 02-kim/01-park 시연에서 실제로 재현됨)를 해결한다. 시장 상위권을
    숨기지 않고 NH를 추가로 보장하는 방식이라 비교 정보 자체는 그대로 유지된다."""
    top = sorted_recommendations[:top_n]
    if any(_NH_KEYWORD in r["bank_name"] for r in top):
        return top
    nh_best = next((r for r in sorted_recommendations if _NH_KEYWORD in r["bank_name"]), None)
    if nh_best is None:
        return top
    combined = [nh_best] + top[: top_n - 1]
    # NH를 맨 앞으로 강제 고정하면 실제 순위(금리 등)를 왜곡해 보여줄 수 있어서,
    # 원래 정렬 순서(sorted_recommendations 안에서의 위치) 기준으로 다시 정렬한다 —
    # NH 포함은 보장하되 "가장 좋은 조건이 맨 위"라는 원래 의미는 유지.
    return sorted(combined, key=sorted_recommendations.index)


def _credit_grade_field(credit_score: int) -> str:
    if credit_score > 900:
        return "crdt_grad_1"
    if credit_score > 800:
        return "crdt_grad_4"
    if credit_score > 700:
        return "crdt_grad_5"
    if credit_score > 600:
        return "crdt_grad_6"
    if credit_score > 500:
        return "crdt_grad_10"
    if credit_score > 400:
        return "crdt_grad_11"
    if credit_score > 300:
        return "crdt_grad_12"
    return "crdt_grad_13"


class DepositRecommendation(BaseModel):
    bank_name: str
    product_name: str
    save_term_months: int
    interest_rate: float  # 기본금리
    interest_rate_preferential: float  # 우대금리 포함 최고금리


@tool
@with_fault_injection("recommend_deposit_products")
def recommend_deposit_products(
    save_term_months: int = 12, bank_name_filter: str | None = None
) -> list[dict]:
    """가입기간(개월)에 맞는 정기예금 상품을 금리 높은 순으로 최대 3개 추천한다.

    bank_name_filter: 특정 은행으로 좁히고 싶을 때 은행명 일부(예: "농협") 전달. 미지정 시 전체 은행권 대상.
    """
    key = os.environ["FINLIFE_API_KEY"]
    base = os.environ["FINLIFE_BASE_URL"]

    resp = httpx.get(
        f"{base}/depositProductsSearch.json",
        params={"auth": key, "topFinGrpNo": _TOP_FIN_GRP_NO, "pageNo": 1},
        timeout=10,
        follow_redirects=True,
    )
    resp.raise_for_status()
    result = resp.json()["result"]

    if result["err_cd"] != "000":
        raise RuntimeError(f"{result['err_cd']}: {result['err_msg']}")

    products_by_key = {
        (p["fin_co_no"], p["fin_prdt_cd"]): p for p in result.get("baseList", [])
    }
    if bank_name_filter:
        products_by_key = {
            k: p for k, p in products_by_key.items() if bank_name_filter in p["kor_co_nm"]
        }

    matching_options = [
        o
        for o in result.get("optionList", [])
        if o.get("save_trm") == str(save_term_months)
        and (o["fin_co_no"], o["fin_prdt_cd"]) in products_by_key
    ]
    matching_options.sort(key=lambda o: o.get("intr_rate2") or 0, reverse=True)

    recommendations = []
    for option in matching_options:
        product = products_by_key.get((option["fin_co_no"], option["fin_prdt_cd"]))
        if not product:
            continue
        recommendations.append(
            DepositRecommendation(
                bank_name=product["kor_co_nm"],
                product_name=product["fin_prdt_nm"],
                save_term_months=save_term_months,
                interest_rate=option.get("intr_rate") or 0,
                interest_rate_preferential=option.get("intr_rate2") or 0,
            ).model_dump()
        )
    return _pick_with_nh_priority(recommendations)


class CreditLoanRecommendation(BaseModel):
    bank_name: str
    product_name: str
    loan_type: str
    credit_score_band: str
    interest_rate: float


@tool
@with_fault_injection("recommend_credit_loan_products")
def recommend_credit_loan_products(
    credit_score: int = 700, bank_name_filter: str | None = None
) -> list[dict]:
    """고객 신용점수(0~1000)에 맞는 개인신용대출 상품을 공시금리 낮은 순으로 최대 3개 추천한다.
    실제 대출 승인 여부·한도는 결정하지 않는다 — 공시된 금리표 조회만 제공한다.

    bank_name_filter: 특정 은행으로 좁히고 싶을 때 은행명 일부(예: "농협") 전달. 미지정 시 전체 은행권 대상.
    """
    key = os.environ["FINLIFE_API_KEY"]
    base = os.environ["FINLIFE_BASE_URL"]

    resp = httpx.get(
        f"{base}/creditLoanProductsSearch.json",
        params={"auth": key, "topFinGrpNo": _TOP_FIN_GRP_NO, "pageNo": 1},
        timeout=10,
        follow_redirects=True,
    )
    resp.raise_for_status()
    result = resp.json()["result"]

    if result["err_cd"] != "000":
        raise RuntimeError(f"{result['err_cd']}: {result['err_msg']}")

    products_by_key = {
        (p["fin_co_no"], p["fin_prdt_cd"]): p for p in result.get("baseList", [])
    }
    if bank_name_filter:
        products_by_key = {
            k: p for k, p in products_by_key.items() if bank_name_filter in p["kor_co_nm"]
        }

    grade_field = _credit_grade_field(credit_score)
    matching_options = [
        o
        for o in result.get("optionList", [])
        # 이 API는 같은 상품에 대해 대출금리(A)/기준금리(B)/가산금리(C) 세 행을 따로 준다
        # (finlife 실API 응답에서 확인). A(대출금리)만 걸러야 한다 — 안 그러면
        # 스프레드 성분인 가산금리(C, 값이 항상 제일 작음)가 "최저금리"로 잘못 뽑힌다.
        if o.get("crdt_lend_rate_type") == "A"
        and o.get(grade_field) is not None
        and (o["fin_co_no"], o["fin_prdt_cd"]) in products_by_key
    ]
    matching_options.sort(key=lambda o: o[grade_field])

    recommendations = []
    for option in matching_options:
        product = products_by_key.get((option["fin_co_no"], option["fin_prdt_cd"]))
        if not product:
            continue
        recommendations.append(
            CreditLoanRecommendation(
                bank_name=product["kor_co_nm"],
                product_name=product["fin_prdt_nm"],
                loan_type=product["crdt_prdt_type_nm"],
                credit_score_band=_CREDIT_GRADE_LABELS[grade_field],
                interest_rate=option[grade_field],
            ).model_dump()
        )
    return _pick_with_nh_priority(recommendations)


class LoanRateRecommendation(BaseModel):
    bank_name: str
    product_name: str
    lend_rate_min: float
    lend_rate_max: float


def _recommend_loan_by_min_rate(endpoint: str, bank_name_filter: str | None) -> list[dict]:
    """전세자금대출/주택담보대출 공통 로직 — 이 두 API는 신용점수구간별 금리표가
    아니라 상품별 금리범위(lend_rate_min/max)만 제공한다(finlife.fss.or.kr 실제
    API 스펙 페이지에서 확인, 개인신용대출과 응답 스키마가 다름). 상품 하나가
    상환유형·금리유형별로 여러 옵션을 가질 수 있어, 상품별 최저금리 옵션만
    골라 그 기준으로 순위를 매긴다."""
    key = os.environ["FINLIFE_API_KEY"]
    base = os.environ["FINLIFE_BASE_URL"]

    resp = httpx.get(
        f"{base}/{endpoint}.json",
        params={"auth": key, "topFinGrpNo": _TOP_FIN_GRP_NO, "pageNo": 1},
        timeout=10,
        follow_redirects=True,
    )
    resp.raise_for_status()
    result = resp.json()["result"]

    if result["err_cd"] != "000":
        raise RuntimeError(f"{result['err_cd']}: {result['err_msg']}")

    products_by_key = {
        (p["fin_co_no"], p["fin_prdt_cd"]): p for p in result.get("baseList", [])
    }
    if bank_name_filter:
        products_by_key = {
            k: p for k, p in products_by_key.items() if bank_name_filter in p["kor_co_nm"]
        }

    best_option_by_product: dict[tuple, dict] = {}
    for option in result.get("optionList", []):
        key_pair = (option["fin_co_no"], option["fin_prdt_cd"])
        if key_pair not in products_by_key:
            continue
        rate = option.get("lend_rate_min")
        if rate is None:
            continue
        current = best_option_by_product.get(key_pair)
        if current is None or rate < current["lend_rate_min"]:
            best_option_by_product[key_pair] = option

    ranked = sorted(best_option_by_product.items(), key=lambda item: item[1]["lend_rate_min"])

    recommendations = []
    for key_pair, option in ranked:
        product = products_by_key[key_pair]
        recommendations.append(
            LoanRateRecommendation(
                bank_name=product["kor_co_nm"],
                product_name=product["fin_prdt_nm"],
                lend_rate_min=option["lend_rate_min"],
                lend_rate_max=option.get("lend_rate_max") or option["lend_rate_min"],
            ).model_dump()
        )
    return _pick_with_nh_priority(recommendations)


@tool
@with_fault_injection("recommend_jeonse_loan_products")
def recommend_jeonse_loan_products(bank_name_filter: str | None = None) -> list[dict]:
    """전세자금대출 상품을 최저금리 낮은 순으로 최대 3개 추천한다. 실제 대출 승인
    여부·한도는 결정하지 않는다 — 공시된 금리표 조회만 제공한다.

    bank_name_filter: 특정 은행으로 좁히고 싶을 때 은행명 일부(예: "농협") 전달. 미지정 시 전체 은행권 대상.
    """
    return _recommend_loan_by_min_rate("rentHouseLoanProductsSearch", bank_name_filter)


@tool
@with_fault_injection("recommend_mortgage_loan_products")
def recommend_mortgage_loan_products(bank_name_filter: str | None = None) -> list[dict]:
    """주택담보대출 상품을 최저금리 낮은 순으로 최대 3개 추천한다. 실제 대출 승인
    여부·한도는 결정하지 않는다 — 공시된 금리표 조회만 제공한다.

    bank_name_filter: 특정 은행으로 좁히고 싶을 때 은행명 일부(예: "농협") 전달. 미지정 시 전체 은행권 대상.
    """
    return _recommend_loan_by_min_rate("mortgageLoanProductsSearch", bank_name_filter)


_BUSINESS_CREDIT_GRADE_LABELS = {
    "val1_grad_1": "900점 초과",
    "val1_grad_2": "801~900점",
    "val1_grad_3": "701~800점",
    "val1_grad_4": "601~700점",
    "val1_grad_5": "501~600점",
    "val1_grad_6": "401~500점",
    "val1_grad_7": "301~400점",
    "val1_grad_8": "300점 이하",
}


def _business_credit_grade_field(credit_score: int) -> str:
    """개인사업자대출 API의 신용구간 필드는 개인신용대출(crdt_grad_1/4/5/6/10/11/12/13,
    비순차)과 다르게 val1_grad_1~8로 순차 매핑된다 — finlife 실제 API 스펙 페이지에서
    확인, _credit_grade_field()를 그대로 재사용하면 안 됨."""
    if credit_score > 900:
        return "val1_grad_1"
    if credit_score > 800:
        return "val1_grad_2"
    if credit_score > 700:
        return "val1_grad_3"
    if credit_score > 600:
        return "val1_grad_4"
    if credit_score > 500:
        return "val1_grad_5"
    if credit_score > 400:
        return "val1_grad_6"
    if credit_score > 300:
        return "val1_grad_7"
    return "val1_grad_8"


class BusinessLoanRecommendation(BaseModel):
    bank_name: str
    product_name: str
    credit_score_band: str
    interest_rate: float


@tool
@with_fault_injection("recommend_business_loan_products")
def recommend_business_loan_products(
    credit_score: int = 700, bank_name_filter: str | None = None
) -> list[dict]:
    """고객(개인사업자) 신용점수(0~1000)에 맞는 개인사업자대출 상품을 공시금리 낮은
    순으로 최대 3개 추천한다. 실제 대출 승인 여부·한도는 결정하지 않는다 — 공시된
    금리표 조회만 제공한다.

    bank_name_filter: 특정 은행으로 좁히고 싶을 때 은행명 일부(예: "농협") 전달. 미지정 시 전체 은행권 대상.
    """
    key = os.environ["FINLIFE_API_KEY"]
    base = os.environ["FINLIFE_BASE_URL"]

    resp = httpx.get(
        f"{base}/busiLoanProductsSearch.json",
        params={"auth": key, "topFinGrpNo": _TOP_FIN_GRP_NO, "pageNo": 1},
        timeout=10,
        follow_redirects=True,
    )
    resp.raise_for_status()
    result = resp.json()["result"]

    if result["err_cd"] != "000":
        raise RuntimeError(f"{result['err_cd']}: {result['err_msg']}")

    products_by_key = {
        (p["fin_co_no"], p["fin_prdt_cd"]): p for p in result.get("baseList", [])
    }
    if bank_name_filter:
        products_by_key = {
            k: p for k, p in products_by_key.items() if bank_name_filter in p["kor_co_nm"]
        }

    grade_field = _business_credit_grade_field(credit_score)
    matching_options = [
        o
        for o in result.get("optionList", [])
        if o.get(grade_field)  # 0(해당 신용구간 미취급)과 None(미제공) 둘 다 걸러냄 —
        # 정기예금·개인신용대출과 달리 이 API는 취급 안 하는 구간을 0으로 채워서 줌,
        # 그대로 두면 "0%"가 가장 저렴한 금리로 오인되어 최우선 추천됨(실제로 확인됨)
        and (o["fin_co_no"], o["fin_prdt_cd"]) in products_by_key
    ]
    matching_options.sort(key=lambda o: o[grade_field])

    recommendations = []
    for option in matching_options:
        product = products_by_key.get((option["fin_co_no"], option["fin_prdt_cd"]))
        if not product:
            continue
        recommendations.append(
            BusinessLoanRecommendation(
                bank_name=product["kor_co_nm"],
                product_name=product["fin_prdt_nm"],
                credit_score_band=_BUSINESS_CREDIT_GRADE_LABELS[grade_field],
                interest_rate=option[grade_field],
            ).model_dump()
        )
    return _pick_with_nh_priority(recommendations)

# 연금저축(annuitySavingProductsSearch) — 시도했으나 뺌. finlife.fss.or.kr 공식
# 문서상 스펙(pnsn_kind/save_trm/intr_rate 필드)과 실제 응답이 다름 — topFinGrpNo를
# 020000/050000/060000으로 바꿔가며 실호출해봐도 매번 개인사업자대출과 동일한
# 필드(val1_grad_1~8, lend_rate_min/max/avg)가 나오고, total_count와 실제
# option 개수도 서로 안 맞음(예: total_count=0인데 option 5건, total_count=297인데
# option 0건) — 우리 코드 문제가 아니라 API 서버쪽 응답이 스펙과 어긋나는 것으로
# 판단. 억지로 잘못된 데이터를 매핑해서 쓰지 않고 스코프에서 제외함.
