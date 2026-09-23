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

<case id="C031">
<trajectory>
input: 농협에서 신용점수 650점 사업자대출 금리 알려줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_business_loan_products", "args": {"credit_score": 650, "bank_name_filter": "농협"}, "error": "empty_result"}
- call_tool {"name": "recommend_business_loan_products", "args": {"credit_score": 650}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 농협에서 신용점수 650점으로 받을 수 있는 사업자대출 금리는 조회 결과 확인되지 않았습니다. 대신, 신용점수 650점(601~700점 구간)에 해당하는 다른 은행의 사업자대출 금리를 안내해 드리면 다음과 같습니다.

- 제주은행 JJB가맹점우대론: 연 4.46%
- 우리은행 우리상생파트너론: 연 4.85%
- 우리은행 우리CUBE론-X(일반,산업단지): 연 4.95%

참고로, 처음에는 농협에 한정해서 조회했으나 결과가 없어 조건을 넓혀 안내드리는 점 양해 부탁드립니다.
</trajectory>
</case>

<case id="C032">
<trajectory>
input: 가게 운영자금 대출 알아보는데 금리 낮은 데 있어?
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_business_loan_products", "args": {"credit_score": 700}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["prohibited_terms"]}
- finalize_answer {}
final output: 현재 조회 결과 기준으로, 가게 운영자금 대출 중에서는 제주은행의 'JJB가맹점우대론'이 4.46%로 가장 낮은 금리를 제공하고 있습니다. 그 외에 우리은행의 '우리상생파트너론'(4.85%)과 '우리CUBE론-X(일반,산업단지)'(4.95%)가 있습니다.
</trajectory>
</case>

<case id="C033">
<trajectory>
input: 환율 알려줘
- route_query {"route": "exchange_rate"}
- call_tool {"name": "inquire_exchange_rate", "args": {}, "error": null, "result_count": 1}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 현재 USD/KRW 환율은 1358.2원입니다. (기준일: 2026.09.22)
</trajectory>
</case>

<case id="C034">
<trajectory>
input: 달러 환율 얼마야?
- route_query {"route": "exchange_rate"}
- call_tool {"name": "inquire_exchange_rate", "args": {}, "error": null, "result_count": 1}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 현재 USD/KRW 환율은 1358.2원입니다. (기준일: 2026.09.22)
</trajectory>
</case>

<case id="C035">
<trajectory>
input: 지금 원달러 몇 원이야?
- route_query {"route": "exchange_rate"}
- call_tool {"name": "inquire_exchange_rate", "args": {}, "error": null, "result_count": 1}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 현재 USD/KRW 환율은 1358.2원입니다. (기준일: 2026.09.22)
</trajectory>
</case>
