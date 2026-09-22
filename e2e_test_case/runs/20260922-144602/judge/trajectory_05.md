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

<case id="C021">
<trajectory>
input: 주택담보대출 금리 낮은 곳 추천해줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_mortgage_loan_products", "args": {"bank_name_filter": null}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["prohibited_terms"]}
- finalize_answer {}
final output: 현재 조회된 주택담보대출 상품 중에서 금리가 가장 낮은 곳은 경남은행의 '집집마다 도움대출II'로, 최저 금리가 3.7%입니다. 그 다음으로는 우리은행의 '우리아파트론'(최저 4.18%), 농협은행의 'NH주택담보대출'(최저 4.49%) 순입니다.
</trajectory>
</case>

<case id="C022">
<trajectory>
input: 신한은행 주담대 금리 알려줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_mortgage_loan_products", "args": {"bank_name_filter": "신한"}, "error": null, "result_count": 2}
- run_guardrail {"guardrail": ["numeric_self_check"]}
- finalize_answer {}
final output: 신한은행의 주택담보대출(주담대) 금리는 상품에 따라 다르며, 현재 조회된 결과에 따르면 다음과 같습니다.

- 신한주택대출(아파트): 연 4.39% ~ 5.69%
- 신한주택대출: 연 4.39% ~ 5.79%

실제 적용 금리는 대출 조건이나 신용도 등에 따라 달라질 수 있으니 참고하시기 바랍니다.
</trajectory>
</case>

<case id="C023">
<trajectory>
input: 하나은행 주택담보대출 상품 있어?
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_mortgage_loan_products", "args": {"bank_name_filter": "하나은행"}, "error": null, "result_count": 1}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 네, 하나은행에는 "하나원큐아파트론2"라는 주택담보대출 상품이 있습니다. 이 상품의 대출 금리는 연 4.5%에서 5.7% 사이입니다.
</trajectory>
</case>

<case id="C024">
<trajectory>
input: 집 사려고 하는데 대출 금리 어디가 괜찮아?
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_mortgage_loan_products", "args": {"bank_name_filter": null}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 현재 조회된 주택담보대출 금리를 보면,  
- 경남은행의 '집집마다 도움대출II'가 연 3.7%~5.51%  
- 우리은행의 '우리아파트론'이 연 4.18%~5.28%  
- 농협은행의 'NH주택담보대출'이 연 4.49%~6.29%입니다.

이 중에서는 경남은행의 최저 금리(3.7%)가 가장 낮고, 우리은행은 최대 금리가 상대적으로 낮은 편(5.28%)입니다. 본인의 조건(신용도, 대출기간 등)에 따라 실제 적용 금리는 달라질 수 있으니, 여러 은행에 상담을 받아보시고 비교해보시는 것이 좋겠습니다.
</trajectory>
</case>

<case id="C025">
<trajectory>
input: 주담대 금리 은행별로 비교해줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_mortgage_loan_products", "args": {"bank_name_filter": null}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 현재 조회된 주택담보대출(주담대) 금리를 은행별로 비교해드리면 다음과 같습니다.

- 경남은행의 '집집마다 도움대출II' 상품은 금리가 연 3.7%에서 5.51% 사이입니다.
- 우리은행의 '우리아파트론' 상품은 연 4.18%에서 5.28% 사이입니다.
- 농협은행의 'NH주택담보대출' 상품은 연 4.49%에서 6.29% 사이입니다.

각 은행별로 최저 금리와 최고 금리가 다르니, 본인의 조건에 맞는 상품을 선택하시는 것이 좋겠습니다.
</trajectory>
</case>
