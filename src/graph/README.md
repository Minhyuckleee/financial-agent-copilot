# graph

Agent 핵심 그래프 — LangGraph `StateGraph`로 조립된 5단계 파이프라인(라우팅 → context → tool call → 가드레일 → answer).

## 그래프 흐름

```
                     query
                       │
                  router ← Tier0
       ┌───────────────┼───────────────┐
상품추천/환율조회   사내규정질의(RAG)   out_of_scope
       │                   │              │
  ┌─→ tool call ← Tier1/2  │              │
  │      │  │              │              │
  └──────┘  └─────┬────────┘              │
                  │                       │
              guardrail                   │
                  │                       │
                answer ───────────────────┘

Tier0 — 라우팅 실패 시 노드 내부에서 1회 재작성 후 재분류
Tier1/2 — API레벨 예외처리(tool call 그래프 self-loop 재시도)
```

router 직후 LangGraph의 conditional edge로 route별로 필요한 노드로만 바로 분기합니다 — 해당 없는 노드는 아예 호출되지 않습니다.

조건부 조기종료:
- out_of_scope로 확정되면 context/tool_call/guardrail 전부 건너뛰고 고정문구로 바로 answer
- context에서 confidence 필터 통과 chunk가 0개면 tool_call/guardrail을 건너뛰고 바로 answer
- tool_call 예외(Tier1/Tier2) 재시도 상한을 초과하면 guardrail을 건너뛰고 바로 answer

## 파일별 역할

0. **router** - 사용자의 현재 발화와 history를 기반으로 클래스 분류를 합니다. 해당 발화의 의도를 파악하지 못했을 시, 질문을 재작성하여 router에서 1회 재시도되고(Tier0) 실패시 end 됩니다.

1. **context** - router에서 사내규정질의로 분류하였을 시 RAG 검색을 합니다. FAISS confidence score 기준으로 특정 임계값을 넘지 못할 시 chunk 반환이 되지 않습니다. chunk는 최대 6개에서 최소 0개 반환되며 0개 반환시 end 됩니다.

2. **tool_call** - router에서 상품추천 및 환율조회로 분류하였을 시 실행됩니다. 이때 API 레벨의 예외처리는 API 자체문제로 보는 Tier 1과 agent에서 parameter 설정을 잘못 뽑았다고 보는 Tier 2로 구분하여 진행합니다.

3. **guardrail** - context 및 tool_call에서 뽑은 context와 사용자 발화를 바탕으로 1차 답변 생성을 진행합니다. 이후 해당 답변의 안정성을 보장하기 위해 5개의 가드레일 규칙을 통과시킵니다.

4. **answer** - 최종 답변을 확정합니다.

* **builder** - 그래프 조립(흐름제어)
* **state** - 공유 상태 스키마
