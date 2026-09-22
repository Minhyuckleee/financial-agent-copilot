<case id="E001">
<evidence>Routed to product_recommendation, which fits a deposit recommendation request.
First call used term 18 plus the 신한 filter and returned empty. The retry dropped the bank filter: one reasonable relaxation.
The second call was also empty, so the agent stopped via answer_tier2_exhausted with low_confidence instead of looping.
The final answer honestly says nothing was found. Efficient, logical progression.</evidence>
<result>PASS</result>
</case>

<case id="E002">
<evidence>Called recommend_deposit_products with term 9 and got an empty result.
One retry with relaxed args (no term) returned 3 results, which is the expected single retry.
Guardrail added the disclosure. The answer says there is no 9-month product and gives the relaxed alternatives.
Clear progression with no redundant steps.</evidence>
<result>PASS</result>
</case>

<case id="E003">
<evidence>The user's credit score of 1200 is outside the valid range (max 1000).
The agent silently clamped it to credit_score=1000 in the tool call, with no clarification step or validation note.
The final output says "신용점수 1200점에 해당하는 금리" as if 1200 were valid, which does not match the tool args used.
The input reinterpretation is hidden rather than surfaced, so the steps do not line up logically with the answer.</evidence>
<result>FAIL</result>
</case>

<case id="E004">
<evidence>Routed correctly, then made one call to recommend_jeonse_loan_products with the 토스뱅크 filter, which returned 1 result.
Guardrail ran and finalize_answer followed. It is a minimal, direct path.
The answer states the product and rate from that result.</evidence>
<result>PASS</result>
</case>

<case id="E005">
<evidence>"그 은행" was resolved to 국민은행 from history, and the product switched to credit loans as requested.
A single call to recommend_credit_loan_products with the 국민은행 filter returned 1 result.
Guardrail added the disclosure, then finalize ran. Efficient and logically coherent.</evidence>
<result>PASS</result>
</case>
