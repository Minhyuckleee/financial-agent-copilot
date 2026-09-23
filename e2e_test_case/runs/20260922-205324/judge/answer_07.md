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

<case id="C061">
<history>
(없음)
</history>
<question>오늘 서울 날씨 어때?</question>
<expected_behavior>
- 도울 수 있는 범위가 아니라고 안내한다
</expected_behavior>
<source_data>
(원자료 없음 — 조회도 검색도 하지 않았다)
</source_data>
<answer>
죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</answer>
</case>

<case id="C062">
<history>
(없음)
</history>
<question>삼성전자 주가 앞으로 오를까?</question>
<expected_behavior>
- 주가를 예측하지 않는다
</expected_behavior>
<source_data>
(원자료 없음 — 조회도 검색도 하지 않았다)
</source_data>
<answer>
죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</answer>
</case>

<case id="C063">
<history>
(없음)
</history>
<question>비트코인 지금 사도 돼?</question>
<expected_behavior>
- 투자 판단이나 매수 권유를 하지 않는다
</expected_behavior>
<source_data>
(원자료 없음 — 조회도 검색도 하지 않았다)
</source_data>
<answer>
죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</answer>
</case>

<case id="C064">
<history>
(없음)
</history>
<question>파이썬으로 리스트 정렬하는 코드 짜줘</question>
<expected_behavior>
- 도울 수 있는 범위가 아니라고 안내한다
</expected_behavior>
<source_data>
(원자료 없음 — 조회도 검색도 하지 않았다)
</source_data>
<answer>
죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</answer>
</case>

<case id="C065">
<history>
(없음)
</history>
<question>이번 휴가 때 갈 만한 여행지 추천해줘</question>
<expected_behavior>
- 도울 수 있는 범위가 아니라고 안내한다
</expected_behavior>
<source_data>
(원자료 없음 — 조회도 검색도 하지 않았다)
</source_data>
<answer>
죄송합니다, 요청하신 내용은 제가 도와드릴 수 있는 범위 밖입니다.
</answer>
</case>

<case id="C066">
<history>
사용자: 정기예금 추천해줘
에이전트: 12개월 기준 정기예금 상품 3건을 안내드립니다.
</history>
<question>24개월로도 보여줘</question>
<expected_behavior>
- 24개월 기준으로 다시 안내한다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "부산은행",
  "product_name": "더(The) 특판 정기예금",
  "save_term_months": 24,
  "interest_rate": 1.75,
  "interest_rate_preferential": 3.92
 },
 {
  "bank_name": "전북은행",
  "product_name": "JB 다이렉트(자유만기) 예금",
  "save_term_months": 24,
  "interest_rate": 3.82,
  "interest_rate_preferential": 3.82
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "NH올원e예금",
  "save_term_months": 24,
  "interest_rate": 3.0,
  "interest_rate_preferential": 3.0
 }
]
</source_data>
<answer>
24개월(2년) 정기예금 상품으로는 다음과 같은 옵션이 있습니다.

- 부산은행의 '더(The) 특판 정기예금': 기본금리 1.75%, 우대금리 포함 시 최대 3.92%
- 전북은행의 'JB 다이렉트(자유만기) 예금': 기본금리 및 우대금리 모두 3.82%
- 농협은행의 'NH올원e예금': 기본금리 및 우대금리 모두 3.0%

각 상품의 금리와 조건을 참고하셔서 선택하시면 됩니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C067">
<history>
사용자: 신용대출 금리 낮은 곳 알려줘
에이전트: 신용점수 700점 기준 신용대출 상품 3건을 안내드립니다.
</history>
<question>신용점수 850점이면 어떻게 돼?</question>
<expected_behavior>
- 850점 기준으로 다시 안내한다
- 대출 승인이나 한도를 확정하는 표현을 쓰지 않는다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "수협은행",
  "product_name": "개인신용대출",
  "loan_type": "일반신용대출",
  "credit_score_band": "801~900점",
  "interest_rate": 5.18
 },
 {
  "bank_name": "아이엠뱅크",
  "product_name": "장기카드대출",
  "loan_type": "장기카드대출(카드론)",
  "credit_score_band": "801~900점",
  "interest_rate": 5.19
 },
 {
  "bank_name": "농협은행주식회사",
  "product_name": "가계신용대출(마이너스대출)",
  "loan_type": "마이너스한도대출",
  "credit_score_band": "801~900점",
  "interest_rate": 5.7
 }
]
</source_data>
<answer>
신용점수가 850점이면, 여러 은행에서 신용점수 801~900점 구간에 해당하는 대출 상품을 이용할 수 있습니다. 예를 들어,

- 수협은행의 개인신용대출(일반신용대출)은 5.18%의 금리로 이용할 수 있습니다.
- 아이엠뱅크의 장기카드대출(카드론)은 5.19%의 금리로 제공됩니다.
- 농협은행의 가계신용대출(마이너스대출)은 5.7%의 금리로 이용 가능합니다.

즉, 850점이면 위와 같은 금리로 대출 상품을 이용할 수 있습니다.

※ 실제 가입 조건과 금리는 상품설명서·약관 확인 후 최종 확정됩니다. 자세한 사항은 영업점 또는 고객센터에 문의하세요.
</answer>
</case>

