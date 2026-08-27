"""tool 선택 전략(A vs B) 재현 확인용 추가 50건 생성.

`tool_selection_strategy_dataset.json`(100건)에서 절차형(예: "어떻게 신청하나요?")이
naive 지시와 목적재정의 지시의 성공률 차이가 가장 크게 나는 유형임을 확인했습니다. 같은
발견이 다른 문구·다른 조건값으로도 재현되는지 보기 위해 추가로 구성한 50건입니다.

100건과 겹치지 않도록:
1. 절차형 문구 10개 전부 100건의 5개("어떻게 신청하나요?" 등)와 다르게 새로 작성
2. 이전 턴 조건값(은행명/신용점수/기간)도 다르게 설정
3. 전부 복합조건(이전 턴에 구체조건 있음)으로 구성 — tool 재선택뿐 아니라 파라미터
   보존까지 같이 확인

실행: PYTHONPATH=src .venv/Scripts/python.exe scripts/build_tool_selection_strategy_testset.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
EVAL_DIR = ROOT / "data" / "eval"

# train과 다른 값으로 설정(train: deposit[6,24,36], credit_loan[650,750,800],
# jeonse[농협은행,하나은행,신협], mortgage[국민은행,부산은행,경남은행], business[600,700,850])
_PRODUCTS = {
    "deposit": {
        "label": "정기예금",
        "tool_name": "recommend_deposit_products",
        "param_key": "save_term_months",
        "param_value": 12,
        "turn1_query": "12개월짜리 정기예금 좋은 상품 추천해줘",
    },
    "credit_loan": {
        "label": "신용대출",
        "tool_name": "recommend_credit_loan_products",
        "param_key": "credit_score",
        "param_value": 720,
        "turn1_query": "신용점수 720인 고객 신용대출 알아봐줘",
    },
    "jeonse_loan": {
        "label": "전세자금대출",
        "tool_name": "recommend_jeonse_loan_products",
        "param_key": "bank_name_filter",
        "param_value": "신한은행",
        "turn1_query": "신한은행 전세자금대출 상품 알아봐줘",
    },
    "mortgage_loan": {
        "label": "주택담보대출",
        "tool_name": "recommend_mortgage_loan_products",
        "param_key": "bank_name_filter",
        "param_value": "하나은행",
        "turn1_query": "하나은행 주택담보대출 상품 알아봐줘",
    },
    "business_loan": {
        "label": "사업자대출",
        "tool_name": "recommend_business_loan_products",
        "param_key": "credit_score",
        "param_value": 680,
        "turn1_query": "신용점수 680인 사업자대출 알아봐줘",
    },
}

# train의 5개 절차형 문구("어떻게 신청하나요?", "신청은 어디서 하나요?", "필요한 서류가
# 있나요?", "언제부터 신청 가능해요?", "신청 절차가 궁금해요")와 안 겹치는 신규 10개
_PROCEDURAL_TEMPLATES_V2 = [
    "가입 방법을 알려주세요",
    "심사는 얼마나 걸리나요?",
    "온라인으로도 신청 가능한가요?",
    "지금 바로 신청할 수 있나요?",
    "가입하려면 뭐가 필요해요?",
    "어디로 연락하면 되나요?",
    "방문 안 하고도 되나요?",
    "가입 조건이 따로 있나요?",
    "처리 기간이 얼마나 걸려요?",
    "지금 신청하면 언제 되나요?",
]


def build() -> list[dict]:
    cases = []
    for product_id, product in _PRODUCTS.items():
        turn1_answer = f"{product['label']} 상품 3건을 안내드립니다."
        for variant_idx, turn2_query in enumerate(_PROCEDURAL_TEMPLATES_V2, start=1):
            cases.append(
                {
                    "id": f"test_{product_id}_procedural_{variant_idx}",
                    "product": product_id,
                    "phrasing_type": "procedural",
                    "complexity": "complex",
                    "turn1_query": product["turn1_query"],
                    "turn1_answer": turn1_answer,
                    "turn2_query": turn2_query,
                    "expected_tool_name": product["tool_name"],
                    "expected_tool_params_contains": {product["param_key"]: product["param_value"]},
                }
            )
    return cases


def main() -> None:
    cases = build()
    assert len(cases) == 50, f"50건이어야 하는데 {len(cases)}건"
    out_path = EVAL_DIR / "tool_selection_strategy_testset.json"
    out_path.write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"저장: {out_path} ({len(cases)}건)")


if __name__ == "__main__":
    main()
