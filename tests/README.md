# tests

pytest 테스트 스위트입니다. 두 계층으로 나뉩니다 — 노드 함수 단위 테스트(mock 없이 실제 LLM/API 호출) + 전체 그래프 e2e 테스트(`StateGraph.invoke()`로 실제 실행).

## 노드 함수 단위 테스트

- `test_router.py` — 라우팅 노드. 4클래스 분류, history 기반 후속질문 처리
- `test_tool_call.py` — tool call 노드. Tier1(fail/delay)·Tier2(empty_result/param_invalid/no_selection) 예외분기 전부, 조건부 엣지 분기함수까지 결정론적으로 검증
- `test_guardrail.py` — 가드레일 노드. 여러 규칙 동시발동(전량검사) + 자동교정 확인
- `test_answer.py` — answer 노드. LLM 호출 없는 순수함수임을 확인

## 전체 그래프 e2e 테스트

- `test_graph_exchange_rate.py` — 환율조회 골든패스
- `test_graph_product_recommendation.py` — 상품추천(5종) 골든패스 + history 기반 파라미터 재사용
- `test_graph_policy_qa.py` — 사내규정질의 골든패스
- `test_graph_tier0.py` — 라우팅 재작성(Tier0) 후속질문/최종거절
- `test_graph_tier1.py` — API 레벨 예외(fail/delay)
- `test_graph_tier2.py` — 파라미터 재해석(Tier2)

## 실행

```bash
pip install -e ".[dev]"
PYTHONPATH=src pytest
```

`.env`에 실제 API 키(OpenAI/ECOS/FINLIFE)가 있어야 통과합니다 — mock을 쓰지 않고 실제 외부 API를 그대로 호출합니다.
