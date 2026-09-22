<case id="C006">
<evidence>
- route=product_recommendation matches a deposit-recommendation request
- recommend_deposit_products with save_term_months=12 is a reasonable default term; no error, 3 results
- guardrail (disclosure_missing, prohibited_terms) ran, then finalize: 4 steps, no wasted calls
- final text says "다음과 같습니다" but lists no products; that is a finalization/answer-quality issue, not a step-sequence issue
</evidence>
<result>PASS</result>
</case>

<case id="C007">
<evidence>
- route=product_recommendation, then recommend_deposit_products with save_term_months=12, matching "1년 만기"
- no error, 3 results; guardrail and finalize follow in order
- efficient linear progression with no redundant calls
- final text starts mid-list ("그 다음으로는") and looks truncated; that is answer quality, while the trajectory itself is sound
</evidence>
<result>PASS</result>
</case>

<case id="C008">
<evidence>
- route=product_recommendation fits the question
- recommend_credit_loan_products with no args is fine because the user gave no credit score; 3 results
- guardrail then finalize; the answer states which score band it assumed (601~700)
- logical, minimal sequence
</evidence>
<result>PASS</result>
</case>

<case id="C009">
<evidence>
- route=product_recommendation
- recommend_credit_loan_products with credit_score=900 passes the user's score through correctly; 3 results
- guardrail then finalize; the answer is framed on the 900-point condition
- clean, efficient progression
</evidence>
<result>PASS</result>
</case>

<case id="C010">
<evidence>
- user said "600점대 초반" (about 600-650), but the tool was called with credit_score=600
- the tool returned the 501~600 band, and the final answer explicitly says the rates are for "501~600점 구간"
- this band does not match the user's stated range (600대 → 601~700 band); the agent did not notice or re-query
- the argument choice sent the tool to the wrong data slice, so later steps do not logically serve the goal
</evidence>
<result>FAIL</result>
</case>
