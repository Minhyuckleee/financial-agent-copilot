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
final output: 현재 가입할 수 있는 정기예금 상품 중에서는 다음과 같은 상품들을 추천드릴 수 있습니다. 1. 광주은행의 '굿스타트예금' - 가입 기간: 12개월 - 기본 금리: 연 3.45% - 우대 금리 적용 시: 최대 연 3.95% 2. 부산은행의 '더(The) 특판 정기예금' - 가입 기간: 12개월 - 기본 금리: 연 2.1% - 우대 금리 적용 시: 최대 연 3.92% 3. 농협은행의 'NH왈츠회전예금 II' - 가입 기간: 12개월 - 기본 금리: 연 3.35% - 우대 금리 적용 시: 최대 연 3.45% 이 중에서는 광주은행의 '굿스타트예금'이 우대 금리 기준으로 가장 높은 연 3.95%를 제공합니다. ※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="E013">
<trajectory>
input: 왜 그래요?
history:
사용자: 금융상품 설명의무는 뭘 설명해야 하나요?
에이전트: 일반금융소비자에게 중요사항을 이해할 수 있도록 설명해야 합니다.
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "금융회사가 일반금융소비자에게 중요사항을 이해할 수 있도록 설명하여야 하는 법적 근거 및 그 취지를 설명한 조항을 제시해 주세요.", "retrieved": [{"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}, {"source": "온라인 설명의무 가이드라인.txt", "score": null}, {"source": "온라인 설명의무 가이드라인.txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 문서에 따르면, 금융회사가 일반금융소비자에게 중요사항을 이해할 수 있도록 설명하여야 하는 법적 근거 및 그 취지를 설명한 조항은 다음과 같습니다.

---

### 1. 법적 근거

#### 금융소비자보호법 제19조제1항  
(문서 Page 2, 파트 1. 금융상품 설명화면 구성, 원칙 ❶)
> 금융상품판매업자등은 금융소비자가 금융소비자보호법 제19조제1항에 따른 금융상품의 중요한 사항을 명확하게 인식할 수 있도록 제시합니다.

#### 약관의 규제에 관한 법률(약관규제법) 제3조제3항  
(문서 Page 8)
> 제3조(약관의 작성 및 설명의무 등) ③ 사업자는 약관에 정하여져 있는 중요한 내용을 고객이 이해할 수 있도록 설명하여야 한다. 다만, 계약의 성질상 설명하는 것이 현저하게 곤란한 경우에는 그러하지 아니하다.

---

### 2. 취지

(문서 Page 2)
> 금융소비자가 금융상품의 중요한 사항을 설명받고 있다고 인식할 수 있도록 화면에 명확하게 표시합니다.  
> 금융소비자의 합리적인 금융상품 구매결정에 도움이 되는 사항을 우선하여 제공합니다.

(문서 Page 8)
> 금융소비자보호법상 중요 설명사항으로 열거되지 않더라도 약관상 중요한 내용*은 소비자가 이해하기 쉽게 설명해야 함

---

**요약:**  
- **금융소비자보호법 제19조제1항** 및 **약관규제법 제3조제3항**이 법적 근거입니다.
- 그 취지는 금융소비자가 금융상품의 중요한 사항을 명확히 인식하고, 합리적인 구매결정을 할 수 있도록 정보를 이해하기 쉽게 제공하는 데 있습니다.
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
final output: 네, 다른 상품도 있습니다.  
현재 601~700점 신용점수 구간에서 마이너스한도대출로는 다음과 같은 상품들이 조회되었습니다:

- 농협은행주식회사의 '가계신용대출(마이너스대출)'(금리 5.72%)
- 주식회사 하나은행의 '마이너스한도대출'(금리 6.12%)
- 우리은행의 '협약금리 外 신용대출상품'(금리 6.22%)

이 외의 상품 정보는 조회 결과에 없습니다.

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
final output: 조회 결과에 따르면, 주식회사 하나은행, 국민은행, 농협은행주식회사에서 마이너스한도대출 상품을 제공하고 있습니다. 각 은행의 대출 상품에 신청하려면 해당 은행의 영업점 방문, 인터넷뱅킹, 모바일 앱 등 공식 채널을 통해 신청하실 수 있습니다. 구체적인 신청 방법과 필요 서류는 각 은행의 홈페이지나 고객센터를 통해 확인하시는 것이 좋습니다.
</trajectory>
</case>
