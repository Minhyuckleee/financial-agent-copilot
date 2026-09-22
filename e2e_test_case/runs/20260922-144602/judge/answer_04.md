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

<case id="C031">
<history>
(없음)
</history>
<question>농협에서 신용점수 650점 사업자대출 금리 알려줘</question>
<expected_behavior>
- 농협 650점 기준 금리를 안내하거나, 조회되지 않으면 그렇다고 밝힌다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "제주은행",
  "product_name": "JJB가맹점우대론",
  "credit_score_band": "601~700점",
  "interest_rate": 4.46
 },
 {
  "bank_name": "우리은행",
  "product_name": "우리상생파트너론",
  "credit_score_band": "601~700점",
  "interest_rate": 4.85
 },
 {
  "bank_name": "우리은행",
  "product_name": "우리CUBE론-X(일반,산업단지)",
  "credit_score_band": "601~700점",
  "interest_rate": 4.95
 }
]
</source_data>
<answer>
농협에서 신용점수 650점으로 받을 수 있는 사업자대출 금리는 조회 결과 확인되지 않았습니다. 대신, 신용점수 601~700점 구간의 다른 은행 상품 금리는 다음과 같습니다:

- 제주은행 JJB가맹점우대론: 연 4.46%
- 우리은행 우리상생파트너론: 연 4.95%
- 우리은행 우리CUBE론-X(일반,산업단지): 연 4.95%

참고로, 처음에는 농협으로만 조회했으나 결과가 없어 조건을 넓혀 안내드리는 점 참고 부탁드립니다.
</answer>
</case>

<case id="C032">
<history>
(없음)
</history>
<question>가게 운영자금 대출 알아보는데 금리 낮은 데 있어?</question>
<expected_behavior>
- 개인사업자대출 상품을 안내한다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "제주은행",
  "product_name": "JJB가맹점우대론",
  "credit_score_band": "601~700점",
  "interest_rate": 4.46
 },
 {
  "bank_name": "우리은행",
  "product_name": "우리상생파트너론",
  "credit_score_band": "601~700점",
  "interest_rate": 4.85
 },
 {
  "bank_name": "우리은행",
  "product_name": "우리CUBE론-X(일반,산업단지)",
  "credit_score_band": "601~700점",
  "interest_rate": 4.95
 }
]
</source_data>
<answer>
현재 조회 결과 기준으로, 가게 운영자금 대출 중에서는 제주은행의 'JJB가맹점우대론'이 4.46%로 가장 낮은 금리를 제공하고 있습니다. 그 외에는 우리은행의 '우리상생파트너론'(4.95%)과 '우리CUBE론-X(일반,산업단지)'(4.95%)가 있습니다.
</answer>
</case>

<case id="C033">
<history>
(없음)
</history>
<question>환율 알려줘</question>
<expected_behavior>
- 원/달러 환율 값을 안내한다
- 기준일을 밝힌다
</expected_behavior>
<source_data>
[조회 결과 1]
{
 "currency_pair": "USD/KRW",
 "rate": 1381.0,
 "base_date": "20260921"
}
</source_data>
<answer>
현재 USD/KRW 환율은 1381.0원입니다. (기준일: 2026.09.21)
</answer>
</case>

<case id="C034">
<history>
(없음)
</history>
<question>달러 환율 얼마야?</question>
<expected_behavior>
- 원/달러 환율 값을 안내한다
- 기준일을 밝힌다
</expected_behavior>
<source_data>
[조회 결과 1]
{
 "currency_pair": "USD/KRW",
 "rate": 1381.0,
 "base_date": "20260921"
}
</source_data>
<answer>
현재 USD/KRW 환율은 1381.0원입니다. (기준일: 2026.09.21)
</answer>
</case>

<case id="C035">
<history>
(없음)
</history>
<question>지금 원달러 몇 원이야?</question>
<expected_behavior>
- 원/달러 환율 값을 안내한다
- 기준일을 밝힌다
</expected_behavior>
<source_data>
[조회 결과 1]
{
 "currency_pair": "USD/KRW",
 "rate": 1381.0,
 "base_date": "20260921"
}
</source_data>
<answer>
현재 USD/KRW 환율은 1381.0원입니다. (기준일: 2026.09.21)
</answer>
</case>

