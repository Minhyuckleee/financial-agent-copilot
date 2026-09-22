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

<case id="C006">
<trajectory>
input: 목돈 맡기려는데 이자 많이 주는 예금 어디야?
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_deposit_products", "args": {"save_term_months": 12}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing", "prohibited_terms"]}
- finalize_answer {}
final output: 현재 1년(12개월) 기준으로 이자를 많이 주는 예금 상품은 다음과 같습니다. ※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="C007">
<trajectory>
input: 1년 만기 예금 중에 우대금리 높은 거 알려줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_deposit_products", "args": {"save_term_months": 12}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing", "prohibited_terms"]}
- finalize_answer {}
final output: 그 다음으로는 부산은행의 '더(The) 특판 정기예금'이 3.92%, 농협은행의 'NH왈츠회전예금 II'가 3.45%의 우대금리를 제공합니다. ※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="C008">
<trajectory>
input: 신용대출 금리 낮은 곳 추천해줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_credit_loan_products", "args": {}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 현재 조회된 결과 중 신용점수 601~700점 기준으로 신용대출 금리가 가장 낮은 곳은 농협은행주식회사의 '가계신용대출(마이너스대출)'로, 금리는 5.72%입니다.  
다음으로 하나은행(6.12%), 우리은행(6.22%) 순으로 금리가 높으니 참고하시면 좋겠습니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="C009">
<trajectory>
input: 신용점수 900점이면 신용대출 어디가 싸?
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_credit_loan_products", "args": {"credit_score": 900}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing", "prohibited_terms"]}
- finalize_answer {}
final output: 신용점수가 900점일 경우, 조회 결과 기준으로 가장 낮은 금리의 신용대출 상품은 수협은행의 '개인신용대출'(일반신용대출)로, 금리는 5.18%입니다. 그 다음으로는 아이엠뱅크의 '장기카드대출'(카드론)이 5.19%, 농협은행의 '가계신용대출(마이너스대출)'이 5.7%입니다. ※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="C010">
<trajectory>
input: 신용점수 600점대 초반인데 받을 수 있는 신용대출 금리 알려줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_credit_loan_products", "args": {"credit_score": 600}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 신용점수가 600점대 초반이라면, 받을 수 있는 신용대출 금리는 다음과 같습니다.

- 우리은행: 연 7.25%
- 신한은행: 연 7.45%
- 농협은행: 연 8.1%

위 금리는 모두 신용점수 501~600점 구간에 해당하는 일반신용대출 상품 기준입니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>
