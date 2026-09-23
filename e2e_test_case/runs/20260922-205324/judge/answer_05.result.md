<case id="C041">
<evidence>
- behavior(결론+문서 근거): met - "전화 통화를 통해 개인정보 수집에 대한 동의를 받는 것은 관련 법령상 허용됩니다" + "서면, 전화, 인터넷, 전자우편 등의 방법으로 ... (보호법 제22조 제1항, 보호법 시행령 제17조 제2항)" (문서 6 Q50과 일치)
- behavior(조항·수치 미날조): met - 인용 조항 모두 문서 6에 존재
- exist_vs_unchecked: met - 해당 없음
- absolute_claim: met - 과장 표현 없음
- unsupported_number: met - 수치 없음
- hidden_condition_change: met - 조건 변경 없음
- unsupported_regulation: met - "정보주체의 음성을 녹음하는 등의 방법으로 동의의사를 확인받는 것이 필요" 문서 6 근거
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C042">
<evidence>
- behavior(기재 사항 문서 근거 안내): met - "1. 개인정보의 처리 목적 2. 개인정보의 처리 및 보유 기간 ..." 문서 3의 제30조 각 호와 일치, "10. 개인정보의 안전성 확보 조치"는 문서 6 목차 근거. 다만 "네, 맞습니다", "질문에서 언급한 항목들"은 질문에 없는 전제를 가정한 부자연스러운 표현(판정 기준 위반은 아님)
- behavior(조항·수치 미날조): met - 조항 번호·수치 제시 없음
- exist_vs_unchecked: met - 해당 없음
- absolute_claim: met - 없음
- unsupported_number: met - 없음
- hidden_condition_change: met - 없음
- unsupported_regulation: met - 나열 항목 모두 문서 3·6에 근거
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C043">
<evidence>
- behavior(통지·신고 기한 문서 근거): met - "개인정보 유출 사실을 알게 된 때로부터 72시간 이내에 신고해야 함" (문서 1·4·6)
- behavior(조항·수치 미날조): met - "개인정보 보호법 제34조", "신용정보법 제39조의4", "72시간" 모두 문서에 존재
- exist_vs_unchecked: met - 해당 없음
- absolute_claim: met - 없음
- unsupported_number: met - 신용정보법 "72시간 이내"도 문서 1·2 표에 존재
- hidden_condition_change: met - 없음
- unsupported_regulation: met - 예외 "천재지변이나 그 밖에 부득이한 사유" 문서 4·6 근거
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C044">
<evidence>
- behavior(동의 요건 문서 근거): met - "민감정보인 특징정보의 경우에는 다른 개인정보 처리에 대한 동의와 별도 동의가 필요" 문서 3 직접 인용
- behavior(조항·수치 미날조): met - "개인정보 보호법 제23조" 문서 2·3에 존재
- exist_vs_unchecked: met - 해당 없음
- absolute_claim: met - 없음
- unsupported_number: met - 없음
- hidden_condition_change: met - 없음
- unsupported_regulation: met - "법령에서 명시적으로 허용하거나 요구하는 경우에는 동의 없이도 처리" 문서 2·3 근거. "생체인식정보(지문 등)는 민감정보"는 문서상 특징정보에 한정되는 내용을 다소 일반화했으나 인용문으로 특징정보임을 밝힘
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C045">
<evidence>
- behavior(가명정보 의미 문서 근거): met - "“가명정보”란 가명처리한 개인신용정보를 말한다." 및 가명처리 정의 (문서 5)
- behavior(조항·수치 미날조): met - "신용정보법 제2조 제16호", "15호", "제40조의2제1항 및 제2항" 모두 문서 5에 존재
- exist_vs_unchecked: met - 해당 없음
- absolute_claim: met - 없음
- unsupported_number: met - 없음
- hidden_condition_change: met - 없음
- unsupported_regulation: met - 문서 인용 그대로
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C046">
<evidence>
- behavior(제3자 제공 요건 문서 근거): met - "미리 개별적으로 동의를 받아야 합니다 (제32조 1항)", "(제33조 6항 각 호 참조)", "(제33조 7항)" 문서 1·4 근거
- behavior(조항·수치 미날조): not met - "제3자에게 제공받은 개인신용정보는 다시 타인에게 제공해서는 안 됩니다. (제23조 5항, 제32조 4항)" 에서 제32조 4항은 문서상 필수/선택 동의 구분 조항이며 재제공 금지 근거가 아님
- exist_vs_unchecked: met - 해당 없음
- absolute_claim: met - 없음
- unsupported_number: met - 새 수치 없음
- hidden_condition_change: met - 없음
- unsupported_regulation: not met - 문서 1의 제23조⑤는 공공기관으로부터 받은 정보에 한정된 재제공 금지인데 "제공받은 자의 재제공 금지"로 일반 원칙화함. 또한 "법령에 따라 공개된 정보, 신용정보주체가 스스로 공개한 정보 등은 동의 없이 수집·제공이 가능 (제15조 2항)"은 문서상 수집에 대한 예외일 뿐 제공 예외가 아님
</evidence>
<result>FAIL</result>
<violations>behavior, unsupported_regulation</violations>
</case>

