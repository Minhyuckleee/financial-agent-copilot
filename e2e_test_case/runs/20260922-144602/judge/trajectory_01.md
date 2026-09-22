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

<case id="C001">
<trajectory>
input: 정기예금 금리 좋은 거 추천해줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_deposit_products", "args": {"save_term_months": 12}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing", "prohibited_terms"]}
- finalize_answer {}
final output: 그 외에도 부산은행의 '더(The) 특판 정기예금'이 최대 3.92%, 농협은행의 'NH왈츠회전예금 II'가 최대 3.45%의 금리를 제공하고 있습니다. 금리와 조건을 비교해보시고 선택하시면 좋을 것 같습니다. ※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="C002">
<trajectory>
input: 6개월짜리 정기예금 보여줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_deposit_products", "args": {"save_term_months": 6}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 6개월짜리 정기예금 상품은 다음과 같습니다.

1. 부산은행 - 더(The) 레벨업 정기예금  
   - 기본 금리: 연 2.5%  
   - 우대 금리 포함: 연 3.72%

2. 수협은행 - Sh해양플라스틱Zero!예금(만기일시지급식)  
   - 기본 금리: 연 3.2%  
   - 우대 금리 포함: 연 3.55%

3. 농협은행주식회사 - NH왈츠회전예금 II  
   - 기본 금리: 연 3.15%  
   - 우대 금리 포함: 연 3.25%

각 상품의 금리와 조건을 참고해보시기 바랍니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="C003">
<trajectory>
input: 2년짜리 예금 금리 높은 곳 알려줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_deposit_products", "args": {"save_term_months": 24}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 2년(24개월)짜리 예금 상품 중 금리가 높은 곳은 다음과 같습니다.

- 부산은행의 '더(The) 특판 정기예금': 최고 연 3.92% (우대금리 포함)
- 전북은행의 'JB 다이렉트(자유만기) 예금': 연 3.82%
- 농협은행의 'NH올원e예금': 연 3.0%

이 중 부산은행의 '더(The) 특판 정기예금'이 우대금리 적용 시 가장 높은 금리(3.92%)를 제공합니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="C004">
<trajectory>
input: 우리은행 정기예금 상품 뭐 있어?
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_deposit_products", "args": {"bank_name_filter": "우리"}, "error": null, "result_count": 1}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 우리은행의 정기예금 상품으로는 "WON플러스예금"이 있습니다. 가입 기간은 12개월이고, 금리는 연 3.5%입니다. (우대금리 포함 시에도 3.5%입니다.)

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="C005">
<trajectory>
input: 하나은행 3년 정기예금 금리 알려줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_deposit_products", "args": {"save_term_months": 36, "bank_name_filter": "하나"}, "error": null, "result_count": 1}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 하나은행의 3년(36개월) 정기예금 금리는 기본 연 2.3%이고, 우대금리 적용 시 최대 연 2.7%입니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>
