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

<case id="E006">
<trajectory>
input: 하나은행 걸로 보여줘
history:
사용자: 6개월 정기예금 추천해줘
에이전트: 6개월 기준 정기예금 상품 3건을 안내드립니다.
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_deposit_products", "args": {"save_term_months": 6, "bank_name_filter": "하나"}, "error": null, "result_count": 1}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 하나은행의 예금 상품으로는 '하나의정기예금'이 있습니다. 6개월 만기 기준 기본 금리는 연 2.25%이고, 우대금리를 포함하면 최대 연 3.3%까지 적용됩니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="E007">
<trajectory>
input: 개인사업자대출도 같은 점수로 봐줘
history:
사용자: 신용점수 650점 신용대출 알려줘
에이전트: 신용점수 650점 기준 신용대출 상품 3건을 안내드립니다.
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_business_loan_products", "args": {"credit_score": 650}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 601~700점 신용점수 기준으로 조회된 개인사업자대출 상품은 다음과 같습니다.

- 제주은행의 JJB가맹점우대론: 금리 4.46%
- 우리은행의 우리상생파트너론: 금리 4.85%
- 우리은행의 우리CUBE론-X(일반,산업단지): 금리 4.95%

위 상품들이 해당 신용점수 구간에서 이용 가능한 대출 상품입니다.
</trajectory>
</case>

<case id="E008">
<trajectory>
input: 전세대출은?
history:
사용자: 농협 주택담보대출 금리 알려줘
에이전트: 농협 주택담보대출 상품을 안내드립니다.
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_jeonse_loan_products", "args": {"bank_name_filter": "농협"}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 전세대출 상품으로는 농협은행에서 제공하는 다음과 같은 상품들이 있습니다.

1. NH전세대출(서울보증보험): 금리는 연 3.69%에서 6.39% 사이입니다.
2. NH전세대출(주택금융공사): 금리는 연 3.69%에서 6.39% 사이입니다.
3. NH전세대출(주택도시보증공사): 금리는 연 3.7%에서 6.4% 사이입니다.

각 상품의 금리는 조건에 따라 달라질 수 있습니다.
</trajectory>
</case>

<case id="E009">
<trajectory>
input: 환율도 알려줘
history:
사용자: 정기예금 추천해줘
에이전트: 12개월 기준 정기예금 상품 3건을 안내드립니다.
- route_query {"route": "exchange_rate"}
- call_tool {"name": "inquire_exchange_rate", "args": {}, "error": null, "result_count": 1}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 현재 USD/KRW 환율은 1358.2원입니다. (기준일: 2026.09.22)
</trajectory>
</case>

<case id="E010">
<trajectory>
input: 그런데 개인정보 수집 동의는 어떻게 받아야 해?
history:
사용자: 신용대출 금리 낮은 곳 알려줘
에이전트: 신용대출 상품 3건을 안내드립니다.
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "신용대출 상품 안내를 위해 개인정보를 수집할 때 필요한 동의 절차에 관하여 규정한 조항을 확인하고 싶습니다.", "retrieved": [{"source": "개인정보 질의응답 모음집.txt", "score": null}, {"source": "신용정보의 이용 및 보호에 관한 법률(법률)(제20304호)(20240814).txt", "score": null}, {"source": "개인정보 질의응답 모음집.txt", "score": null}, {"source": "신용정보의 이용 및 보호에 관한 법률(법률)(제20304호)(20240814).txt", "score": null}, {"source": "개인정보 처리방침 작성지침(2025.4.).txt", "score": null}, {"source": "개인정보 보호 법령 및 지침, 고시 해설서(2020.12).txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 문서에서 신용대출 상품 안내를 위해 개인정보를 수집할 때 필요한 동의 절차에 관하여 규정한 조항은 다음과 같습니다.

### 관련 법령 및 조항

#### 1. 개인정보 보호법 제15조, 제22조
- 개인정보를 수집하려면 보호법 제15조 제1항 각 호에 해당하는 경우에만 수집·이용할 수 있습니다.
- 제1호(정보주체 동의)에 따라 동의를 받는 경우, 동의 사항을 구분하고 중요한 내용을 명확히 표시하여 정보주체가 명확히 인지할 수 있도록 해야 합니다(제22조 제1항).
- 개인정보 수집 목적, 항목 등을 구체적으로 밝히고, 약관과 별도로 설명하여 자발적으로 동의 여부를 결정하도록 해야 합니다.

#### 2. 신용정보의 이용 및 보호에 관한 법률 제34조의2(개인신용정보 등의 활용에 관한 동의의 원칙)
- 신용정보회사 등은 신용정보주체로부터 동의를 받을 때, 개인정보 보호법 제15조제2항, 제17조제2항 및 제18조제3항에 따라 고지사항을 알리고 동의를 받아야 합니다.
- 동의 사항과 금융거래 등 상거래관계의 설정 및 유지 등에 관한 사항이 명확하게 구분되도록 해야 하며, 정보활용의 목적별로 동의 사항을 구분하여 개별적으로 동의할 수 있도록 해야 합니다.
- 보다 쉬운 용어나 시청각적 전달 수단을 사용하여 정보주체가 동의 사항을 이해할 수 있도록 해야 합니다.

#### 3. 예외 및 추가사항
- 개별법(예: 위치정보법 등)에서 약관에 필수항목을 기재한 후 동의를 받도록 특별한 명시적 규정이 있는 경우에는 그 절차와 방법에 따라야 합니다.
- 필요한 범위에서 최소한의 개인정보만 수집해야 하며, 약관에 부당하게 불리한 조항이 있으면 무효가 될 수 있습니다.

---

**요약:**  
신용대출 상품 안내를 위해 개인정보를 수집할 때는,  
- 개인정보 보호법 및 신용정보법에 따라 동의 사항을 명확히 구분·고지하고,  
- 정보주체가 자발적으로 동의 여부를 결정할 수 있도록 해야 하며,  
- 동의는 약관과 별도로 받아야 하고,  
- 동의 절차와 고지사항, 동의 방식 등은 법령에서 정한 절차를 따라야 합니다.

**관련 조항:**  
- 개인정보 보호법 제15조, 제22조  
- 신용정보의 이용 및 보호에 관한 법률 제34조의2

문서에서 위 조항들을 확인할 수 있습니다.
</trajectory>
</case>
