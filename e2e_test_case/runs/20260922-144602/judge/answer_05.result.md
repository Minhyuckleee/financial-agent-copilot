<case id="C041">
<evidence>
- 행동1 충족(결론+문서 근거): "전화 통화를 통해 개인정보 수집에 대한 동의를 받는 것은 관련 법령상 허용됩니다" + 인용 "개인정보처리자는 전화상으로 개인정보 수집에 대한 정보주체의 동의를 받을 수 있다"
- 행동2 충족: 인용한 조항 "보호법 제22조 제1항, 보호법 시행령 제17조 제2항"은 문서 6에 있음. "Page 428"은 인용 위치 표기이고 규정 수치는 아님(문서 5에는 쪽 번호가 보이지 않음, 경미)
- exist_vs_unchecked 충족: 해당 없음
- absolute_claim 충족: "녹취 등 입증 가능한 방법을 사용하는 것이 필요합니다"
- unsupported_number 충족: 72시간·금액 등 새 수치 없음
- hidden_condition_change 충족: 해당 없음
- unsupported_regulation 충족: 입증책임·녹음 필요는 문서 5·6이 뒷받침함
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C042">
<evidence>
- 행동1 일부 충족: "「개인정보 보호법」 제30조 및 동법 시행령, 표준지침에서..."는 문서 근거가 있음. 다만 목록에 문서에 없는 항목을 섞음
- 행동2 미충족: "제21조제1항 단서에 따라 개인정보를 보존하여야 하는 경우", "민감정보의 공개 가능성 및 비공개를 선택하는 방법 (제23조제3항...)" — 문서에 없는 조항 번호
- unsupported_number 미충족: "제23조제3항", "제21조제1항 단서"
- unsupported_regulation 미충족: "개인정보의 제3자 제공에 관한 사항", "개인정보처리의 위탁에 관한 사항", "정보주체 이외로부터 수집한 개인정보의 경우에도 항목과 법적 근거를 기재해야 함" — 문서에 없는 기재 의무
- absolute_claim / hidden_condition_change / exist_vs_unchecked: 해당 없음
</evidence>
<result>FAIL</result>
<violations>behavior, unsupported_number, unsupported_regulation</violations>
</case>

<case id="C043">
<evidence>
- 행동1 미충족: 신고 기한만 답함 "**72시간 이내에** 관계 기관...에 신고해야 합니다". 정보주체 통지 기한(제26조 72시간)은 빠짐. 신고 대상 요건(문서의 "다음 각 호의 어느 하나에 해당하는 경우로서", 1천명 이상 등)도 빠져서 모든 유출에 신고 의무가 있는 것처럼 읽힘
- 행동2 충족: "72시간", "제40조", "제34조제1항"은 모두 문서에 있음
- unsupported_number 충족
- absolute_claim / unsupported_regulation / hidden_condition_change: 위반 없음
- exist_vs_unchecked: 해당 없음
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>

<case id="C044">
<evidence>
- 행동1 충족: "원칙적으로 정보주체(본인)로부터 별도의 동의를 받아야 합니다" / "법령에서 ... 요구하거나 허용하는 경우에는 별도의 동의 없이도 처리할 수 있습니다" — 문서 2·3이 근거
- 행동2 충족: 새 조항 번호나 수치 없음
- 참고(경미): "(문서 인용)"으로 표시한 "직원 개인의 근태 관리를 위해 ... 허용되지 않습니다"는 문서에 보이는 부분("직원 개인의 근태 관")보다 길다. 다만 내용은 이미 문서가 뒷받침하는 원칙을 다시 말한 것이다
- unsupported_regulation 충족: 별도 동의 원칙은 문서 3이 뒷받침함
- absolute_claim / unsupported_number / hidden_condition_change / exist_vs_unchecked: 위반 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C045">
<evidence>
- 행동1 미충족: 제시한 정의가 "“가명정보”란 가명처리한 개인신용정보를 말한다"뿐이고, "“가명처리”의 정의는 제2조 제15호에 규정되어 있습니다"라며 가명처리가 무엇인지는 설명하지 않음. 문서 5에 설명(추가정보 없이는 특정 개인을 알아볼 수 없도록 처리)이 있는데도 의미 설명이 순환 정의에 그침
- 행동2 충족: "신용정보법 제2조 제16호", "제15호"는 문서에 있음
- unsupported_number / unsupported_regulation / absolute_claim / hidden_condition_change / exist_vs_unchecked: 위반 없음
</evidence>
<result>FAIL</result>
<violations>behavior</violations>
</case>

