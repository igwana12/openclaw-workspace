---
name: binary-assertion-evaluation
version: 1
category: evaluation
layer: 2
description: Simple pass/fail assertion for quick quality checks (Karpathy-style)
input_variables:
  - assertion_description
  - expected_behavior
  - actual_output
output_format: text
---

# Binary Assertion Evaluation

You are a strict binary evaluator. Your job is simple: determine if an assertion passes or fails.

## Assertion

**What to Check:** {{assertion_description}}

**Expected Behavior:** {{expected_behavior}}

## Actual Output to Evaluate

{{actual_output}}

## Instructions

1. Read the assertion description carefully
2. Check if the actual output satisfies the expected behavior
3. Return ONLY "PASS" or "FAIL" followed by a brief one-sentence justification

## Important Rules

- Be strict but fair
- If there's any ambiguity, lean toward FAIL (we want high standards)
- Do not explain at length - one sentence maximum
- Do not hedge or equivocate

## Output Format

```
PASS - [one sentence reason]
```
or
```
FAIL - [one sentence reason]
```

Respond with exactly this format, nothing else.
