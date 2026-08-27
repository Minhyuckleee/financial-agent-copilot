# scripts

RAG·가드레일·Agent 품질을 측정하는 평가 스크립트, API 연동 확인용 smoke test.

## 구성

- `rag_eval_deterministic.py` — 골든셋 질문을 `retrieve()`에 그대로 넣고 정답청크가 남았는지 코드로 계산(Recall/Precision/MRR, LLM 미사용)
- `rag_eval_ragas.py` — 골든셋 문항으로 전체 그래프(`StateGraph.invoke()`)를 실제로 돌리고, OpenAI를 judge로 RAGAS 4종 채점
- `build_citation_grounding_dataset.py` — RAGAS 평가에서 나온 실제 답변+검색문서 쌍을 재사용해서, 가드레일 규칙⑤ 판정기의 예측이 실제 정답과 얼마나 맞는지 검증할 데이터셋 생성
- `build_citation_grounding_negatives.py` — 같은 목적. 자연발화로는 "진짜 근거없는 claim"이 잘 안 나와서, 실패유형별로 직접 틀린 답변을 저술해 negative 샘플 확보
- `build_citation_grounding_negatives_extra.py` — 위조 표본을 10건→50건으로 늘리기 위해 같은 5실패유형을 미사용 golden 문항 40개에 추가 적용(LLM 초안 생성 + 사람 스팟체크)
- `prepare_citation_grounding_pool100.py` — 규칙⑤ cosine-vs-LLM 비교용 정상 50 + 위조 50 pool 구성(신규 생성 없이 기존 라벨 재사용)
- `eval_citation_grounding_cosine_range.py` — 폐기된 "임베딩 코사인 유사도" 판정 방식을 재현해 정상/위조 그룹의 유사도 range가 얼마나 겹치는지 기술(descriptive, threshold 분류 안 함)
- `eval_citation_grounding_llm_detection.py` — 같은 pool에 현재 프로덕션 판정기(`_check_grounding_llm`)를 그대로 돌려 위조탐지율 측정
- `build_tool_selection_strategy_dataset.py` — tool 선택 프롬프트 전략(naive vs 목적재정의) 비교용 100건 생성(5상품×모호발화 4유형×5변형)
- `build_tool_selection_strategy_testset.py` — 같은 발견의 재현 확인용 추가 50건 생성(100건과 문구·조건값 안 겹침)
- `eval_tool_selection_strategy.py` — 100건에 두 프롬프트 전략을 각각 적용해 tool 호출 성공률·답변 정확도 비교(`tool_call.py` 무변경, 비교용 프롬프트만 스크립트 안에 별도 구현)
- `eval_tool_selection_strategy_testset.py` — 같은 비교를 추가 50건에도 실행
- `run_agent_eval.py` — 케이스 파일(질문+기대결과)로 그래프를 실제 실행하고, route/tool선택/파라미터/가드레일발동 같은 구조적 필드를 기대값과 코드로 비교(LLM judge 없음)
- `smoke/` — ECOS/FINLIFE/OpenAI 각 API 키가 유효한지 최소 호출 1번으로 확인

## 측정 결과

