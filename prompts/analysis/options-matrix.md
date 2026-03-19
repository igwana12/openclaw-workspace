# Options Analysis Matrix

**Version:** v1
**Last used:** 2026-03-17 (Waza recovery options)
**Status:** Working

## When to Use

When you have 3-5 possible actions and need to choose one. Works for: tactical decisions, recovery strategies, resource allocation, vendor selection.

## The Prompt

```
I need to evaluate options for: [decision]

Context:
- [what led to this decision point]
- [constraints: time, money, relationships, etc.]

Options I'm considering:
1. [option A]
2. [option B]
3. [option C]

Please produce:
1. Matrix comparing: effort, probability of success, expected value, risks
2. For each option: 1-sentence summary of pro and con
3. Recommendation with reasoning
4. What would change the recommendation (sensitivity analysis)
```

## Example Output Structure

```
| Action | Effort | Probability | Expected Value |
|--------|--------|-------------|----------------|
| Continue litigation | High ($$$) | Low-Medium | Depends on X |
| Settle for equity | Low | High | $0 near-term, option value |
| Pressure via authorities | Medium | Low | Limited jurisdiction |
| Monitor and wait | Low | Unknown | Free option |
```

## What Works

- Effort/Probability/EV columns force quantification
- "What would change the recommendation" prevents false confidence
- One-sentence pro/con is easier to remember than paragraphs
- Including a "do nothing" option as baseline

## Common Patterns

**Recovery situations:** Lead with "pause active spend" options — burning money on low-probability recovery is usually wrong

**Negotiation:** Include "BATNA" (best alternative to negotiated agreement) as explicit option

**Time pressure:** Add "decision deadline" and "cost of delay" columns
