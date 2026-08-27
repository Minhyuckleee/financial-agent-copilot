"""tool 선택 프롬프트 전략(naive vs 목적재정의) 비교용 테스트셋 100건 생성.

라우팅(4클래스 분류)이 아니라 tool_call 내부의 "이 tool을 호출할지 말지" 판단 지점을
겨냥한다. 후속발화가 tool이 직접 답할 내용처럼 안 보이면(예: "어떻게 신청하나요?") LLM이
tool 호출 자체를 거부하는데(no_selection), 이때 history는 이미 프롬프트에 들어가 있다 —
차이는 재시도 프롬프트의 "전략"뿐이라는 걸 검증하려는 목적. 정답 라벨은 전부
결정론적(이전 턴 조건으로 고정)이라 사람이 채점할 필요가 없다.

구성: 5개 상품 × 4개 모호발화 유형(절차형/재확인형/이유질문형/맞장구확장형) × 5개 변형
     = 100건. 변형 1~2는 이전 턴이 상품만 언급(단순), 3~5는 구체조건(은행/신용점수/기간)
     포함(복합) — tool 재선택뿐 아니라 파라미터 보존까지 같이 검증한다.

실행: PYTHONPATH=src .venv/Scripts/python.exe scripts/build_tool_selection_strategy_dataset.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
EVAL_DIR = ROOT / "data" / "eval"

_PRODUCTS = {
    "deposit": {
        "label": "정기예금",
        "tool_name": "recommend_deposit_products",
        "simple_query": "정기예금 좋은 상품 추천해줘",
        "complex_param_key": "save_term_months",
        "complex_values": [6, 24, 36],
        "complex_query": lambda v: f"{v}개월짜리 정기예금 좋은 상품 추천해줘",
    },
    "credit_loan": {
        "label": "신용대출",
        "tool_name": "recommend_credit_loan_products",
        "simple_query": "신용대출 상품 알아봐줘",
        "complex_param_key": "credit_score",
        "complex_values": [650, 750, 800],
        "complex_query": lambda v: f"신용점수 {v}인 고객 신용대출 알아봐줘",
    },
    "jeonse_loan": {
        "label": "전세자금대출",
        "tool_name": "recommend_jeonse_loan_products",
        "simple_query": "전세자금대출 상품 알아봐줘",
        "complex_param_key": "bank_name_filter",
        "complex_values": ["농협은행", "하나은행", "신협"],
        "complex_query": lambda v: f"{v} 전세자금대출 상품 알아봐줘",
    },
    "mortgage_loan": {
        "label": "주택담보대출",
        "tool_name": "recommend_mortgage_loan_products",
        "simple_query": "주택담보대출 상품 추천해줘",
        "complex_param_key": "bank_name_filter",
        "complex_values": ["국민은행", "부산은행", "경남은행"],
        "complex_query": lambda v: f"{v} 주택담보대출 상품 알아봐줘",
    },
    "business_loan": {
        "label": "사업자대출",
        "tool_name": "recommend_business_loan_products",
        "simple_query": "사업자대출 상품 알아봐줘",
        "complex_param_key": "credit_score",
        "complex_values": [600, 700, 850],
        "complex_query": lambda v: f"신용점수 {v}인 사업자대출 알아봐줘",
    },
}

_PHRASING_TYPES = {
    "procedural": [  # 절차형 — tool이 제일 안 어울려 보임(가장 어려운 유형)
        "어떻게 신청하나요?",
        "신청은 어디서 하나요?",
        "필요한 서류가 있나요?",
        "언제부터 신청 가능해요?",
        "신청 절차가 궁금해요",
    ],
    "reconfirm": [  # 재확인형
        "그게 다예요?",
        "다시 한번 봐주세요",
        "정말이에요?",
        "다시 조회해주세요",
        "확실한 건가요?",
    ],
    "reason": [  # 이유질문형
        "왜 안돼요?",
        "그건 왜 그런거죠?",
        "왜 그런 거예요?",
        "이유가 뭔가요?",
        "어째서 그런가요?",
    ],
    "vague": [  # 맞장구/확장형
        "그런가요?",
        "그거 좀 더 알려주세요",
        "음, 그래요?",
        "좀 더 자세히요",
        "그거 어떻게 되나요?",
    ],
}


def build() -> list[dict]:
    cases = []
    for product_id, product in _PRODUCTS.items():
        for type_id, phrasings in _PHRASING_TYPES.items():
            for variant_idx, turn2_query in enumerate(phrasings, start=1):
                is_complex = variant_idx >= 3
                if is_complex:
                    complex_value = product["complex_values"][variant_idx - 3]
                    turn1_query = product["complex_query"](complex_value)
                    expected_params = {product["complex_param_key"]: complex_value}
                else:
                    turn1_query = product["simple_query"]
                    expected_params = {}

                turn1_answer = f"{product['label']} 상품 3건을 안내드립니다."

                cases.append(
                    {
                        "id": f"{product_id}_{type_id}_{variant_idx}",
                        "product": product_id,
                        "phrasing_type": type_id,
                        "complexity": "complex" if is_complex else "simple",
                        "turn1_query": turn1_query,
                        "turn1_answer": turn1_answer,
                        "turn2_query": turn2_query,
                        "expected_tool_name": product["tool_name"],
                        "expected_tool_params_contains": expected_params,
                    }
                )
    return cases


def main() -> None:
    cases = build()
    assert len(cases) == 100, f"100건이어야 하는데 {len(cases)}건"
    out_path = EVAL_DIR / "tool_selection_strategy_dataset.json"
    out_path.write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"저장: {out_path} ({len(cases)}건)")


if __name__ == "__main__":
    main()