| 스크립트 | 결과 | 비고 |
| --- | --- | --- |
| `rag_eval_deterministic.py` | train(n=120) recall 0.82·precision 0.20·mrr 0.50 / test(n=40) recall 0.68·precision 0.16·mrr 0.39 / valid(n=40) recall 0.80·precision 0.18·mrr 0.43 | precision이 낮은 건 설계상 의도된 것입니다 — 검색 단계는 후보를 넉넉히(최대 6개) 뽑아 recall을 우선하고, 그 중 실제로 답에 쓸지는 뒷단(답변생성+가드레일)이 판단하는 구조입니다 |
| `rag_eval_ragas.py` | train(n=51) context_recall 0.91·faithfulness 0.89 / test(n=40) context_recall 0.83·faithfulness 0.85 | 검색 정확도뿐 아니라 생성된 답변이 검색문서에 실제로 근거하는지까지 확인합니다 |
| `build_citation_grounding_dataset.py` + `_negatives.py` | train 40/40, test 34/34 (전부 정확 판정) | negative가 5건뿐이라(하나만 틀려도 수치가 크게 흔들림) 일반화된 정확도로 보긴 어렵고, "오탐 없이 동작한다"는 최소 검증(sanity check)에 가깝습니다 |
| `eval_citation_grounding_cosine_range.py` + `_llm_detection.py` | 아래 참고 | 규칙⑤를 임베딩 코사인 유사도 방식에서 LLM entailment 판정으로 전환한 근거를 정상 50 + 위조 50 표본으로 재현·검증 |
| `eval_tool_selection_strategy.py` + `_testset.py` | 아래 참고 | tool 선택 재시도 프롬프트를 naive 지시에서 목적재정의 지시로 바꾼 근거를 150건 표본으로 재현·검증 |
| `run_agent_eval.py` | 아래 참고 | 공고가 요구하는 "테스트셋 기반 품질분석·개선"에 가장 직접 대응되는 결과 |

### run_agent_eval.py — 개선 과정

두 단계로 평가셋을 확장했습니다:

1. **1차 평가셋**([agent_eval_v1.json](../data/eval/agent_eval_v1.json), 기능별 최소 1건씩, 53건) — 각 기능이 개별적으로 정상 동작하는지 최소 확인했습니다. 100% 도달했지만, 실패 사례를 다시 들여다보니 전부 테스트 설계 문제였지 실제 버그가 아니었음을 확인했습니다 — 단일 기능만 확인하는 방식으로는 미처 못 잡는 부분이 있다고 판단해 다음 단계로 확장했습니다.
2. **복합 시나리오 평가셋**([agent_quality_train.json](../data/eval/agent_quality_train.json) / [agent_quality_test.json](../data/eval/agent_quality_test.json), 이력·예외분기·가드레일 규칙이 동시에 겹치는 케이스) — route·tool·가드레일 결과를 미리 예측해 expected로 못박았습니다. 8개 유형, 각 8건씩 구성:

| 유형 | 이름 | 검증 목적 |
| --- | --- | --- |
| b8 | 단일턴 route경계 | 조건 하나로 route가 정확히 갈리는지(대조군) |
| b2 | 라우팅 topic-switch 경계 | 상품 이력 중 규정질문으로 화제전환 시 policy_qa로 정확히 넘어가는지 |
| b3 | Tier0 rewrite 성공률 | 모호한 후속발화("왜 그래요?")를 이력 기반으로 재작성해 올바른 route로 복구하는지 |
| b4 | RAG rewrite 충실도 | policy_qa 후속질문이 코퍼스 밖으로 드리프트했을 때 정직하게 거절/근거대조하는지 |
| m1 | 이력+Tier2 조건이어받기 | 상품을 바꿔 재조회할 때 tool은 전환하고 은행명 등 조건은 유지하는지 |
| m4 | 다턴모순 정정 | 이전 턴 조건을 사용자가 정정했을 때 새 값으로 덮어쓰는지 |
| m7 | PII 이력재인용 누출 | 이력에 있던 PII가 무관한 후속질문 답변에 새어나오지 않는지 |
| m10 | Tier0 최종거절+이력있는 상태 | 이력이 있어도 진짜 범위밖 질문은 최종 거절하는지 |

결과:

- train([케이스](../data/eval/agent_quality_train.json) / [결과](../data/eval/agent_quality_train_results.json)) 64건: 1차 실행 87.5%(56/64) → 실패 8건을 전수조사해 원인별로 분리 — **agent 로직버그 2건**(원인 1개: 이력 기반 tool 재사용 프롬프트가 상품전환 요청에도 이전 tool을 고수하던 버그, 프롬프트 수정으로 해결) + **테스트셋 설계 문제 6건**(존재하지 않는 은행-상품 조합 1건, grep만으로 판단한 RAG 커버리지 오판 라벨 4건, 좁은 채점 문구 1건 — `retrieve()` 직접 호출·전체 파이프라인 재실행으로 근본원인 검증 후 데이터만 정정) → 재실행 **100%(64/64)**
- test([케이스](../data/eval/agent_quality_test.json) / [결과](../data/eval/agent_quality_test_results.json)) 16건: **93.8%(15/16)**

