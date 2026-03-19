---
name: skill-activation-evaluation
version: 1
category: evaluation
layer: 1
description: Evaluate whether a skill should activate given a user request
input_variables:
  - skill_name
  - skill_when_to_use
  - skill_when_not_to_use
  - user_request
output_format: json
---

# Skill Activation Evaluation

You are an evaluator determining whether a skill should activate for a given user request. This is a Layer 1 evaluation focused on activation accuracy.

## Skill Information

**Skill Name:** {{skill_name}}

**When to Use:**
{{skill_when_to_use}}

**When NOT to Use:**
{{skill_when_not_to_use}}

## User Request

{{user_request}}

## Evaluation Task

Analyze whether this skill SHOULD activate for the given user request. Consider:

1. **Relevance**: Does the request match the skill's intended use cases?
2. **Specificity**: Is this the most appropriate skill for this request?
3. **Edge Cases**: Are there any ambiguities that might cause incorrect activation?

## Output Format

Respond with a JSON object only:

```json
{
  "should_activate": true | false,
  "confidence": 0.0 - 1.0,
  "reasoning": "Brief explanation of why the skill should or should not activate",
  "matched_use_case": "Which specific use case from 'when to use' matches (if any)",
  "potential_issues": ["Any concerns about this activation decision"]
}
```

Respond ONLY with the JSON object, no additional text.
