<case id="C044">
<evidence>
- behavior 1 (생체정보 동의 요건을 문서 근거로 안내) met: "원칙적으로 정보주체(본인)로부터 별도의 동의를 받아야 합니다" + 문서 3 인용 "원칙적으로 민감정보는 정보주체로부터 별도의 동의를 받은 경우나 법령에서 민감정보의 처리를 요구·허용하는 경우 외에는 처리할 수 없습니다"
- behavior 2 (조항 번호·기한·수치 지어내지 않음) met: 조항 번호·수치를 적지 않음
- exist_vs_unchecked met: 해당 없음, 없음/확인불가 혼동 없음
- absolute_claim met: "반드시 별도의 동의가 필요합니다"는 법령 예외 조건과 함께 쓰였고 문서 근거가 있음(수익·원금 관련 단정 아님)
- unsupported_number met: 수치 없음
- hidden_condition_change met: 조건 변경 없음
- unsupported_regulation met: "명시적이고 자유로운 의사에 따른 동의"는 문서 4에 근거가 있음(필수 동의 예외를 뭉뚱그렸지만 없는 규정을 지어낸 것은 아님)
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C045">
<evidence>
- behavior 1 (가명정보의 의미를 문서 근거로 설명) not met: "“가명정보”란 가명처리한 개인신용정보를 말한다" 만 인용하고 "“가명처리”의 정의는 제2조 제15호에 규정되어 있습니다"로 끝남. 핵심인 가명처리(추가정보 없이는 특정 개인을 알아볼 수 없도록 처리)를 설명하지 않아 정의가 순환에 그침
- behavior 2 met: "신용정보법 제2조 제16호", "제2조 제15호"는 문서 5에 있음
- exist_vs_unchecked met: 해당 없음
- absolute_claim met: 없음
- unsupported_number met: 없음
- hidden_condition_change met: 조건 변경 없음
- unsupported_regulation met: 인용 조항이 문서에 있음
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>

<case id="C046">
<evidence>
- behavior 1 (제3자 제공 요건을 문서 근거로 안내) met: "제33조 제6항에서는 예외적으로 동의 없이 제공할 수 있는 경우를 열거", "제7항에서는 제공 사실 및 이유 등을 사전에 신용정보주체에게 알려야", "제34조의2 ... 신용정보주체로부터 동의를 받아야 하며, 동의 시 고지해야 할 사항". 요건이 얇고 제10항 신원·목적 확인은 빠졌지만 문서에 근거한 요건을 제시함
- behavior 2 met: 제33조 제6항·제7항, 제34조의2는 모두 문서 4·5에 있음
- exist_vs_unchecked met: 해당 없음
- absolute_claim met: 없음
- unsupported_number met: 수치 없음
- hidden_condition_change met: 조건 변경 없음
- unsupported_regulation met: "예외적으로 동의 없이 제공할 수 있는 경우"는 제6항의 "제1항부터 제5항까지를 적용하지 아니한다"를 해석한 것이지만, 제34조의2가 제공 동의를 다루므로 문서 범위 안의 해석임
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C047">
<evidence>
- behavior 1 (전송요구권의 의미를 문서 근거로 설명) met: 문서 인용 "정보주체가 개인정보처리자에게 자신의 개인정보를 본인 또는 다른 개인정보처리자에게 전송하도록 요구할 수 있는 권리"
- behavior 2 met: "제35조의2, 제35조의3, 제35조의4", "'23.3.14. 공포, '25.3.13. 시행"은 문서 1·4에 있음
- exist_vs_unchecked met: 해당 없음
- absolute_claim met: 없음
- unsupported_number met: 날짜는 모두 원문에 있음
- hidden_condition_change met: 조건 변경 없음
- unsupported_regulation met(경계선): "정의는 ... 제35조의2, 제35조의3, 제35조의4에서 규정"은 세 조항에 정의가 있다고 넓게 말했지만, 문서 1이 세 조항을 제도의 "법적 근거"로 들고 있어 근거 없는 규정으로 보지는 않음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C048">
<evidence>
- behavior 1 (전송 시 인증 방식을 문서 근거로 안내) met: "인증정보 입력: ID/PASSWORD, 소셜로그인, PIN번호 등", "휴대폰 SMS, 전화 ARS, 휴대폰 본인확인 등", "인가코드 발급", "ID토큰 발급을 요청(API 전송요구-005)", "Nonce 생성 및 전송, 전자서명 생성 요청"은 모두 문서 1·6에 있음. 다만 5.3 주민등록번호 기반 유형을 빠뜨렸고, "연계정보(예: UCPID 등)"는 문서에서 연계정보의 예로 나온 것이 아님(사소함)
- behavior 2 met: "API 전송요구-005" 등 번호는 원문에 있고 지어낸 조항·기한·수치 없음
- exist_vs_unchecked met: 해당 없음
- absolute_claim met: 없음
- unsupported_number met: 없음
- hidden_condition_change met: 조건 변경 없음
- unsupported_regulation met: 지침 내용은 문서 1에 있음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
