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

<case id="C011">
<trajectory>
input: 카카오뱅크 신용대출 금리 알려줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_credit_loan_products", "args": {"bank_name_filter": "카카오뱅크"}, "error": null, "result_count": 2}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 카카오뱅크의 신용대출 금리는 신용점수 601~700점 기준으로 일반신용대출은 연 7.93%, 마이너스한도대출은 연 8.65%입니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="C012">
<trajectory>
input: 신한은행에서 신용점수 750점으로 신용대출 받으면 금리 얼마야?
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_credit_loan_products", "args": {"credit_score": 750, "bank_name_filter": "신한"}, "error": null, "result_count": 2}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 신한은행에서 신용점수 750점으로 신용대출을 받으실 경우,  
- 마이너스한도대출(마통)은 금리가 6.52%이고,  
- 일반신용대출은 금리가 7.36%입니다.  

두 상품 모두 신용점수 701~800점 구간에 해당하는 금리입니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="C013">
<trajectory>
input: 직장인 신용대출 금리 비교해줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_credit_loan_products", "args": {}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 직장인 신용대출 금리를 비교해드리면, 신용점수 601~700점 기준으로

- 농협은행의 '가계신용대출(마이너스대출)'은 금리가 5.72%
- 하나은행의 '마이너스한도대출'은 금리가 6.12%
- 우리은행의 '협약금리 외 신용대출상품'은 금리가 6.22%

입니다. 각 은행별로 금리 차이가 있으니 참고하시기 바랍니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="C014">
<trajectory>
input: 마이너스통장 금리 낮은 은행 어디야?
- route_query {"route": "out_of_scope", "rewritten_query": "마이너스통장 금리가 가장 낮은 은행이 어디인지 알려줘."}
- answer_out_of_scope {}
- finalize_answer {}
final output: 죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</trajectory>
</case>

<case id="C015">
<trajectory>
input: 전세자금대출 금리 낮은 데 알려줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_jeonse_loan_products", "args": {"bank_name_filter": null}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["prohibited_terms"]}
- finalize_answer {}
final output: 참고로, 'NH전세대출(주택도시보증공사)' 상품의 최저 금리는 3.7%입니다.
</trajectory>
</case>
