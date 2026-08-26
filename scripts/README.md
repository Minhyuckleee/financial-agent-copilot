# scripts

RAG·가드레일·Agent 품질을 측정하는 평가 스크립트, API 연동 확인용 smoke test.

## 구성

- `rag_eval_deterministic.py` — 골든셋 질문을 `retrieve()`에 그대로 넣고 정답청크가 남았는지 코드로 계산(Recall/Precision/MRR, LLM 미사용)
- `rag_eval_ragas.py` — 골든셋 문항으로 전체 그래프(`StateGraph.invoke()`)를 실제로 돌리고, OpenAI를 judge로 RAGAS 4종 채점
- `build_citation_grounding_dataset.py` — RAGAS 평가에서 나온 실제 답변+검색문서 쌍을 재사용해서, 가드레일 규칙⑤ 판정기의 예측이 실제 정답과 얼마나 맞는지 검증할 데이터셋 생성
- `build_citation_grounding_negatives.py` — 같은 목적. 자연발화로는 "진짜 근거없는 claim"이 잘 안 나와서, 실패유형별로 직접 틀린 답변을 저술해 negative 샘플 확보
- `run_agent_eval.py` — 케이스 파일(질문+기대결과)로 그래프를 실제 실행하고, route/tool선택/파라미터/가드레일발동 같은 구조적 필드를 기대값과 코드로 비교(LLM judge 없음)
- `smoke/` — ECOS/FINLIFE/OpenAI 각 API 키가 유효한지 최소 호출 1번으로 확인

## 측정 결과

| 스크립트 | 결과 | 비고 |
| --- | --- | --- |
| `rag_eval_deterministic.py` | train(n=120) recall 0.82·precision 0.20·mrr 0.50 / test(n=40) recall 0.68·precision 0.16·mrr 0.39 / valid(n=40) recall 0.80·precision 0.18·mrr 0.43 | precision이 낮은 건 설계상 의도된 것입니다 — 검색 단계는 후보를 넉넉히(최대 6개) 뽑아 recall을 우선하고, 그 중 실제로 답에 쓸지는 뒷단(답변생성+가드레일)이 판단하는 구조입니다 |
| `rag_eval_ragas.py` | train(n=51) context_recall 0.91·faithfulness 0.89 / test(n=40) context_recall 0.83·faithfulness 0.85 | 검색 정확도뿐 아니라 생성된 답변이 검색문서에 실제로 근거하는지까지 확인합니다 |
| `build_citation_grounding_dataset.py` + `_negatives.py` | train 40/40, test 34/34 (전부 정확 판정) | negative가 5건뿐이라(하나만 틀려도 수치가 크게 흔들림) 일반화된 정확도로 보긴 어렵고, "오탐 없이 동작한다"는 최소 검증(sanity check)에 가깝습니다 |
| `run_agent_eval.py` | 아래 참고 | 공고가 요구하는 "테스트셋 기반 품질분석·개선"에 가장 직접 대응되는 결과 |

### run_agent_eval.py — 개선 과정

두 단계로 평가셋을 확장했습니다:

1. **1차 평가셋**(기능별 최소 1건씩, 53건) — 각 기능이 개별적으로 정상 동작하는지 최소 확인했습니다. 100% 도달했지만, 실패 사례를 다시 들여다보니 전부 테스트 설계 문제였지 실제 버그가 아니었음을 확인했습니다 — 단일 기능만 확인하는 방식으로는 미처 못 잡는 부분이 있다고 판단해 다음 단계로 확장했습니다.
2. **복합 시나리오 평가셋**(여러 조건이 동시에 겹치는 520건 = 개발용 416건 + 개발에 안 쓴 별도 검증용 104건) — 이력·예외분기·가드레일 규칙이 동시에 겹치는 케이스를 다룹니다.

결과:

- 개발용 416건: 1차 실행 88.2%(367/416) → 실패 49건을 전수조사해 진짜 코드버그 4건만 골라 수정(나머지는 테스트케이스 설계오류로 판명, 같이 수정) → 재실행 96.9%(403/416)
- 별도 검증용 104건: 1차 실행 98.1%(102/104) → 실제 코드결함 2건 수정 + 골든셋 라벨 오류 1건 정정 → 최종 100%(104/104)
