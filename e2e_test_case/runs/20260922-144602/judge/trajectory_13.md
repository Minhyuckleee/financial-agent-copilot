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

<case id="C061">
<trajectory>
input: 오늘 서울 날씨 어때?
- route_query {"route": "out_of_scope", "rewritten_query": "오늘 서울의 날씨 정보를 알려줄 수 있나요?"}
- answer_out_of_scope {}
- finalize_answer {}
final output: 죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</trajectory>
</case>

<case id="C062">
<trajectory>
input: 삼성전자 주가 앞으로 오를까?
- route_query {"route": "out_of_scope", "rewritten_query": "삼성전자 주가가 앞으로 상승할 가능성이 있을지 궁금합니다."}
- answer_out_of_scope {}
- finalize_answer {}
final output: 죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</trajectory>
</case>

<case id="C063">
<trajectory>
input: 비트코인 지금 사도 돼?
- route_query {"route": "out_of_scope", "rewritten_query": "지금 비트코인을 매수해도 괜찮을까요?"}
- answer_out_of_scope {}
- finalize_answer {}
final output: 죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</trajectory>
</case>

<case id="C064">
<trajectory>
input: 파이썬으로 리스트 정렬하는 코드 짜줘
- route_query {"route": "out_of_scope", "rewritten_query": "파이썬으로 숫자로 이루어진 리스트를 오름차순으로 정렬하는 코드를 작성해줘."}
- answer_out_of_scope {}
- finalize_answer {}
final output: 죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</trajectory>
</case>

<case id="C065">
<trajectory>
input: 이번 휴가 때 갈 만한 여행지 추천해줘
- route_query {"route": "out_of_scope", "rewritten_query": "이번 휴가 때 내가 갈 수 있는 국내 여행지를 추천해줘."}
- answer_out_of_scope {}
- finalize_answer {}
final output: 죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</trajectory>
</case>
