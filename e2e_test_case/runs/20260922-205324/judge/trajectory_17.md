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

<case id="E011">
<trajectory>
input: 주담대 금리는?
history:
사용자: 달러 환율 알려줘
에이전트: 현재 USD/KRW 환율은 1,390원입니다.
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_mortgage_loan_products", "args": {"bank_name_filter": null}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 현재 주택담보대출(주담대) 금리는 은행별로 다음과 같습니다.

- 경남은행 '집집마다 도움대출II': 연 3.7% ~ 5.51%
- 우리은행 '우리아파트론': 연 4.18% ~ 5.28%
- 농협은행 'NH주택담보대출': 연 4.49% ~ 6.29%

은행과 상품에 따라 금리가 다르니 참고하시기 바랍니다.
</trajectory>
</case>

<case id="E012">
<trajectory>
input: 그럼 정기예금 추천해줘
history:
사용자: 예금거래기본약관은 언제 볼 수 있어?
에이전트: 영업점에서 영업시간 중 볼 수 있습니다.
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_deposit_products", "args": {"save_term_months": 12, "bank_name_filter": null}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing", "prohibited_terms"]}
- finalize_answer {}
final output: 현재 가입할 수 있는 정기예금 상품 중에서는 다음과 같은 상품들을 추천드릴 수 있습니다. 1. 광주은행의 '굿스타트예금'은 12개월 만기에 기본 금리 3.45%, 우대금리 적용 시 최대 3.95%의 금리를 제공합니다. 2. 부산은행의 '더(The) 특판 정기예금'은 12개월 만기에 기본 금리 2.1%, 우대금리 적용 시 최대 3.92%의 금리를 받을 수 있습니다. 3. 농협은행의 'NH왈츠회전예금 II'는 12개월 만기에 기본 금리 3.35%, 우대금리 적용 시 최대 3.45%입니다. 각 상품의 우대금리 조건을 확인하신 후 본인에게 맞는 상품을 선택하시면 좋겠습니다. ※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="E013">
<trajectory>
input: 왜 그래요?
history:
사용자: 금융상품 설명의무는 뭘 설명해야 하나요?
에이전트: 일반금융소비자에게 중요사항을 이해할 수 있도록 설명해야 합니다.
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "금융상품 판매자는 일반금융소비자가 금융상품의 중요사항을 충분히 이해할 수 있도록 설명할 의무가 있는 이유에 관하여 규정한 조항을 확인하고 싶습니다.", "retrieved": [{"source": "온라인 설명의무 가이드라인.txt", "score": null}, {"source": "온라인 설명의무 가이드라인.txt", "score": null}, {"source": "온라인 설명의무 가이드라인.txt", "score": null}, {"source": "온라인 설명의무 가이드라인.txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 문서에 따르면, 금융상품 판매자가 일반금융소비자가 금융상품의 중요사항을 충분히 이해할 수 있도록 설명할 의무가 있는 이유는 **금융소비자보호법 제19조제1항**에 근거하고 있습니다.

문서의 관련 내용은 다음과 같습니다:

- "금융상품판매업자등은 금융소비자가 금융소비자보호법 제19조제1항에 따른 금융상품의 중요한 사항을 명확하게 인식할 수 있도록 제시합니다."
- "금융소비자보호법상 설명의무는 중요한 사항 설명, 설명한 사항에 대한 이해 여부 확인으로 이루어지며..."

따라서, **금융소비자보호법 제19조제1항**이 해당 의무의 근거 조항임을 문서에서 확인할 수 있습니다.
</trajectory>
</case>

<case id="E014">
<trajectory>
input: 다른 것도 있어?
history:
사용자: 정기예금 추천해줘
에이전트: 12개월 기준 정기예금 상품 3건을 안내드립니다.
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_credit_loan_products", "args": {}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 현재 조회 결과에는 농협은행의 '가계신용대출(마이너스대출)', 하나은행의 '마이너스한도대출', 우리은행의 '협약금리 外 신용대출상품' 이렇게 세 가지 마이너스한도대출 상품만 확인됩니다. 이 외의 다른 상품 정보는 조회 결과에 포함되어 있지 않습니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="E015">
<trajectory>
input: 어떻게 신청하나요?
history:
사용자: 신용점수 800점 신용대출 추천해줘
에이전트: 신용점수 800점 기준 신용대출 상품 3건을 안내드립니다.
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_credit_loan_products", "args": {"credit_score": 800}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 조회 결과에는 각 은행의 마이너스한도대출 상품 정보(금리, 신용점수 구간 등)만 제공되어 있고, 구체적인 신청 방법에 대한 내용은 포함되어 있지 않습니다.  
신청 방법에 대해 더 자세히 알고 싶으시다면 해당 은행(하나은행, 국민은행, 농협은행)의 공식 홈페이지나 가까운 영업점을 통해 안내를 받으시는 것이 좋습니다.
</trajectory>
</case>
