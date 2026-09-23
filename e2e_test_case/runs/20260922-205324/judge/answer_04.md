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
농협에서 신용점수 650점으로 받을 수 있는 사업자대출 금리는 조회 결과 확인되지 않았습니다. 대신, 신용점수 650점(601~700점 구간)에 해당하는 다른 은행의 사업자대출 금리를 안내해 드리면 다음과 같습니다.

- 제주은행 JJB가맹점우대론: 연 4.46%
- 우리은행 우리상생파트너론: 연 4.85%
- 우리은행 우리CUBE론-X(일반,산업단지): 연 4.95%

참고로, 처음에는 농협에 한정해서 조회했으나 결과가 없어 조건을 넓혀 안내드리는 점 양해 부탁드립니다.
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
현재 조회 결과 기준으로, 가게 운영자금 대출 중에서는 제주은행의 'JJB가맹점우대론'이 4.46%로 가장 낮은 금리를 제공하고 있습니다. 그 외에 우리은행의 '우리상생파트너론'(4.85%)과 '우리CUBE론-X(일반,산업단지)'(4.95%)가 있습니다.
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
 "rate": 1358.2,
 "base_date": "20260922"
}
</source_data>
<answer>
현재 USD/KRW 환율은 1358.2원입니다. (기준일: 2026.09.22)
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
 "rate": 1358.2,
 "base_date": "20260922"
}
</source_data>
<answer>
현재 USD/KRW 환율은 1358.2원입니다. (기준일: 2026.09.22)
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
 "rate": 1358.2,
 "base_date": "20260922"
}
</source_data>
<answer>
현재 USD/KRW 환율은 1358.2원입니다. (기준일: 2026.09.22)
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
 "rate": 1358.2,
 "base_date": "20260922"
}
</source_data>
<answer>
현재 USD/KRW 환율은 1358.2원입니다. (기준일: 2026.09.22)
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
 "rate": 1358.2,
 "base_date": "20260922"
}
</source_data>
<answer>
현재 USD/KRW 환율은 1358.2원입니다. (기준일: 2026.09.22)
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
 "rate": 1358.2,
 "base_date": "20260922"
}
</source_data>
<answer>
현재 USD/KRW 환율은 1358.2원입니다. (기준일: 2026.09.22)
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

[문서 3] 금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt
## Page 11 참고 4 약관상 중요한 내용 관련 판례(대법원 2016다276177) 설명의무의 대상이 되는 ‘중요한 내용’은 사회통념에 비추어 고객 이 계약체결의 여부나 대가를 결정하는 데 직접적인 영향을 미칠 수 있 는 사항을 말한다. 사업자에게 약관의 명시·설명의무를 요구하는 것 은 어디까지나 고객이 알지 못하는 가운데 약관의 중요한 사항이 계 약 내용으로 되어 고객이 예측하지 못한 불이익을 받게 되는 것을 피 하고자 하는 데 근거가 있다. 따라서 약관에 정하여진 사항이라고 하더 라도 거래상 일반적이고 공통된 것이어서 고객이 별도의 설명 없이도 충 분히 예상할 수 있었던 사항이거나 이미 법령에 의하여 정하여진 것을 되풀이하거나 부연하는 정도에 불과한 사항이라면, 그러한 사항에 대하 여서까지 사업자에게 설명의무가 있다고 할 수는 없다. 사업자의 설명의무를 면제하는 사유로서 ‘거래상 일반적이고 공통된 것’이라는 요건은 해당 약관 조항이 거래계에서 일반적으로 통용되고 있는지의 측면에서, ‘고객이 별도의 설명 없이도 충분히 예상할 수 있는 사항’인지는 소송당사자인 특정 고객에 따라 개별적으로 예측가능성이 있었는지의 측면에서 각 판단되어야 한다. 다음으로 약관에 정하여진 사항이 ‘이미 법령에 의하여 정하여진 것을 되풀이하거나 부연하는 정도에 불과한지’는 약관과 법령의 규정 내용, 법령의 형식 및 목적과 취지, 해당 약관이 고객에게 미치는 영향 등 여 러 가지 사정을 종합적으로 고려하여 판단하여야 한다. 여기에서 말하 는 ‘법령’은 일반적인 의미에서의 법령, 즉 법률과 그 밖의 법규명 령으로서의 대통령령, 총리
령, 부령 등을 의미하고, (중략) 대외적 구 속력이 인정되지 않는 행정규칙으로서의 고시는 (중략) 사업자의 설명 의무가 면제된다고 할 수 없다.

