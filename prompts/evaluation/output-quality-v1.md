---
name: output-quality-evaluation
version: 1
category: evaluation
layer: 2
description: Evaluate the quality of a skill's output against expected criteria
input_variables:
  - skill_name
  - task_description
  - input_data
  - actual_output
  - quality_criteria
output_format: json
---

# Output Quality Evaluation

You are a quality evaluator assessing whether a skill's output meets the expected standards. This is a Layer 2 evaluation focused on output quality.

## Skill Information

**Skill Name:** {{skill_name}}

**Task Description:** {{task_description}}

## Input Provided to Skill

{{input_data}}

## Actual Output from Skill

{{actual_output}}

## Quality Criteria

{{quality_criteria}}

## Evaluation Task

Evaluate the output against each quality criterion. For each criterion, determine if it passes or fails.

Consider:
1. **Completeness**: Does the output address all required aspects?
2. **Accuracy**: Is the information correct and properly extracted/transformed?
3. **Format**: Does the output follow the expected structure?
4. **Usefulness**: Would this output be valuable to the user?

## Output Format

Respond with a JSON object only:

```json
{
  "overall_pass": true | false,
  "overall_score": 0.0 - 1.0,
  "criteria_results": [
    {
      "criterion": "criterion name",
      "pass": true | false,
      "reasoning": "Brief explanation"
    }
  ],
  "strengths": ["What the output does well"],
  "improvements": ["What could be improved"],
  "recommendation": "keep" | "discard" | "iterate"
}
```

Respond ONLY with the JSON object, no additional text.