<case id="C047">
<evidence>
- behavior(전송요구권 의미 문서 근거): met - "정보주체가 개인정보처리자에게 본인의 개인정보를 자신에게 전송할 것을 요구할 수 있는 권리(본인전송요구)" 및 제3자전송요구 (문서 3)
- behavior(조항·수치 미날조): met - "보호법 제35조의2 제1항 및 제2항" 문서 3에 존재
- exist_vs_unchecked: met - 해당 없음
- absolute_claim: met - 없음
- unsupported_number: met - 없음
- hidden_condition_change: met - 없음
- unsupported_regulation: met - 문서 인용 그대로
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C048">
<evidence>
- behavior(인증 방식 문서 근거): met - "연계정보 기반", "개별식별자 기반", "ID/PASSWORD, 소셜로그인, PIN번호", "휴대폰 SMS, 전화 ARS, 휴대폰 본인확인" 문서 5 근거, 간편인증서 문서 1·2 근거
- behavior(조항·수치 미날조): met - 조항 번호·수치 제시 없음
- exist_vs_unchecked: met - 해당 없음
- absolute_claim: met - 없음
- unsupported_number: met - 없음
- hidden_condition_change: met - 없음
- unsupported_regulation: not met - "인증 과정에서 SSL/TLS 등 암호화 기반 인터넷 보안 프로토콜을 활용하여 개인정보가 유출되지 않도록 해야 합니다" 에서 문서 3은 본인전송요구 시 정보전송자가 데이터를 전송할 때 SSL/TLS를 "활용할 수 있다"고만 하며 인증 과정의 의무로 규정하지 않음. "모든 인증 과정은 법적·기술적 안전조치를 준수해야" 도 문서 근거 없는 일반화
</evidence>
<result>FAIL</result>
<violations>unsupported_regulation</violations>
</case>

<case id="C049">
<evidence>
- behavior(오류 정정 요구 문서 근거): met - "① 이용자는 전자금융거래에 오류가 있음을 안 때에는 그 금융회사 또는 전자금융업자에게 이에 대한 정정을 요구할 수 있다." (문서 1 제8조)
- behavior(조항·수치 미날조): met - "제8조" 문서 1에 존재
- exist_vs_unchecked: met - 해당 없음
- absolute_claim: met - 없음
- unsupported_number: met - 없음
- hidden_condition_change: met - 없음
- unsupported_regulation: met - 문서 인용 그대로
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>

<case id="C050">
<evidence>
- behavior(분실·도난 시 책임 관계 문서 근거): met - "이용자가 분실·도난 사실을 금융회사 등에 통지한 이후 발생한 손해에 대해서는 금융회사 또는 전자금융업자가 책임을 집니다" (문서 1 제10조)
- behavior(조항·수치 미날조): met - "제10조" 문서 1에 존재
- exist_vs_unchecked: met - 해당 없음
- absolute_claim: met - 없음
- unsupported_number: met - 없음
- hidden_condition_change: met - 없음
- unsupported_regulation: met - "선불전자지급수단이나 전자화폐 ... 대통령령이 정하는 경우에는 그러하지 아니하다" 문서 1 근거. "(예: 카드, OTP 등)"는 예시일 뿐 규정 주장 아님
</evidence>
<result>PASS</result>
<violations>none</violations>
</case>
