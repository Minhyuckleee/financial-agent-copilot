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

<case id="C026">
<trajectory>
input: 기업은행 주택담보대출 금리 얼마야?
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_mortgage_loan_products", "args": {"bank_name_filter": "기업은행"}, "error": null, "result_count": 1}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 기업은행(중소기업은행)의 IBK주택담보대출 금리는 4.89%입니다.
</trajectory>
</case>

<case id="C027">
<trajectory>
input: 개인사업자대출 금리 낮은 곳 알려줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_business_loan_products", "args": {}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["prohibited_terms"]}
- finalize_answer {}
final output: 그 다음으로는 우리은행의 '우리상생파트너론'(4.85%), '우리CUBE론-X(일반,산업단지)'(4.95%)가 있습니다.
</trajectory>
</case>

<case id="C028">
<trajectory>
input: 신용점수 800점 개인사업자인데 대출 금리 어디가 낮아?
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_business_loan_products", "args": {"credit_score": 800}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["prohibited_terms"]}
- finalize_answer {}
final output: 조회 결과에 따르면, 신용점수 800점인 개인사업자에게 적용되는 대출 금리는 우리은행의 B2B 대출과 우리 지역선도기업 대출이 각각 연 4.85%로 가장 낮습니다. 우리 첨단선도기업대출은 연 4.86%입니다.
</trajectory>
</case>

<case id="C029">
<trajectory>
input: 국민은행 개인사업자대출 상품 있어?
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_business_loan_products", "args": {"bank_name_filter": "국민은행"}, "error": "empty_result"}
- call_tool {"name": "recommend_business_loan_products", "args": {"bank_name_filter": "국민"}, "error": "empty_result"}
- answer_tier2_exhausted {"low_confidence": true}
- finalize_answer {}
final output: 국민은행의 개인사업자대출 상품은 현재 조회 결과가 없습니다.

※ 이 조건으로는 충분히 찾지 못해, 확인된 정보만 안내드립니다.
</trajectory>
</case>

<case id="C030">
<trajectory>
input: 자영업자 대출 금리 비교해줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_business_loan_products", "args": {}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 현재 601~700점 신용점수 구간에서 자영업자 대출 금리는 다음과 같이 비교할 수 있습니다.

- 제주은행의 'JJB가맹점우대론' : 연 4.46%
- 우리은행의 '우리상생파트너론' : 연 4.85%
- 우리은행의 '우리CUBE론-X(일반,산업단지)' : 연 4.95%

따라서, 같은 신용점수 구간에서는 제주은행의 'JJB가맹점우대론'이 가장 낮은 금리(4.46%)를 제공합니다.
</trajectory>
</case>
