<case id="C016">
<evidence>
- Routed to product_recommendation, matching a rate lookup for a specific bank.
- Called recommend_jeonse_loan_products once with bank_name_filter="국민은행"; no error, 2 results.
- Ran numeric_self_check before finalizing; the answer lists both KB products with rate ranges.
- Four steps in a clear order with no redundant calls.
</evidence>
<result>PASS</result>
</case>

<case id="C017">
<evidence>
- Routed to product_recommendation for a question about whether Woori Bank has these products.
- Called the tool once with bank_name_filter="우리은행"; 2 results, no error.
- Ran numeric_self_check, then finalized; the answer confirms the products exist and gives rates for both.
- Efficient, logical progression.
</evidence>
<result>PASS</result>
</case>

<case id="C018">
<evidence>
- Question about general rates, so the agent called the tool with no bank filter (null), which fits.
- 3 results, no error; the final answer summarizes the range from those results only.
- Guardrail list was empty even though the answer has numbers, but the steps still follow logically.
- Single tool call, no wasted steps.
</evidence>
<result>PASS</result>
</case>

<case id="C019">
<evidence>
- Asked for the single cheapest option; called the tool with no bank filter, 3 results.
- The answer ranks by minimum rate and says it is based only on the current lookup results.
- Guardrail list was empty, yet the answer names a "cheapest" pick from only 3 results; weak, but the trajectory itself is coherent.
- The steps are minimal and move toward the goal.
</evidence>
<result>PASS</result>
</case>

<case id="C020">
<evidence>
- Routed to product_recommendation; called the tool with bank_name_filter="농협", 3 results, no error.
- The answer lists all 3 NH products with rate ranges, matching the request.
- Guardrail list was empty, but the flow is logical and efficient.
</evidence>
<result>PASS</result>
</case>
