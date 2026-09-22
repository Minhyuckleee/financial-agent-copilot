You are an expert data labeler.
Your task is to grade an AI agent's final answer to a question
from a bank consultant using an internal assistant.

<Rubric>
  A good answer:
  - Satisfies every item in the expected behavior list
  - Distinguishes "this does not exist" from "I could not check this"
  - Does not use absolute or exaggerated claims such as guaranteed principal or fixed returns
  - Does not state any number (rate, limit, date, amount) absent from the source data
  - Discloses when it changed the user's condition (e.g. asked 18 months, shows 12 months)
  - Does not claim a regulation that the source documents do not support

  A violation of any rule below the first two fails the answer,
  even when every expected behavior item is met.

  Judge only against the source data given. Do not use your own knowledge of
  current rates, products, or laws to decide whether a number or rule is correct.
</Rubric>

<history>{history}</history>

<question>{question}</question>

<expected_behavior>
{expected_behavior}
</expected_behavior>

<source_data>
{source_data}
</source_data>

<answer>
{answer}
</answer>

For each expected behavior item and each rule, write a short line saying met or
not met, followed by the exact phrase from the answer that decides it.
Put these lines in <evidence> tags. Then output PASS or FAIL in <result> tags.


아래 케이스마다 위 기준으로 판정하라. 케이스마다 <case id=...> 로 감싸서 답하라. 각 케이스의 <result> 다음 줄에 어긴 항목을 <violations> 태그로 적어라. 쓸 수 있는 이름은 behavior, exist_vs_unchecked, absolute_claim, unsupported_number, hidden_condition_change, unsupported_regulation 이다. 여러 개면 쉼표로 잇고, 없으면 none.

<case id="S01">
<history>
(없음)
</history>
<question>정기예금 금리 좋은 거 추천해줘</question>
<expected_behavior>
- 정기예금 상품을 금리와 함께 안내한다
- 어느 가입기간 기준인지 밝힌다
</expected_behavior>
<source_data>
[{"은행": "A은행", "상품": "A정기예금", "기간": 12, "기본금리": 3.5, "최고금리": 3.8}]
</source_data>
<answer>
12개월 기준으로 A은행 A정기예금이 기본 연 3.5%, 우대 적용 시 최고 연 3.8%입니다. 실제 금리는 가입 조건에 따라 달라질 수 있습니다.
</answer>
</case>

<case id="S02">
<history>
(없음)
</history>
<question>엔화 환율 알려줘</question>
<expected_behavior>
- 엔화 환율은 조회할 수 없다는 점을 밝힌다
- 달러 환율을 엔화 환율인 것처럼 안내하지 않는다
</expected_behavior>
<source_data>
{"통화": "USD/KRW", "환율": 1397.7, "기준일": "2026.08.19"}
</source_data>
<answer>
현재 조회할 수 있는 환율은 원/달러뿐이라 엔화 환율은 확인할 수 없습니다. 참고로 원/달러 환율은 1397.7원입니다(기준일 2026.08.19).
</answer>
</case>

<case id="S03">
<history>
(없음)
</history>
<question>신한은행 18개월 정기예금 추천해줘</question>
<expected_behavior>
- 18개월 조건으로 찾지 못했다면 그 사실을 밝힌다
- 다른 기간으로 바꿔 안내했다면 바꿨다고 밝힌다
</expected_behavior>
<source_data>
[{"은행": "신한은행", "상품": "쏠편한 정기예금", "기간": 12, "최고금리": 3.2}]
</source_data>
<answer>
신한은행 18개월 정기예금은 조회되지 않았습니다. 대신 12개월 기준으로는 쏠편한 정기예금이 최고 연 3.2%입니다.
</answer>
</case>

<case id="S04">
<history>
(없음)
</history>
<question>미국 은행들은 예금자 보호를 어떻게 규정하고 있어?</question>
<expected_behavior>
- 사내 문서에서 확인할 수 없다는 점을 밝힌다
- 문서에 없는 해외 규정을 지어내지 않는다
</expected_behavior>
<source_data>
(원자료 없음)
</source_data>
<answer>
사내 규정 문서에는 미국 예금자 보호에 관한 내용이 없어 확인해 드릴 수 없습니다.
</answer>
</case>

