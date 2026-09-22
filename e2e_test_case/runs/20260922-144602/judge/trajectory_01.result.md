<case id="C001">
<evidence>
- route -> recommend_deposit_products -> guardrail -> finalize: logical order, no wasted steps
- save_term_months=12 assumed although the user gave no term; a reasonable default
- tool returned 3 results, but the final output opens with "그 외에도" and names only 2 products; the first (top) recommendation is missing
- the final answer is cut off and incoherent, so the trajectory does not deliver the recommendation it was built for
</evidence>
<result>FAIL</result>
</case>

<case id="C002">
<evidence>
- routed to product_recommendation; tool called with save_term_months=6, matching "6개월"
- 3 results returned and all 3 presented with base and preferential rates
- disclosure guardrail applied, then finalized; efficient and complete
</evidence>
<result>PASS</result>
</case>

<case id="C003">
<evidence>
- "2년" mapped to save_term_months=24
- 3 results, listed and compared, with the highest rate named
- guardrail then finalize; clear progression, no redundant calls
</evidence>
<result>PASS</result>
</case>

<case id="C004">
<evidence>
- bank_name_filter="우리" matches the user's request for Woori Bank; no term forced
- 1 result returned and presented accurately
- guardrail then finalize; efficient
</evidence>
<result>PASS</result>
</case>

<case id="C005">
<evidence>
- both constraints mapped: save_term_months=36 and bank_name_filter="하나"
- 1 result, answered directly with base and max rate
- guardrail then finalize; single call, logical
</evidence>
<result>PASS</result>
</case>