<case id="C036">
<history>
(없음)
</history>
<question>미국 달러 시세 좀 알려줘</question>
<expected_behavior>
- 원/달러 환율 값을 안내한다
- 기준일을 밝힌다
</expected_behavior>
<source_data>
[조회 결과 1]
{
 "currency_pair": "USD/KRW",
 "rate": 1381.0,
 "base_date": "20260921"
}
</source_data>
<answer>
현재 USD/KRW 환율은 1381.0원입니다. (기준일: 2026.09.21)
</answer>
</case>

<case id="C037">
<history>
(없음)
</history>
<question>환율 조회해줘, 기준일도 같이</question>
<expected_behavior>
- 원/달러 환율 값을 안내한다
- 기준일을 밝힌다
</expected_behavior>
<source_data>
[조회 결과 1]
{
 "currency_pair": "USD/KRW",
 "rate": 1381.0,
 "base_date": "20260921"
}
</source_data>
<answer>
현재 USD/KRW 환율은 1381.0원입니다. (기준일: 2026.09.21)
</answer>
</case>

<case id="C038">
<history>
(없음)
</history>
<question>해외여행 가서 달러 환전하려는데 지금 환율 어때?</question>
<expected_behavior>
- 원/달러 환율 값을 안내한다
- 기준일을 밝힌다
</expected_behavior>
<source_data>
[조회 결과 1]
{
 "currency_pair": "USD/KRW",
 "rate": 1381.0,
 "base_date": "20260921"
}
</source_data>
<answer>
현재 USD/KRW 환율은 1381.0원입니다. (기준일: 2026.09.21)
</answer>
</case>

<case id="C039">
<history>
(없음)
</history>
<question>예금거래기본약관은 고객이 언제 볼 수 있어?</question>
<expected_behavior>
- 영업시간 중 열람과 교부 청구가 가능하다는 약관 내용을 안내한다
- 문서에 없는 조항 번호·기한·수치를 지어내지 않는다
</expected_behavior>
<source_data>
[문서 1] 예금거래기본약관.txt
Page 1  
*이 약관은 금융소비자보호에 관한 법률 등 관련 법령 및 당행의 내부통제기준에 따른 절차를 거쳐 제공됩니다. - 1 -
예금거래기본약관
이 예금거래기본약관(이하 “약관”이라 한다)은 우리은행(이하 “은행”이라 한다)과 거래처
(또는 예금주)가 서로 믿음을 바탕으로 예금거래를 빠르고 틀림 없이 처리하는 한편, 서
로의 이해관계를 합리적으로 조정하기 위하여 기본적이고 일반적인 사항을 정한 것이다.
은행은 이 약관을 영업점에 놓아두고, 거래처는 영업시간 중 언제든지 이 약관을 볼 수
있고 또한 그 교부를 청구할 수 있다.
============================================================
[섹션 전환: 0 → 1]
============================================================
## 제1조(적용범위)
이 약관은 입출금이 자유로운 예금, 거치식예금 및 적립식예금 거래에 적용한다.

[문서 2] 예금거래기본약관.txt
## Page 1 *이 약관은 금융소비자보호에 관한 법률 등 관련 법령 및 당행의 내부통제기준에 따른 절차를 거쳐 제공됩니다. - 1 - 예금거래기본약관 이 예금거래기본약관(이하 “약관”이라 한다)은 우리은행(이하 “은행”이라 한다)과 거래처 (또는 예금주)가 서로 믿음을 바탕으로 예금거래를 빠르고 틀림 없이 처리하는 한편, 서 로의 이해관계를 합리적으로 조정하기 위하여 기본적이고 일반적인 사항을 정한 것이다. 은행은 이 약관을 영업점에 놓아두고, 거래처는 영업시간 중 언제든지 이 약관을 볼 수 있고 또한 그 교부를 청구할 수 있다.

