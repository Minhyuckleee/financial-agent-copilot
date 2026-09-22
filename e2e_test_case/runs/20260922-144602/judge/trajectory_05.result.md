<case id="C021">
<evidence>
- Route product_recommendation fits a request for low-rate mortgage recommendations.
- The single call to recommend_mortgage_loan_products had no filter and returned 3 results with no error.
- A prohibited_terms guardrail ran, then finalize.
- The answer ranks the 3 products by their lowest rate. It is logical and efficient.
</evidence>
<result>PASS</result>
</case>

<case id="C022">
<evidence>
- Route product_recommendation, then the tool call with bank_name_filter "신한" matches the bank named in the query.
- Returned 2 results with no error.
- A numeric_self_check guardrail ran before finalize.
- The answer lists both Shinhan products and their rate ranges. The path is direct.
</evidence>
<result>PASS</result>
</case>

<case id="C023">
<evidence>
- Route, then a filtered tool call with "하나은행", matches the question.
- Returned 1 result with no error.
- No guardrail triggered, then finalize.
- The answer confirms the product exists and gives its rate range. Minimal and coherent.
</evidence>
<result>PASS</result>
</case>

<case id="C024">
<evidence>
- An implicit mortgage-rate question was routed to product_recommendation. The tool was called unfiltered and returned 3 results.
- One tool call, no guardrail, finalize.
- The answer compares the 3 products and tells the user to consult banks. It progresses logically.
</evidence>
<result>PASS</result>
</case>

<case id="C025">
<evidence>
- A bank-by-bank comparison request got an unfiltered tool call, which is correct for getting several banks. It returned 3 results.
- No errors, no redundant steps, then finalize.
- The answer lists each bank's rate range. Goal achieved efficiently.
</evidence>
<result>PASS</result>
</case>