### eval_citation_grounding_cosine_range.py / _llm_detection.py — cosine vs LLM 재현 비교

규칙⑤(citation grounding)를 임베딩 코사인 유사도 방식에서 LLM entailment 판정으로 전환한 근거였던
초기 파일럿(negative 5건)은 표본이 너무 작아 일반화하기 어려웠습니다. 정상 50건(실제 파이프라인
출력, 사람이 chunk 대조로 확정한 라벨) + 위조 50건(5개 실패유형 × 10건, 골든셋 문서 기반으로
구성 후 사람이 원문 대조 검증)으로 재현했습니다.

- **cosine 유사도**(claimed_phrase ↔ retrieved chunk 중 최댓값, KURE-v1 임베딩): 정상 range
  [0.629, 0.961](평균 0.777) / 위조 range [0.415, 0.893](평균 0.668) — 위조 50건 중 **34건(68%)**이
  정상 range 안에 그대로 묻혀 threshold 하나로 구분 불가능함을 확인
- **LLM entailment 판정**(`_check_grounding_llm`, 프로덕션 코드 그대로): 정상 50/50 오탐 없음,
  위조 46/50(92%) 탐지. 미탐 4건 중 3건은 구체적 숫자·조항 없이 일반적 어투로 서술된 위조 주장이
  애초에 "citation claim"으로 추출되지 않은 경우(has_citation_claim=False), 1건은 판정
  자체가 틀림(entailment miss) — LLM 판정도 완벽하진 않지만, cosine이 원천적으로 구분 못 하는
  구간을 유의미하게 걸러낸다는 점은 명확함

### eval_tool_selection_strategy.py / _testset.py — tool 선택 프롬프트 전략 비교

후속발화가 tool이 직접 답할 내용처럼 보이지 않으면(예: "어떻게 신청하나요?") LLM이 tool 호출
자체를 거부합니다(no_selection). 이때 이전 대화(history)는 두 조건 다 프롬프트에 동일하게
포함돼 있고, 차이는 재시도 지시 문구(전략)뿐입니다.

- **naive 지시**: "이전 대화를 참고해 반드시 tool을 호출하세요" 정도의 일반적인 재시도 지시
- **목적재정의 지시(현재 프로덕션)**: tool 호출의 목적을 "질문에 직접 답하는 것"이 아니라
  "이전 대화 맥락의 상품 정보를 다시 확보하는 것"으로 재정의하는 구체적인 지시

5개 상품 × 모호 발화 4유형(절차형/재확인형/이유질문형/맞장구형)으로 100건을 구성해 실험한 뒤,
같은 발견이 다른 문구·조건값으로도 재현되는지 확인하기 위해 겹치지 않는 50건을 추가로
구성했습니다(총 150건).

결과:

- 150건 중 87건(58%)은 1차 시도에서 이미 정상적으로 해결됐습니다 — 모호해 보이는 후속질문
  이라고 해서 전부 어려운 것은 아니었습니다. 실제로 재시도 상황까지 간 것은 63건이었고, 그중
  대부분(50건)이 절차형이었습니다.
- 재시도가 필요했던 63건 기준: naive 지시는 tool 호출 성공 50.8%(32/63), 답변 정확도
  50.8%(32/63)에 그쳤고, 목적재정의 지시는 tool 호출 성공 98.4%(62/63), 답변 정확도
  93.7%(59/63)로 개선됐습니다.
- 처음에는 4유형 모두 비슷하게 tool 호출을 방해할 것으로 예상했으나, 실제로는 절차·방법을
  묻는 절차형에서만 이 문제가 두드러졌습니다(다른 3유형은 대부분 1차 시도에서 바로 해결).
