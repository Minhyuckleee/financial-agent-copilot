<case id="C061">
<evidence>Weather question is unrelated to the stock domain; route_query correctly classifies it as out_of_scope.
Path route -> answer_out_of_scope -> finalize is minimal and logical, with no unnecessary tool calls.
The final output is a scope refusal, which matches the routing.</evidence>
<result>PASS</result>
</case>

<case id="C062">
<evidence>The request asks for a future price prediction; routing it to out_of_scope fits a no-prediction constraint.
Three steps in a clear progression, with no data fetching wasted on a prediction.
The final refusal is consistent with the route. (A softer redirect could have been offered, but the trajectory itself is coherent.)</evidence>
<result>PASS</result>
</case>

<case id="C063">
<evidence>The request is a buy recommendation on crypto; out_of_scope routing is appropriate (recommendation and non-stock asset).
Minimal route -> refusal -> finalize path, with no detours.
The final output matches the route.</evidence>
<result>PASS</result>
</case>

<case id="C064">
<evidence>Coding request is unrelated to the domain; correctly routed out_of_scope.
The rewritten query adds details (numbers, ascending) that are not in the input, but this has no effect on the path.
Efficient three-step path, and the output matches.</evidence>
<result>PASS</result>
</case>

<case id="C065">
<evidence>Travel recommendation is unrelated to the domain; correctly routed out_of_scope.
The rewrite adds "domestic", which is harmless because no downstream step uses it.
Minimal, logical path, and the final refusal is consistent.</evidence>
<result>PASS</result>
</case>
