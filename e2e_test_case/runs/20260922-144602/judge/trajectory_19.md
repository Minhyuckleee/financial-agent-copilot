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

<case id="E021">
<trajectory>
input: 전세대출 말고 주담대 금리만 보여줘
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_mortgage_loan_products", "args": {"bank_name_filter": null}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 주택담보대출(주담대) 금리는 다음과 같습니다.

- 경남은행: 집집마다 도움대출II, 금리 3.7% ~ 5.51%
- 우리은행: 우리아파트론, 금리 4.18% ~ 5.28%
- 농협은행: NH주택담보대출, 금리 4.49% ~ 6.29%

전세대출 금리는 포함하지 않았습니다.
</trajectory>
</case>

<case id="E022">
<trajectory>
input: 개인사업자인데 대출 좀 알아보고 있어요
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_business_loan_products", "args": {"credit_score": 700}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["numeric_self_check"]}
- finalize_answer {}
final output: 현재 조회된 결과를 바탕으로, 개인사업자 분이 이용하실 수 있는 대출 상품은 다음과 같습니다.

1. 제주은행의 'JJB가맹점우대론' 상품이 있으며, 신용점수 601~700점 구간에서 금리는 연 4.46%입니다.
2. 우리은행의 '우리상생파트너론' 상품은 신용점수 601~700점 구간에서 연 4.95% 금리로 제공됩니다.
3. 우리은행의 '우리CUBE론-X(일반,산업단지)' 상품도 신용점수 601~700점 구간에서 연 4.95% 금리로 이용하실 수 있습니다.

각 상품의 세부 조건이나 한도, 필요 서류 등은 해당 은행에 문의하시면 더 자세히 안내받으실 수 있습니다.
</trajectory>
</case>

<case id="E023">
<trajectory>
input: 월세 보증금 대출 금리 알려줘
- route_query {"route": "out_of_scope", "rewritten_query": "월세 보증금 대출의 현재 금리를 알려줘."}
- answer_out_of_scope {}
- finalize_answer {}
final output: 죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</trajectory>
</case>

<case id="E024">
<trajectory>
input: 사업도 하긴 하는데 이번엔 개인 신용대출로 알아볼래
- route_query {"route": "product_recommendation"}
- call_tool {"name": "recommend_credit_loan_products", "args": {}, "error": null, "result_count": 3}
- run_guardrail {"guardrail": ["disclosure_missing"]}
- finalize_answer {}
final output: 현재 조회된 결과를 보면, 사업을 하시더라도 이번에는 개인 신용대출(마이너스한도대출)로 알아보실 수 있습니다. 신용점수 601~700점 구간 기준으로,

- 농협은행의 '가계신용대출(마이너스대출)'은 금리가 5.72%,
- 하나은행의 '마이너스한도대출'은 금리가 6.12%,
- 우리은행의 '협약금리 外 신용대출상품'은 금리가 6.22%

로 확인됩니다.

각 은행별로 금리와 조건이 다르니, 본인 상황에 맞게 비교해보시고 선택하시면 좋겠습니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</trajectory>
</case>

<case id="E025">
<trajectory>
input: 대출 금리인하요구권은 어떤 조건일 때 쓸 수 있어?
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "대출 금리인하요구권을 행사할 수 있는 조건에 대해 설명한 조항을 확인하고 싶습니다.", "retrieved": [{"source": "온라인 설명의무 가이드라인.txt", "score": null}, {"source": "신용정보의 이용 및 보호에 관한 법률(법률)(제20304호)(20240814).txt", "score": null}, {"source": "온라인 설명의무 가이드라인.txt", "score": null}, {"source": "신용정보의 이용 및 보호에 관한 법률(법률)(제20304호)(20240814).txt", "score": null}, {"source": "온라인 설명의무 가이드라인.txt", "score": null}, {"source": "신용정보의 이용 및 보호에 관한 법률(법률)(제20304호)(20240814).txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 문서 내에는 "대출 금리인하요구권을 행사할 수 있는 조건"에 대해 설명한 조항이나 내용이 포함되어 있지 않습니다.  
따라서 해당 조건에 대해 문서에서 확인할 수 없습니다.
</trajectory>
</case>