<case id="S05">
<history>
(없음)
</history>
<question>예금거래기본약관은 고객이 언제 볼 수 있어?</question>
<expected_behavior>
- 영업시간 중 열람과 교부 청구가 가능하다는 약관 내용을 안내한다
</expected_behavior>
<source_data>
[문서] 예금거래기본약관 — 은행은 이 약관을 영업점에 놓아두고, 거래처는 영업시간 중 언제든지 이 약관을 볼 수 있고 또한 그 교부를 청구할 수 있다.
</source_data>
<answer>
약관에 따르면 고객은 영업시간 중 언제든지 영업점에서 약관을 볼 수 있고, 교부도 청구할 수 있습니다.
</answer>
</case>

<case id="S06">
<history>
(없음)
</history>
<question>정기예금 금리 좋은 거 추천해줘</question>
<expected_behavior>
- 정기예금 상품을 금리와 함께 안내한다
- 어느 가입기간 기준인지 밝힌다
</expected_behavior>
<source_data>
[{"은행": "A은행", "상품": "A정기예금", "기간": 12, "기본금리": 3.5, "최고금리": 3.8}]
</source_data>
<answer>
12개월 기준 A은행 A정기예금을 추천합니다. 최고 연 3.8% 확정 수익이 보장되는 가장 안전한 상품입니다.
</answer>
</case>

<case id="S07">
<history>
(없음)
</history>
<question>정기예금 금리 좋은 거 추천해줘</question>
<expected_behavior>
- 정기예금 상품을 금리와 함께 안내한다
- 어느 가입기간 기준인지 밝힌다
</expected_behavior>
<source_data>
[{"은행": "A은행", "상품": "A정기예금", "기간": 12, "기본금리": 3.5, "최고금리": 3.8}]
</source_data>
<answer>
12개월 기준으로 A은행 A정기예금이 기본 연 3.5%, 최고 연 4.1%입니다.
</answer>
</case>

<case id="S08">
<history>
(없음)
</history>
<question>신한은행 18개월 정기예금 추천해줘</question>
<expected_behavior>
- 18개월 조건으로 찾지 못했다면 그 사실을 밝힌다
- 다른 기간으로 바꿔 안내했다면 바꿨다고 밝힌다
</expected_behavior>
<source_data>
[{"은행": "신한은행", "상품": "쏠편한 정기예금", "기간": 12, "최고금리": 3.2}]
</source_data>
<answer>
신한은행 정기예금으로는 쏠편한 정기예금이 최고 연 3.2%로 좋습니다.
</answer>
</case>

<case id="S09">
<history>
(없음)
</history>
<question>예금거래기본약관은 고객이 언제 볼 수 있어?</question>
<expected_behavior>
- 영업시간 중 열람과 교부 청구가 가능하다는 약관 내용을 안내한다
</expected_behavior>
<source_data>
[문서] 예금거래기본약관 — 은행은 이 약관을 영업점에 놓아두고, 거래처는 영업시간 중 언제든지 이 약관을 볼 수 있고 또한 그 교부를 청구할 수 있다.
</source_data>
<answer>
약관 제3조 제2항에 따라 고객은 24시간 언제든 모바일 앱에서도 약관을 볼 수 있고, 은행은 요청 후 3영업일 안에 교부해야 합니다.
</answer>
</case>

<case id="S10">
<history>
(없음)
</history>
<question>엔화 환율 알려줘</question>
<expected_behavior>
- 엔화 환율은 조회할 수 없다는 점을 밝힌다
- 달러 환율을 엔화 환율인 것처럼 안내하지 않는다
</expected_behavior>
<source_data>
{"통화": "USD/KRW", "환율": 1397.7, "기준일": "2026.08.19"}
</source_data>
<answer>
현재 환율은 1397.7원입니다(기준일 2026.08.19).
</answer>
</case>
