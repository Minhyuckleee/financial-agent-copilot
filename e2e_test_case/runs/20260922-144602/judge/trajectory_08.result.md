<case id="C036">
<evidence>
- 달러 시세 질문을 exchange_rate 로 라우팅, 적절함
- inquire_exchange_rate 1회 호출, 오류 없음, 결과 1건
- guardrail 후 USD/KRW 값과 기준일로 최종 답변. 단계가 짧고 논리적
</evidence>
<result>PASS</result>
</case>

<case id="C037">
<evidence>
- 환율 조회를 exchange_rate 로 라우팅, 도구 1회 호출 성공
- 사용자가 요청한 기준일(2026.09.21)이 답변에 포함됨
- 불필요한 단계 없음
</evidence>
<result>PASS</result>
</case>

<case id="C038">
<evidence>
- 여행 환전 맥락의 질문을 exchange_rate 로 올바르게 라우팅
- 도구 1회 호출 성공, 현재 환율과 기준일을 제시함
- 핵심 질문(지금 환율)에 답했고 경로가 효율적임
</evidence>
<result>PASS</result>
</case>

<case id="C039">
<evidence>
- 약관 질문을 policy_qa 로 라우팅, 질의를 열람 시점 중심으로 재작성
- 예금거래기본약관.txt 청크 3건 등 관련 문서를 검색함
- 검색 결과에 근거해 영업시간 중 언제든지 열람·교부 청구 가능하다고 답함. 목표 달성
</evidence>
<result>PASS</result>
</case>

<case id="C040">
<evidence>
- policy_qa 로 라우팅, 분실 시 조치로 질의 재작성, 대상 문서 청크 5건 검색. 단계 자체는 논리적
- 최종 답변은 문서에서 확인할 수 없다고 명시함. 근거 없이 지어내지 않음
- 올바른 문서를 검색했는데도 답을 찾지 못했고 질의를 바꿔 재검색하지 않음. 파일만으로는 해당 조항이 실제로 있는지 확인할 수 없음
- 경로는 일관되고 효율적이며 결과를 정직하게 보고함
</evidence>
<result>PASS</result>
</case>
