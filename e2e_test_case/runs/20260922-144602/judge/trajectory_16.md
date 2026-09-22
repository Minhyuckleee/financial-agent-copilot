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
final output: 하나은행의 예금 상품으로는 '하나의정기예금'이 있습니다. 6개월 만기 기준으로 기본 금리는 연 2.25%이고, 우대금리를 포함하면 최대 연 3.3%까지 적용됩니다.

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
- run_guardrail {"guardrail": ["numeric_self_check"]}
- finalize_answer {}
final output: 601~700점 신용점수 기준으로 조회된 개인사업자대출 상품은 다음과 같습니다.

- 제주은행의 JJB가맹점우대론: 금리 4.46%
- 우리은행의 우리상생파트너론: 금리 4.95%
- 우리은행의 우리CUBE론-X(일반, 산업단지): 금리 4.95%

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

1. NH전세대출(서울보증보험): 금리는 연 3.69%에서 6.39%입니다.
2. NH전세대출(주택금융공사): 금리는 연 3.69%에서 6.39%입니다.
3. NH전세대출(주택도시보증공사): 금리는 연 3.7%에서 6.4%입니다.

각 상품별로 보증기관이 다르며, 금리는 상품과 조건에 따라 달라질 수 있습니다.
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
final output: 현재 USD/KRW 환율은 1381.0원입니다. (기준일: 2026.09.21)
</trajectory>
</case>

<case id="E010">
<trajectory>
input: 그런데 개인정보 수집 동의는 어떻게 받아야 해?
history:
사용자: 신용대출 금리 낮은 곳 알려줘
에이전트: 신용대출 상품 3건을 안내드립니다.
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "신용대출 상품 안내를 위해 개인정보를 수집할 때 동의 절차는 어떠한 방식으로 진행하여야 하는지에 관한 규정을 알려주세요.", "retrieved": [{"source": "개인정보 질의응답 모음집.txt", "score": null}, {"source": "신용정보의 이용 및 보호에 관한 법률(법률)(제20304호)(20240814).txt", "score": null}, {"source": "신용정보의 이용 및 보호에 관한 법률(법률)(제20304호)(20240814).txt", "score": null}, {"source": "신용정보의 이용 및 보호에 관한 법률(법률)(제20304호)(20240814).txt", "score": null}, {"source": "개인정보 보호 법령 및 지침, 고시 해설서(2020.12).txt", "score": null}, {"source": "신용정보의 이용 및 보호에 관한 법률(법률)(제20304호)(20240814).txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 문서에 따르면, 신용대출 상품 안내를 위해 개인정보(예: 휴대전화번호 등)를 수집할 때 동의 절차는 다음과 같이 진행해야 합니다.

1. **동의 사항의 명확한 고지 및 구분**  
   - 개인정보를 수집·이용할 때에는  
     - 개인정보의 수집·이용 목적  
     - 수집하려는 개인정보의 항목  
     - 개인정보의 보유 및 이용 기간  
   등을 정보주체(고객)에게 명확히 알려야 합니다.  
   - 만약 제3자 제공이 있다면  
     - 개인정보를 제공받는 자  
     - 제공받는 자의 이용 목적  
     - 제공하는 개인정보의 항목  
     - 제공받는 자의 보유 및 이용 기간  
   등을 구분하여 고지해야 합니다.  
   - 각각의 동의 사항(수집·이용, 제3자 제공 등)을 구분하여 정보주체가 명확히 인지할 수 있도록 알리고, 각 사항별로 동의를 받아야 합니다.  
   - 개인정보 처리방침에 대한 포괄적 동의로는 개별 동의를 갈음할 수 없습니다.

2. **홍보·마케팅 목적의 별도 동의**  
   - 신용대출 상품 안내(홍보 또는 판매권유 목적)로 개인정보를 이용하려면,  
     - 해당 목적(홍보·마케팅 등)을 명확히 알리고  
     - 별도로 정보주체의 동의를 받아야 합니다.  
   - 이 동의는 다른 개인정보 수집·이용 동의, 제3자 제공 동의, 민감정보 처리 동의 등과 각각 구분하여 받아야 합니다.

3. **동의 방식**  
   - 동의는 서면, 전자서명, 비밀번호 입력, 음성녹음 등 대통령령으로 정하는 방식 중 하나로 받아야 하며,  
   - 동의의 안정성과 신뢰성이 확보될 수 있어야 합니다(신용정보법 제32조 참조).

4. **선택적 동의와 필수적 동의의 구분**  
   - 서비스 제공에 필수적인 동의사항과 선택적 동의사항을 구분하여 설명하고, 각각 동의를 받아야 합니다.  
   - 선택적 동의사항에 동의하지 않았다는 이유로 서비스 제공을 거부해서는 안 됩니다.

**요약**  
신용대출 상품 안내를 위한 개인정보 수집 시에는  
- 수집·이용 목적, 항목, 보유·이용 기간 등 필수사항을 명확히 고지하고  
- 홍보·마케팅 목적임을 별도로 알린 후  
- 각 동의사항별로 구분하여 명확하게 동의를 받아야 하며  
- 동의 방식은 법령에서 정한 안전한 방법을 사용해야 합니다.

(출처: 문서 Page 83, 84, 27 등)
</trajectory>
</case>
