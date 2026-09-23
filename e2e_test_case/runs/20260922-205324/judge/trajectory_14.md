You are an expert data labeler.
Your task is to grade the accuracy of an AI agent's internal trajectory.

<Rubric>
  An accurate trajectory:
  - Makes logical sense between steps
  - Shows clear progression
  - Is relatively efficient, though it does not need to be perfectly efficient
  - A single retry or reinterpretation after an API failure or empty result is expected, not inefficient
</Rubric>

First, try to understand the goal of the trajectory by looking at the input
(if the input is not present try to infer it from the content of the first message),
as well as the output of the final message. Once you understand the goal, grade the trajectory
as it relates to achieving that goal.

Grade the following trajectory:

<trajectory>
{outputs}
</trajectory>

Write the key observations that decide the grade as short lines in <evidence> tags,
then output PASS or FAIL in <result> tags.


아래 케이스마다 위 기준으로 판정하라. 케이스마다 <case id=...> 로 감싸서 답하라.

<case id="C066">
<trajectory>
input: 24개월로도 보여줘
history:
사용자: 정기예금 추천해줘
에이전트: 12개월 기준 정기예금 상품 3건을 안내드립니다.
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_deposit_products", "args": {"save_term_months": 24}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 24개월(2년) 정기예금 상품으로는 다음과 같은 옵션이 있습니다.

- 부산은행의 '더(The) 특판 정기예금': 기본금리 1.75%, 우대금리 포함 시 최대 3.92%
- 전북은행의 'JB 다이렉트(자유만기) 예금': 기본금리 및 우대금리 모두 3.82%
- 농협은행의 'NH올원e예금': 기본금리 및 우대금리 모두 3.0%

각 상품의 금리와 조건을 참고하셔서 선택하시면 됩니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="C067">
<trajectory>
input: 신용점수 850점이면 어떻게 돼?
history:
사용자: 신용대출 금리 낮은 곳 알려줘
에이전트: 신용점수 700점 기준 신용대출 상품 3건을 안내드립니다.
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_credit_loan_products", "args": {"credit_score": 850}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 신용점수가 850점이면, 여러 은행에서 신용점수 801~900점 구간에 해당하는 대출 상품을 이용할 수 있습니다. 예를 들어,

- 수협은행의 개인신용대출(일반신용대출)은 5.18%의 금리로 이용할 수 있습니다.
- 아이엠뱅크의 장기카드대출(카드론)은 5.19%의 금리로 제공됩니다.
- 농협은행의 가계신용대출(마이너스대출)은 5.7%의 금리로 이용 가능합니다.

즉, 850점이면 위와 같은 금리로 대출 상품을 이용할 수 있습니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="C068">
<trajectory>
input: 한 번 더 조회해줄래?
history:
사용자: 달러 환율 알려줘
에이전트: 현재 USD/KRW 환율은 1,390원입니다.
- route_query {"route": "exchange_rate"}
- call_tool {"name": "inquire_exchange_rate", "args": {}, "error": null, "result_count": 1}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 현재 USD/KRW 환율은 1358.2원입니다. (기준일: 2026.09.22)
</trajectory>
</case>

<case id="C069">
<trajectory>
input: 그중에 국민은행 것만 보여줘
history:
사용자: 전세자금대출 금리 낮은 곳 알려줘
에이전트: 전세자금대출 상품 3건을 안내드립니다.
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_jeonse_loan_products", "args": {"bank_name_filter": "국민"}, "error": null, "result_count": 2}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 국민은행의 전세자금대출 상품은 다음과 같습니다.

1. KB주택전세자금대출: 금리는 연 4.21%에서 5.61%입니다.
2. KB플러스전세자금대출: 금리는 연 4.22%에서 5.62%입니다.
</trajectory>
</case>

<case id="C070">
<trajectory>
input: 교부도 요청할 수 있어?
history:
사용자: 예금거래기본약관은 고객이 볼 수 있어?
에이전트: 네, 영업점에서 영업시간 중 볼 수 있습니다.
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "예금거래기본약관의 교부를 고객이 요청할 수 있는지 확인하고자 합니다.", "retrieved": [{"source": "예금거래기본약관.txt", "score": null}, {"source": "예금거래기본약관.txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}, {"source": "예금거래기본약관.txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 네, 문서에 따르면 고객(거래처)은 영업시간 중 언제든지 예금거래기본약관을 볼 수 있고, 또한 그 교부를 청구할 수 있습니다. 따라서 고객이 예금거래기본약관의 교부를 요청할 수 있습니다.
</trajectory>
</case>
