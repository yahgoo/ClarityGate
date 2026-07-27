Here is WorkBuddy's Coach 1 output for TC01. Translate to English if needed, then tell me:
1. Did it correctly flag "fast" as a vague adjective?
2. Did it stay within Coach 1's role (no EARS grammar comments)?
3. Is the JSON format correct?

Expected flags for this test case: vague adjective (fast); no measurable threshold; missing EARS trigger keyword.

{
  "coach": "Coach 1 - Ambiguity Hunter",
  "requirement_id": "TC01",
  "flags": [
    {
      "type": "vague adjective",
      "excerpt": "fast",
      "explanation": "'Fast' is unmeasurable. It provides no quantifiable threshold, so different stakeholders will interpret it differently and no test can verify compliance."
    }
  ],
  "severity": "high",
  "suggested_rewrite": "The system shall process orders within 2 seconds during peak load."
}