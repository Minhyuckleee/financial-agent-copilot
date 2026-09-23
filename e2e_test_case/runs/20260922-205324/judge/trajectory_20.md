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

<case id="E026">
<trajectory>
input: 예금자보호는 한 사람당 얼마까지 돼?
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "예금자보호제도에 따라 1인당 보호받을 수 있는 예금 금액의 한도는 얼마인지 알려주세요.", "retrieved": [{"source": "(전 분야 마이데이터) 개인정보 전송요구권 제도 안내서(2025.4.).txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}, {"source": "NH농협은행_전자금융서비스이용약관.txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}, {"source": "NH농협은행_전자금융서비스이용약관.txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 문서에서 예금자보호제도에 따라 1인당 보호받을 수 있는 예금 금액의 한도에 대한 내용은 확인할 수 없습니다.
</trajectory>
</case>

<case id="E027">
<trajectory>
input: 요즘 DSR 규제 몇 퍼센트 적용돼?
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "현재 적용 중인 총부채원리금상환비율(DSR) 규제 비율은 몇 퍼센트인지 알려주세요.", "retrieved": [{"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}, {"source": "전자금융감독규정.txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}, {"source": "전자금융감독규정.txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 문서에서는 총부채원리금상환비율(DSR) 규제 비율에 대한 정보가 확인되지 않습니다.
</trajectory>
</case>

<case id="E028">
<trajectory>
input: 아파트 담보대출 LTV 한도 얼마야?
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "아파트를 담보로 하는 주택담보대출의 담보인정비율(LTV) 한도는 얼마인지 알려주세요.", "retrieved": [{"source": "금융소비자보호에관한법률(법률)(제21065호)(20260102)_발췌.txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}, {"source": "금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 해당 문서에서는 아파트를 담보로 하는 주택담보대출의 담보인정비율(LTV) 한도에 대한 내용은 확인할 수 없습니다.
</trajectory>
</case>

<case id="E029">
<trajectory>
input: 고객 홍길동 님 입출금 계좌 잔액 조회해줘
- route_query {"route": "out_of_scope", "rewritten_query": "홍길동 님의 입출금 계좌 잔액을 알려줘."}
- answer_out_of_scope {}
- finalize_answer {}
final output: 죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</trajectory>
</case>

<case id="E030">
<trajectory>
input: 이 고객 신용점수 680점인데 신용대출 승인 나고 한도 얼마까지 될까?
- route_query {"route": "out_of_scope", "rewritten_query": "신용점수가 680점인 이 고객이 신용대출을 신청하면 대출 승인이 날 수 있을까요? 승인이 된다면 최대 얼마까지 대출 한도가 나올 수 있나요?"}
- answer_out_of_scope {}
- finalize_answer {}
final output: 죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</trajectory>
</case>
