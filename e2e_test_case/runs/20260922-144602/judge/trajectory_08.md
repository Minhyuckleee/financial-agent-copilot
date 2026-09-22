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

<case id="C036">
<trajectory>
input: 미국 달러 시세 좀 알려줘
- route_query {"route": "exchange_rate"}
- call_tool {"name": "inquire_exchange_rate", "args": {}, "error": null, "result_count": 1}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 현재 USD/KRW 환율은 1381.0원입니다. (기준일: 2026.09.21)
</trajectory>
</case>

<case id="C037">
<trajectory>
input: 환율 조회해줘, 기준일도 같이
- route_query {"route": "exchange_rate"}
- call_tool {"name": "inquire_exchange_rate", "args": {}, "error": null, "result_count": 1}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 현재 USD/KRW 환율은 1381.0원입니다. (기준일: 2026.09.21)
</trajectory>
</case>

<case id="C038">
<trajectory>
input: 해외여행 가서 달러 환전하려는데 지금 환율 어때?
- route_query {"route": "exchange_rate"}
- call_tool {"name": "inquire_exchange_rate", "args": {}, "error": null, "result_count": 1}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 현재 USD/KRW 환율은 1381.0원입니다. (기준일: 2026.09.21)
</trajectory>
</case>

<case id="C039">
<trajectory>
input: 예금거래기본약관은 고객이 언제 볼 수 있어?
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "예금거래기본약관은 고객이 열람할 수 있는 시점에 관한 규정을 확인하고자 합니다.", "retrieved": [{"source": "예금거래기본약관.txt", "score": null}, {"source": "예금거래기본약관.txt", "score": null}, {"source": "NH농협은행_전자금융서비스이용약관.txt", "score": null}, {"source": "예금거래기본약관.txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 문서에 따르면, 예금거래기본약관은 은행 영업점에 비치되어 있으며, 거래처(고객)는 영업시간 중 언제든지 이 약관을 볼 수 있고, 그 교부를 청구할 수 있습니다. 

따라서, **고객은 영업시간 중 언제든지 예금거래기본약관을 열람할 수 있습니다.**
</trajectory>
</case>

<case id="C040">
<trajectory>
input: 예금거래기본약관에서 통장이나 인감을 잃어버리면 어떻게 하라고 돼 있어?
- route_query {"route": "policy_qa"}
- build_context {"rewritten_query": "예금거래기본약관에서 예금자가 통장 또는 인감을 분실한 경우 취해야 할 조치에 관한 규정을 확인하고 싶습니다.", "retrieved": [{"source": "예금거래기본약관.txt", "score": null}, {"source": "예금거래기본약관.txt", "score": null}, {"source": "예금거래기본약관.txt", "score": null}, {"source": "예금거래기본약관.txt", "score": null}, {"source": "예금거래기본약관.txt", "score": null}]}
- run_guardrail {"guardrail": []}
- finalize_answer {}
final output: 제공해주신 문서의 내용에는 예금자가 통장 또는 인감을 분실한 경우 취해야 할 조치(예: 분실신고, 재발급 절차 등)에 관한 구체적인 규정이 포함되어 있지 않습니다. 따라서 해당 사항에 대해 문서에서 확인할 수 없다고 답변드립니다.
</trajectory>
</case>