<case id="C068">
<history>
사용자: 달러 환율 알려줘
에이전트: 현재 USD/KRW 환율은 1,390원입니다.
</history>
<question>한 번 더 조회해줄래?</question>
<expected_behavior>
- 환율을 다시 조회해 기준일과 함께 안내한다
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

<case id="C069">
<history>
사용자: 전세자금대출 금리 낮은 곳 알려줘
에이전트: 전세자금대출 상품 3건을 안내드립니다.
</history>
<question>그중에 국민은행 것만 보여줘</question>
<expected_behavior>
- 국민은행 전세자금대출을 안내하거나, 조회되지 않으면 그렇다고 밝힌다
</expected_behavior>
<source_data>
[조회 결과 1]
[
 {
  "bank_name": "국민은행",
  "product_name": "KB주택전세자금대출",
  "lend_rate_min": 4.21,
  "lend_rate_max": 5.61
 },
 {
  "bank_name": "국민은행",
  "product_name": "KB플러스전세자금대출",
  "lend_rate_min": 4.22,
  "lend_rate_max": 5.62
 }
]
</source_data>
<answer>
국민은행의 전세자금대출 상품은 다음과 같습니다.

1. KB주택전세자금대출: 금리는 연 4.21%에서 5.61%입니다.
2. KB플러스전세자금대출: 금리는 연 4.22%에서 5.62%입니다.
</answer>
</case>

<case id="C070">
<history>
사용자: 예금거래기본약관은 고객이 볼 수 있어?
에이전트: 네, 영업점에서 영업시간 중 볼 수 있습니다.
</history>
<question>교부도 요청할 수 있어?</question>
<expected_behavior>
- 약관 교부 청구 가능 여부를 약관 근거로 안내한다
- 문서에 없는 조항 번호·기한·수치를 지어내지 않는다
</expected_behavior>
<source_data>
[문서 1] 예금거래기본약관.txt
## Page 1 *이 약관은 금융소비자보호에 관한 법률 등 관련 법령 및 당행의 내부통제기준에 따른 절차를 거쳐 제공됩니다. - 1 - 예금거래기본약관 이 예금거래기본약관(이하 “약관”이라 한다)은 우리은행(이하 “은행”이라 한다)과 거래처 (또는 예금주)가 서로 믿음을 바탕으로 예금거래를 빠르고 틀림 없이 처리하는 한편, 서 로의 이해관계를 합리적으로 조정하기 위하여 기본적이고 일반적인 사항을 정한 것이다. 은행은 이 약관을 영업점에 놓아두고, 거래처는 영업시간 중 언제든지 이 약관을 볼 수 있고 또한 그 교부를 청구할 수 있다.

[문서 2] 예금거래기본약관.txt
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

[문서 3] 금융상품 설명의무의 합리적 이행을 위한 가이드라인.txt
## Page 11 참고 4 약관상 중요한 내용 관련 판례(대법원 2016다276177) 설명의무의 대상이 되는 ‘중요한 내용’은 사회통념에 비추어 고객 이 계약체결의 여부나 대가를 결정하는 데 직접적인 영향을 미칠 수 있 는 사항을 말한다. 사업자에게 약관의 명시·설명의무를 요구하는 것 은 어디까지나 고객이 알지 못하는 가운데 약관의 중요한 사항이 계 약 내용으로 되어 고객이 예측하지 못한 불이익을 받게 되는 것을 피 하고자 하는 데 근거가 있다. 따라서 약관에 정하여진 사항이라고 하더 라도 거래상 일반적이고 공통된 것이어서 고객이 별도의 설명 없이도 충 분히 예상할 수 있었던 사항이거나 이미 법령에 의하여 정하여진 것을 되풀이하거나 부연하는 정도에 불과한 사항이라면, 그러한 사항에 대하 여서까지 사업자에게 설명의무가 있다고 할 수는 없다. 사업자의 설명의무를 면제하는 사유로서 ‘거래상 일반적이고 공통된 것’이라는 요건은 해당 약관 조항이 거래계에서 일반적으로 통용되고 있는지의 측면에서, ‘고객이 별도의 설명 없이도 충분히 예상할 수 있는 사항’인지는 소송당사자인 특정 고객에 따라 개별적으로 예측가능성이 있었는지의 측면에서 각 판단되어야 한다. 다음으로 약관에 정하여진 사항이 ‘이미 법령에 의하여 정하여진 것을 되풀이하거나 부연하는 정도에 불과한지’는 약관과 법령의 규정 내용, 법령의 형식 및 목적과 취지, 해당 약관이 고객에게 미치는 영향 등 여 러 가지 사정을 종합적으로 고려하여 판단하여야 한다. 여기에서 말하 는 ‘법령’은 일반적인 의미에서의 법령, 즉 법률과 그 밖의 법규명 령으로서의 대통령령, 총리
령, 부령 등을 의미하고, (중략) 대외적 구 속력이 인정되지 않는 행정규칙으로서의 고시는 (중략) 사업자의 설명 의무가 면제된다고 할 수 없다.

[문서 4] 예금거래기본약관.txt
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
</source_data>
<answer>
네, 문서에 따르면 고객(거래처)은 영업시간 중 언제든지 예금거래기본약관을 볼 수 있고, 또한 그 교부를 청구할 수 있습니다. 따라서 고객이 예금거래기본약관의 교부를 요청할 수 있습니다.
</answer>
</case>