[문서 4] 예금거래기본약관.txt
## 제22조(약관의 변경)
① 은행이 이 약관이나 입출금이자유로운예금약관, 거치식·적립식예금약관(이하 총칭하여
본조에서 “약관등”이라 한다)을 변경하고자 하는 경우에는 변경되는 약관등의 시행
1개월 전에 그 내용을 영업점과 인터넷 홈페이지에 게시하여 거래처에 알린다.
============================================================
[섹션 전환: 30 → 31]
============================================================
## Page 8  
*이 약관은 금융소비자보호에 관한 법률 등 관련 법령 및 당행의 내부통제기준에 따른 절차를 거쳐 제공됩니다.
- 8 -
다만, 다음 각 호의 어느 하나에 해당하는 경우에는 변경된 약관등을 즉시 게시 또는
공고하여야 한다.
1. 법령의 개정, 제도의 개선 또는 관련 법령에 의한 약관변경권고(명령)로 인하여
긴급히 약관등을 변경한 경우
2. 약관등의 개정이 거래처에 유리한 경우
3. 변경 전 내용이 기존 거래처에 그대로 적용되는 경우
4. 기존 약관등의 내용이 실질적으로 변경되지 않는 단순한 문구 변경의 경우
② 
</source_data>
<answer>
예금거래기본약관은 고객이 영업시간 중 언제든지 영업점에서 열람할 수 있으며, 그 교부를 청구할 수도 있습니다.  
(문서 인용: "은행은 이 약관을 영업점에 놓아두고, 거래처는 영업시간 중 언제든지 이 약관을 볼 수 있고 또한 그 교부를 청구할 수 있다.")
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

[문서 2] 예금거래기본약관.txt
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

[문서 3] 예금거래기본약관.txt
## 제10조(지급․해지청구) ① 거래처가 예금․이자를 찾거나 예금계약을 해지하고자 할 때에는 신고한 비밀번호 등 필요사항을 기재하거나 PIN-Pad기에 입력하고, 거래인감을 날인하거나 서명감과 일 치되게 서명한 지급 또는 해지청구서를 제출하여야 한다. ② 거래처가 무통장으로 거래하고 실명확인증표 등에 의해 본인확인된 경우, 은행이 정 하는 바에 따라 제①항에 따른 절차의 전부 또는 일부를 생략할 수 있다. ③ 거래처가 자동이체․전산통신기기․바이오정보 등을 이용하여 찾을 때는 그 약정에서 정한 바에 따른다.

[문서 4] 예금거래기본약관.txt
## Page 1 *이 약관은 금융소비자보호에 관한 법률 등 관련 법령 및 당행의 내부통제기준에 따른 절차를 거쳐 제공됩니다. - 1 - 예금거래기본약관 이 예금거래기본약관(이하 “약관”이라 한다)은 우리은행(이하 “은행”이라 한다)과 거래처 (또는 예금주)가 서로 믿음을 바탕으로 예금거래를 빠르고 틀림 없이 처리하는 한편, 서 로의 이해관계를 합리적으로 조정하기 위하여 기본적이고 일반적인 사항을 정한 것이다. 은행은 이 약관을 영업점에 놓아두고, 거래처는 영업시간 중 언제든지 이 약관을 볼 수 있고 또한 그 교부를 청구할 수 있다.
</source_data>
<answer>
문서에 따르면, 예금거래기본약관에서 예금자가 통장 또는 인감을 분실한 경우 취해야 할 조치에 관한 규정은 **확인할 수 없습니다**.  
제공된 문서에는 통장 또는 인감 분실 시의 구체적인 절차나 조치에 대한 내용이 포함되어 있지 않습니다.
</answer>
</case>
