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

<case id="C016">
<trajectory>
input: 국민은행 전세대출 금리 알려줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_jeonse_loan_products", "args": {"bank_name_filter": "국민은행"}, "error": null, "result_count": 2}
- run_guardrail {"guardrail": ["numeric_self_check"]}
- finalize_answer {}
final output: 국민은행의 전세대출 금리는 다음과 같습니다.

- KB주택전세자금대출: 연 4.22% ~ 5.61%
- KB플러스전세자금대출: 연 4.22% ~ 5.62%

금리는 신청 조건이나 신용도 등에 따라 달라질 수 있으니 참고하시기 바랍니다.
</trajectory>
</case>

<case id="C017">
<trajectory>
input: 우리은행 전세자금대출 상품 있어?
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_jeonse_loan_products", "args": {"bank_name_filter": "우리은행"}, "error": null, "result_count": 2}
- run_guardrail {"guardrail": ["numeric_self_check"]}
- finalize_answer {}
final output: 네, 우리은행에는 전세자금대출 상품이 있습니다.  
예를 들어, '우리전세론(서울보증)' 상품은 금리가 연 3.93%에서 4.59% 사이이고,  
'우리전세론(주택금융보증)' 상품은 연 3.93%에서 4.63% 사이의 금리로 이용하실 수 있습니다.
</trajectory>
</case>

<case id="C018">
<trajectory>
input: 전세 들어가려는데 대출 금리 어느 정도야?
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_jeonse_loan_products", "args": {"bank_name_filter": null}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 현재 조회된 전세대출 상품의 금리는 다음과 같습니다.

- NH전세대출(서울보증보험): 연 3.69% ~ 6.39%
- NH전세대출(주택금융공사): 연 3.69% ~ 6.39%
- NH전세대출(주택도시보증공사): 연 3.7% ~ 6.4%

따라서 전세대출 금리는 대략 연 3.69%에서 6.4% 사이로 확인됩니다. 실제 적용 금리는 신용도, 대출 조건 등에 따라 달라질 수 있으니 참고하시기 바랍니다.
</trajectory>
</case>

<case id="C019">
<trajectory>
input: 전세대출 제일 싼 곳 하나만 딱 찍어줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_jeonse_loan_products", "args": {"bank_name_filter": null}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 현재 조회 결과 기준으로 전세대출 금리가 가장 낮은 곳은 농협은행의 NH전세대출(서울보증보험)과 NH전세대출(주택금융공사) 상품으로, 최저 금리가 3.69%입니다.
</trajectory>
</case>

<case id="C020">
<trajectory>
input: 농협 전세대출 금리 보여줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_jeonse_loan_products", "args": {"bank_name_filter": "농협"}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 농협은행의 전세대출 금리는 다음과 같습니다.

- NH전세대출(서울보증보험): 연 3.69% ~ 6.39%
- NH전세대출(주택금융공사): 연 3.69% ~ 6.39%
- NH전세대출(주택도시보증공사): 연 3.7% ~ 6.4%

각 상품별로 금리 범위가 다소 차이가 있으니 참고하시기 바랍니다.
</trajectory>
</case>