[문서 3] NH농협은행_전자금융서비스이용약관.txt
## 제11조(서비스의 제한) 수 있습니다. 1. 1일 또는 1회 이체최고한도를 초과하거나 입금계좌의 최고예치 한도를 초 과한 때 2. 조회비밀번호, 자금이체비밀번호, 보안카드비밀번호, 보안카드일련번호, 생 체인증, 간편비밀번호는 누적하여 연속 5회, 계좌비밀번호는 누적하여 연속 5회, 일회용비밀번호(OTP)발생기에서 생성되는 비밀번호는 전 금융기관을 통합하여 누적하여 연속 10회 일치하지 않을 때, 모바일OTP의 PIN번호는 누적하여 연속 5회 일치하지 않을 때 3. 12개월간 자금이체 이용실적이 없는 때. 다만, 조회서비스 이용만 신청한 고객은 제외됩니다 4. 그 밖에 「예금거래기본약관」 등에서 정한 거래 제한사유가 발생한 때 ② 제1항제2호의 경우에는 서비스가 자동 중지되며, 제1항제3호의 경우에는 이체성 서비스가 자동 중지됩니다. 농협은 서비스 자동 중지와 관련하여 이용 자에게 다음 각 호와 같이 관련 내용을 사전에 미리 고지하고, 서비스 자동 중 지가 되는 시점에 이용자에게 관련 내용을 통지합니다. 1. 제1항제2호에 따른 자동 중지 : 입력한 비밀번호 또는 PIN번호가 일치하 지 않을 때마다, 제1항제2호의 사유가 발생할 경우 서비스가 중단될 수 있 음을 미리 고지합니다. 2. 제1항제3호에 따른 이체성 서비스 자동 중지 : 10개월간 자금이체 이용실 적이 없는 때에, 제1항제3호의 사유가 발생할 경우 이체성 서비스가 중단

[문서 4] 예금거래기본약관.txt
## 제23조(약관적용의 순서)
① 은행과 거래처 사이에 개별적으로 합의한 사항이 약관조항과 다를 때에는 그 합의사
항을 약관에 우선하여 적용한다.
② 이 약관에 정한 사항과 입출금이 자유로운 예금약관 또는 거치식․적립식 예금약관에
서 정한 사항이 다를 때는 입출금이 자유로운 예금 약관이나 거치식․적립식 예금약
관을 먼저 적용한다.
============================================================
[섹션 전환: 32 → 33]
============================================================
## Page 9  
*이 약관은 금융소비자보호에 관한 법률 등 관련 법령 및 당행의 내부통제기준에 따른 절차를 거쳐 제공됩니다. - 9 -
</source_data>
<answer>
문서에 따르면, 예금거래기본약관은 은행 영업점에 비치되어 있으며, 거래처(고객)는 영업시간 중 언제든지 이 약관을 볼 수 있고, 그 교부를 청구할 수 있습니다. 

따라서, **고객은 영업시간 중 언제든지 예금거래기본약관을 열람할 수 있습니다.**
</answer>
</case>

<case id="C040">
<history>
(없음)
</history>
<question>예금거래기본약관에서 통장이나 인감을 잃어버리면 어떻게 하라고 돼 있어?</question>
<expected_behavior>
- 분실 시 신고 절차를 약관 근거로 안내한다
- 문서에 없는 조항 번호·기한·수치를 지어내지 않는다
</expected_behavior>
<source_data>
[문서 1] 예금거래기본약관.txt
또는 서명, 비밀번호, 성명, 상호, 대표자명, 대리인
명, 주소 등 거래에 필요한 사항을 신고하여야 한다. 다만, 비밀번호는 비밀번호 입
력기(이하 “PIN-Pad기”라 한다)에 의하여 거래처가 직접 등록할 수 있으며, 거래처가
은행에 내점할 수 없는 경우 거래처는 개설된 예금의 첫거래 전에 은행이 정한 방법
에 따라 전산통신기기를 이용하여 비밀번호를 등록하여야 한다.
② 제1항에 불구하고 거치식․적립식 예금은 비밀번호를 신고하지 않을 수 있다.
③ 거래처는 인감과 서명을 함께 신고하거나, 인감 또는 서명을 추가 신고할 수 있다.
============================================================
[섹션 전환: 5 → 6]
============================================================
## Page 2  
*이 약관은 금융소비자보호에 관한 법률 등 관련 법령 및 당행의 내부통제기준에 따른 절차를 거쳐 제공됩니다. - 2 -
④ 통장을 발행하지 않는 경우, 은행은 거래처로부터 인감 또는 서명의 신고 절차를 생
략할 수 있다.

[문서 2] 예금거래기본약관.txt
## 제10조(지급․해지청구)
① 거래처가 예금․이자를 찾거나 예금계약을 해지하고자 할 때에는 신고한 비밀번호 등
필요사항을 기재하거나 PIN-Pad기에 입력하고, 거래인감을 날인하거나 서명감과 일
치되게 서명한 지급 또는 해지청구서를 제출하여야 한다.
② 거래처가 무통장으로 거래하고 실명확인증표 등에 의해 본인확인된 경우, 은행이 정
하는 바에 따라 제①항에 따른 절차의 전부 또는 일부를 생략할 수 있다.
③ 거래처가 자동이체․전산통신기기․바이오정보 등을 이용하여 찾을 때는 그 약정에서
정한 바에 따른다.
============================================================
[섹션 전환: 13 → 14]
============================================================
## Page 4  
*이 약관은 금융소비자보호에 관한 법률 등 관련 법령 및 당행의 내부통제기준에 따른 절차를 거쳐 제공됩니다. - 4 -

