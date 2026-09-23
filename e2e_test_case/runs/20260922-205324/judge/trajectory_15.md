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

<case id="E001">
<trajectory>
input: 신한은행 18개월 정기예금 추천해줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_deposit_products", "args": {"save_term_months": 18, "bank_name_filter": "신한"}, "error": "empty_result"}
- call_tool {"name": "recommend_deposit_products", "args": {"save_term_months": 18}, "error": "empty_result"}
- answer_tier2_exhausted {"low_confidence": true}
- finalize_answer {}
final output: 신한은행의 18개월 정기예금 상품은 현재 조회 결과가 없습니다.

※ 이 조건으로는 충분히 찾지 못해, 확인된 정보만 안내드립니다.
</trajectory>
</case>

<case id="E002">
<trajectory>
input: 9개월짜리 정기예금 있어?
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_deposit_products", "args": {"save_term_months": 9}, "error": "empty_result"}
- call_tool {"name": "recommend_deposit_products", "args": {}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 9개월짜리 정기예금 상품은 조회 결과 현재 제공되고 있지 않습니다. 대신, 조건을 완화해서 전체 정기예금 상품을 조회해보니 12개월짜리 상품들만 확인되었습니다. 만약 9개월 정기예금 상품이 필요하시다면, 추후 다시 한 번 확인해보시거나 12개월 상품을 고려해보시는 것도 좋을 것 같습니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="E003">
<trajectory>
input: 신용점수 1200점인데 신용대출 금리 알려줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_credit_loan_products", "args": {"credit_score": 1000}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 신용점수가 1200점일 경우, 조회 결과에 따르면 다음과 같은 신용대출 금리를 확인할 수 있습니다.

- 국민은행 마이너스한도대출: 연 4.95%
- 수협은행 개인신용대출: 연 4.95%
- 농협은행 가계신용대출(일반): 연 5.34%

위 금리는 모두 신용점수 900점 초과 구간에 해당하는 금리입니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="E004">
<trajectory>
input: 토스뱅크 전세자금대출 금리 알려줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_jeonse_loan_products", "args": {"bank_name_filter": "토스뱅크"}, "error": null, "result_count": 1}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 토스뱅크의 전세자금대출 상품인 '전월세보증금대출 플러스'의 금리는 연 4.36%입니다.
</trajectory>
</case>

<case id="E005">
<trajectory>
input: 그 은행으로 신용대출도 봐주세요
history:
사용자: 국민은행 정기예금 좀 알아봐줘
에이전트: 국민은행 정기예금 상품을 안내드립니다.
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_credit_loan_products", "args": {"bank_name_filter": "국민은행"}, "error": null, "result_count": 1}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 국민은행의 신용대출 상품으로는 '마이너스한도대출'이 있습니다. 신용점수 601~700점 구간에서 적용되는 금리는 7.7%입니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>
