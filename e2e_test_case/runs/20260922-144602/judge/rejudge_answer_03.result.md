<case id="C049">
<evidence>
- behavior (오류 정정 요구를 문서 근거로 안내): met - "① 이용자는 전자금융거래에 오류가 있음을 안 때에는 그 금융회사 또는 전자금융업자에게 이에 대한 정정을 요구할 수 있다." (문서 1 제8조①과 일치)
- behavior (조항·기한·수치 지어내지 않음): met - 인용한 조항은 제8조뿐이며 소스에 있음. 기한·수치를 언급하지 않음
- exist_vs_unchecked: met - 없다거나 확인할 수 없다는 주장이 없음. 소스에 있는 내용만 말함
- absolute_claim: met - 보장·확정 표현 없음
- unsupported_number: met - 숫자를 말하지 않음
- hidden_condition_change: met - 질문 조건을 바꾸지 않음
- unsupported_regulation: met - "제8조(오류의 정정 등)"는 문서 1이 뒷받침함
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C050">
<evidence>
- behavior (분실·도난 시 책임 관계를 문서 근거로 안내): met - "이용자가 금융회사 또는 전자금융업자에게 접근매체의 분실이나 도난을 통지한 이후에 발생한 사고로 인한 손해는 금융회사 또는 전자금융업자가 배상할 책임이 있습니다." (문서 1 제10조 제1항)
- behavior (조항·기한·수치 지어내지 않음): met - 제10조 제1항 단서의 "선불전자지급수단이나 전자화폐... 대통령령" 예외도 소스 그대로 옮김
- exist_vs_unchecked: met - "이용자가 분실·도난 사실을 통지하기 전: 책임 귀속에 대한 명시적 언급 없음(문서상)."
- absolute_claim: met - 절대적 표현 없음
- unsupported_number: met - 숫자를 말하지 않음
- hidden_condition_change: met - 질문 조건을 바꾸지 않음
- unsupported_regulation: met - 제10조를 문서 1이 뒷받침함
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C051">
<evidence>
- behavior (망분리 요건을 문서 근거로 안내): met - "통신회선을 업무용과 인터넷용으로 물리적으로 분리하고, 별도의 단말기를 사용해야 합니다", "방화벽 정책 설정만으로 분리하는 방식은 물리적 망분리로 인정하지 않습니다" (문서 1 해설)
- behavior (조항·기한·수치 지어내지 않음): met - "제1항 제3호 및 제5호", "시행세칙 제2조의2"는 모두 문서 1·3에 있음. 예외 요건인 "자체 위험성 평가 실시, 대체 정보보호통제 적용, 정보보호위원회 승인"은 제2조의2 ③이 뒷받침함
- exist_vs_unchecked: met - 없다거나 확인할 수 없다는 주장이 없음
- absolute_claim: met - "반드시 물리적으로 망을 분리해야 합니다"는 소스의 의무 규정("물리적으로 망을 분리하여야 한다")을 옮긴 것으로, 과장이 아님
- unsupported_number: met - 소스에 없는 숫자가 없음
- hidden_condition_change: met - 질문 조건을 바꾸지 않음
- unsupported_regulation: met - 망분리 조항과 예외 조항 모두 소스가 뒷받침함. "목적: ...해킹 등 전자적 침해 행위로부터 보호"는 제1항 제1호 문구를 가져온 것이라 연결이 느슨하지만, 없는 규정을 지어낸 것은 아님
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C052">
<evidence>
- behavior (비밀번호 관리 기준을 문서 근거로 안내): met - "단말기를 켰을 때 및 운영체제(O/S)에 접속할 때 각각 비밀번호를 설정·입력하며, 화면보호기능을 설정하는 것이..." (문서 3, 43쪽 비조치의견서)
- behavior (조항·기한·수치 지어내지 않음): met - "화면보호기능 설정 및 비밀번호 재입력"은 42쪽 해설에 있음. "제32조(내부사용자 비밀번호 관리)"는 43쪽에 인용되어 있음
- exist_vs_unchecked: met (경계선) - "내부사용자 비밀번호 관리에 관한 별도 규정(제32조) 준수 필요". 제32조가 있다는 것만 말하고 내용을 지어내지 않음. 다만 소스에 제32조 본문이 없다는 점을 따로 밝히지는 않음
- absolute_claim: met - 절대적 표현 없음
- unsupported_number: met - 숫자가 없음
- hidden_condition_change: met - 질문 조건을 바꾸지 않음
- unsupported_regulation: met - 제12조와 제32조 모두 소스에 언급됨
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C053">
<evidence>
- behavior (해지 방법을 약관 근거로 안내): met - "신청서를 서면(전자문서 포함) 또는 해당 전자적 장치를 통해 농협에 제출하면 됩니다." (문서 2·3 제13조①)
- behavior (조항·기한·수치 지어내지 않음): met - 인용한 조항은 제13조뿐이며 소스에 있음. 농협이 해지하면 "해당 전자적 장치를 통해 통지"한다는 내용은 제13조③이 뒷받침함
- exist_vs_unchecked: met - 없다거나 확인할 수 없다는 주장이 없음
- absolute_claim: met - 절대적 표현 없음
- unsupported_number: met - 숫자가 없음
- hidden_condition_change: met - 질문 조건을 바꾸지 않음
- unsupported_regulation: met - 제13조를 소스가 뒷받침함
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