[문서 3] 예금거래기본약관.txt
## 제10조(지급․해지청구) ① 거래처가 예금․이자를 찾거나 예금계약을 해지하고자 할 때에는 신고한 비밀번호 등 필요사항을 기재하거나 PIN-Pad기에 입력하고, 거래인감을 날인하거나 서명감과 일 치되게 서명한 지급 또는 해지청구서를 제출하여야 한다. ② 거래처가 무통장으로 거래하고 실명확인증표 등에 의해 본인확인된 경우, 은행이 정 하는 바에 따라 제①항에 따른 절차의 전부 또는 일부를 생략할 수 있다. ③ 거래처가 자동이체․전산통신기기․바이오정보 등을 이용하여 찾을 때는 그 약정에서 정한 바에 따른다.

[문서 4] 예금거래기본약관.txt
## 제4조(거래방법)
거래처는 은행에서 내준 통장(증서․전자통장을 포함한다. 이하 같다.) 또는 수표․어음
용지로 거래하여야 한다. 그러나 입금할 때, 자동이체약정․전산통신기기이용약정에 따라
거래하는 경우 및 기등록된 생체정보(이하“바이오정보”), 실명확인증표 등을 통해 본인확
인된 경우에는 통장 없이(이하“무통장”)도 거래할 수 있다.
============================================================
[섹션 전환: 4 → 5]
============================================================
## 제5조(인감, 비밀번호 등의 신고)
① 거래처는 거래를 시작할 때 인감 또는 서명, 비밀번호, 성명, 상호, 대표자명, 대리인
명, 주소 등 거래에 필요한 사항을 신고하여야 한다. 다만, 비밀번호는 비밀번호 입
력기(이하 “PIN-Pad기”라 한다)에 의하여 거래처가 직접 등록할 수 있으며, 거래처가
은행에 내점할 수 없는 경우 거래처는 개설된 예금의 첫거래 전에 은행이 정한 방법
에 따라 전산통신기기를 이용하여 비밀번호를 등록하여야 한다.
② 제1항에 불구하고 거치식․적립식 예금은 비밀번호를 신고하지 않을 수 있다.
③ 거래

[문서 5] 예금거래기본약관.txt
 믿을
충분한 이유가 있는 때에는 거래처에 정당하게 통보한 것으로 본다.
② 은행이 예금거래에서 발생하는 일반적 사항을 서면으로 통지했을 때는 천재지변 등
불가항력적인 경우 외에는 보통의 우송기간이 지났을 때 도달한 것으로 본다.
③ 은행은 예금계약의 임의해지 등 중요한 의사표시를 하는 때에는 서면으로 하여야 하
며 그 통지가 거래처에 도달되어야 의사표시의 효력이 생긴다. 다만, 관계법령 또는
어음교환소규약 등에 의하여 예금계약을 해지한 경우나 거래처가 제15조에 의한 변경
신고를 게을리하여 도달되지 않은 때에는 그러하지 아니하다.
============================================================
[섹션 전환: 24 → 25]
============================================================
## 제18조(면 책)
① 은행은 예금지급청구서, 증권 또는 신고서 등에 찍힌 인영(또는 서명)을 신고한 인감
(또는 서명감)과 육안으로 주의 깊게 비교․대조하여 틀림없다고 여기고, 예금지급청
구서 등에 적힌 비밀번호나 PIN-Pad기를 이용하여 입력된 비밀번호가 신고 또는 등
록한 것과 같아서 예금을 지급하였거나 기타 거래처가 요구하는 업무를 처리하였을
때에는 인감이나 서명의 위조․변조 또는 도용이나 그밖의 다른 사고로 인하여 거래
처에 손해가 생겨도 그 책임
</source_data>
<answer>
제공해주신 문서의 내용에는 예금자가 통장 또는 인감을 분실한 경우 취해야 할 조치(예: 분실신고, 재발급 절차 등)에 관한 구체적인 규정이 포함되어 있지 않습니다. 따라서 해당 사항에 대해 문서에서 확인할 수 없다고 답변드립니다.
</answer>
</case>
