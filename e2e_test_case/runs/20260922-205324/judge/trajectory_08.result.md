<case id="C036">
<evidence>
- 달러 시세 질의를 exchange_rate로 라우팅하고 inquire_exchange_rate를 오류 없이 한 번 호출함
- 가드레일 후 결과(USD/KRW 1358.2원, 기준일)를 바로 답변해 불필요한 단계가 없음
</evidence>
<result>PASS</result>
</case>

<case id="C037">
<evidence>
- 환율 조회를 exchange_rate로 라우팅하고 도구를 한 번 호출해 결과 1건을 받음
- 사용자가 요청한 기준일(2026.09.22)이 최종 답변에 들어감
- route, tool, guardrail, finalize로 이어지는 흐름이 간결하고 논리적임
</evidence>
<result>PASS</result>
</case>

<case id="C038">
<evidence>
- 여행 환전이라는 맥락 속 환율 질문을 exchange_rate로 올바르게 라우팅함
- 도구를 한 번 호출해 성공했고, 현재 환율과 기준일로 답변함
- 흐름이 효율적이고 목표를 달성함
</evidence>
<result>PASS</result>
</case>

<case id="C039">
<evidence>
- 약관 질의를 policy_qa로 라우팅하고 질의를 열람 시기/방법 중심으로 재작성함
- 검색 결과 대부분이 예금거래기본약관 문서임
- 영업시간 중 언제든지 열람하고 교부를 청구할 수 있다고 원문을 인용해 답변함
</evidence>
<result>PASS</result>
</case>

<case id="C040">
<evidence>
- policy_qa로 라우팅하고 통장/인감 분실 조치를 묻는 방향으로 질의를 재작성함
- 검색된 4건이 모두 예금거래기본약관인데도 "확인할 수 없음"이라고 답해 사용자 목표를 이루지 못함
- 재검색이나 질의 재구성 같은 회복 시도 없이 바로 종료함
- 해당 약관에는 보통 분실 신고 조항이 있으므로 검색/근거 활용이 실패한 것으로 보임
</evidence>
<result>FAIL</result>
</case>
