<case id="E026">
<evidence>
- 예금자보호 한도는 제도 질문이므로 policy_qa 로 보냄 -> 맞음
- 질문을 구체적으로 바꿔 검색했으나 결과는 전자금융 약관·설명의무 가이드라인뿐이고 관련 근거 없음
- guardrail 을 거쳐 finalize, 근거가 없다는 점을 밝히고 추측하지 않음
- 순서가 짧고 논리적임. 재검색은 없지만 불필요한 단계도 없음
</evidence>
<result>PASS</result>
</case>

<case id="E027">
<evidence>
- DSR 규제 질문을 policy_qa 로 보냄 -> 맞음
- 질문을 DSR 비율로 좁혀 검색, 결과 문서에 해당 내용 없음
- guardrail -> finalize 로 이어지고 수치를 지어내지 않고 확인 불가라고 답함
- route -> retrieve -> guardrail -> answer 로 효율적으로 진행
</evidence>
<result>PASS</result>
</case>

<case id="E028">
<evidence>
- LTV 한도 질문을 policy_qa 로 보냄 -> 맞음
- 질문을 법령·약관 기준으로 바꿔 검색, 문서 5건 모두 LTV 와 무관
- 규정이 문서에 없다고 밝히고 최종 답변을 냄. "예: 70%"는 가정 예시일 뿐 사실로 단정하지 않음
- 단계 흐름이 논리적이고 중복 없음
</evidence>
<result>PASS</result>
</case>

<case id="E029">
<evidence>
- 특정 고객의 계좌 잔액 조회 요청(개인 계좌 데이터)을 out_of_scope 로 보냄 -> 맞음
- 검색 없이 answer_out_of_scope -> finalize 로 바로 종료, 효율적
- 범위 밖이라고 거절한 결과가 라우팅 결정과 일치
</evidence>
<result>PASS</result>
</case>

<case id="E030">
<evidence>
- 개별 고객의 대출 승인 여부와 한도를 판단해 달라는 요청을 out_of_scope 로 보냄 -> 맞음
- 불필요한 검색 없이 answer_out_of_scope -> finalize 로 진행
- 최종 거절 답변이 라우팅 결정과 일치
</evidence>
<result>PASS</result>
</case>