<case id="C046">
<evidence>
- 행동1 미충족: 구체적인 요건은 제시하지 않고 조항 이름만 나열함 "필요한 요건에 대해 설명한 조항은 **제33조**와 **제34조의2**입니다"
- 행동2 미충족: "제7항에서는 제공 사실 및 이유 등을 사전에 신용정보주체에게 알려야 함을 명시" — 제33조 제7항은 문서에 없음
- unsupported_number 미충족: "제7항"
- unsupported_regulation 미충족: "제공 사실 및 이유 등을 사전에 ... 알려야 함", "요건, 절차, 예외 등을 상세히 규정" — 문서 4는 제6항 예외 목록만 보여줌
- absolute_claim / hidden_condition_change / exist_vs_unchecked: 해당 없음
</evidence>
<result>FAIL</result>
<violations>behavior, unsupported_number, unsupported_regulation</violations>
</case>

<case id="C047">
<evidence>
- 행동1 일부 충족: "정보주체가 개인정보처리자에게 자신의 개인정보를 본인 또는 다른 개인정보처리자에게 전송하도록 요구할 수 있는 권리"는 문서 2·4의 취지와 맞음. 다만 인용문 형태로 제시한 문장은 문서에 없음
- 행동2 미충족: "('23.3.14. 공포, '25.3.13. 시행)" — 문서에는 "2025년 3월 ... 본격 시행"만 있음
- unsupported_number 미충족: "'23.3.14.", "'25.3.13."
- unsupported_regulation 충족(경미): "제35조의2, 제35조의3, 제35조의4"는 문서 3에 관계법령으로 있음
- absolute_claim / hidden_condition_change / exist_vs_unchecked: 위반 없음
</evidence>
<result>FAIL</result>
<violations>behavior, unsupported_number</violations>
</case>

<case id="C048">
<evidence>
- 행동1 일부 충족: 연계정보 기반·개별식별자 기반, "ID/PASSWORD, 소셜로그인, PIN번호", "휴대폰 SMS, 전화 ARS"는 문서 1에 있음
- 행동2 미충족: "ID토큰 발급을 요청(API 전송요구-005)" — 문서에는 "API 전송요구-002"만 있음. 인가코드·콜백 URL 단계는 문서에 없음
- unsupported_number 미충족: "API 전송요구-005"
- unsupported_regulation 미충족: 3절 전체 "인증 화면에는 ... 경고문구 ... 를 반드시 삽입해야 합니다", "정보주체가 비용을 지불해야 하는 수단을 적용해서는 안 됩니다", "URL 또는 앱 스킴을 마이데이터 플랫폼에 사전 등록해야 합니다" — 문서에 없는 의무
- absolute_claim / hidden_condition_change / exist_vs_unchecked: 해당 없음
</evidence>
<result>FAIL</result>
<violations>behavior, unsupported_number, unsupported_regulation</violations>
</case>

<case id="C049">
<evidence>
- 행동1 충족: "이용자는 전자금융거래에 오류가 있음을 안 때에는 그 금융회사 또는 전자금융업자에게 이에 대한 정정을 요구할 수 있다" (제8조 ①, 문서 1)
- 행동2 충족: 새 기한이나 수치 없음, "제8조"는 문서에 있음
- unsupported_number / unsupported_regulation / absolute_claim / hidden_condition_change / exist_vs_unchecked: 위반 없음
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C050">
<evidence>
- 행동1 미충족: 문서 근거 없이 답함. 제시한 "제10조(접근매체의 분실과 도난 책임)" 본문은 문서 어디에도 없음. 문서에는 접근매체 분실 책임 조항이 없으므로 확인할 수 없다고 답했어야 함
- 행동2 미충족: "제10조"를 지어냄
- unsupported_number 미충족: "제10조"
- unsupported_regulation 미충족: "통지를 받은 때에는 그 때부터 ... 손해를 배상할 책임을 진다", "선불전자지급수단이나 전자화폐 ... 대통령령이 정하는 경우에는 그러하지 아니하다"
- exist_vs_unchecked: "통지하기 전: 책임 귀속에 대한 명시적 언급 없음(문서상)"이라고 부분적으로 구분했으나, 핵심 조항 자체가 문서에 없다는 점은 밝히지 않음
- absolute_claim / hidden_condition_change: 위반 없음
</evidence>
<result>FAIL</result>
<violations>behavior, unsupported_number, unsupported_regulation</violations>
</case>
