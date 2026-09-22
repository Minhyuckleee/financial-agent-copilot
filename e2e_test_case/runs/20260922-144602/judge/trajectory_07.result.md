<case id="C031">
<evidence>
- 대출 상품 질문을 product_recommendation 으로 라우팅한 것은 맞다.
- 첫 호출은 신용점수 650과 농협 필터를 넘겼고, 결과가 비어서 돌아왔다.
- 필터를 뺀 재시도는 한 번뿐이었고, 결과 3건을 받았다. 루브릭상 기대되는 동작이다.
- 수치 자기점검 guardrail 을 거친 뒤 답변을 마무리했다.
- 최종 답변은 농협 결과가 없다는 점과 조건을 넓혔다는 점을 밝힌다. 흐름이 논리적이고 효율적이다.
</evidence>
<result>PASS</result>
</case>

<case id="C032">
<evidence>
- 라우팅(product_recommendation)과 도구 선택은 맞다.
- 사용자는 신용점수를 말하지 않았는데, 에이전트가 credit_score=700 을 지어내서 도구에 넘겼다.
- 되묻는 단계가 없고, 가정했다는 사실도 최종 답변에 없다.
- 그런데도 "가장 낮은 금리"라고 일반화해서 제시했다. 실제로는 사용자가 모르는 가정 점수 구간의 결과일 뿐이다.
- 근거 없는 인자로 결과 범위가 정해졌다. 단계 사이의 논리가 맞지 않는다.
</evidence>
<result>FAIL</result>
</case>

<case id="C033">
<evidence>
- 환율 질문을 exchange_rate 로 라우팅하고 inquire_exchange_rate 를 한 번 호출해 결과 1건을 받았다.
- 호출 한 번으로 끝났고, 답변에 수치와 기준일이 들어 있다.
- 최소 단계로 곧장 진행했다.
</evidence>
<result>PASS</result>
</case>

<case id="C034">
<evidence>
- 달러 환율 질문을 exchange_rate 로 라우팅하고 inquire_exchange_rate 를 한 번 호출해 결과 1건을 받았다.
- 답변에 USD/KRW 값과 기준일이 들어 있다.
- 효율적이고 논리적이다.
</evidence>
<result>PASS</result>
</case>

<case id="C035">
<evidence>
- 원달러 질문을 exchange_rate 로 라우팅하고 도구를 한 번 호출해 결과 1건을 받았다.
- 답변에 USD/KRW 값과 기준일이 들어 있다.
- 불필요한 단계가 없다.
</evidence>
<result>PASS</result>
</case>
