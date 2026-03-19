# Scenario Analysis Matrix

**Version:** v1
**Last used:** 2026-03-17 (Timon portfolio returns)
**Status:** Working

## When to Use

When evaluating outcomes with significant uncertainty. Works for: portfolio valuations, deal outcomes, recovery scenarios, strategic decisions with multiple paths.

## The Prompt

```
I need a scenario analysis for: [situation]

Key variables:
- [list the 2-3 things that most affect outcome]

Current state:
- [relevant baseline numbers]

Please produce:
1. Bull / Base / Bear case definitions with probability estimates
2. For each case: key assumptions, expected value, what triggers it
3. Actions matrix: what to do now vs. what to monitor vs. what triggers action
4. Summary: which case to plan for, which to hedge against
```

## Example Output Structure

```
### Bull Case (Omni >$1B):
- Omni position worth $80-100M on $7.5M invested
- Top-decile African fund, competitive globally
- Probability: X%

### Base Case (Omni $400-600M):
- Omni position worth $30-50M
- Solid African fund performance
- Probability: Y%

### Bear Case (Omni <$250M):
- Portfolio struggles to return principal
- Probability: Z%
```

## What Works

- Naming scenarios by the key variable (e.g., "Omni >$1B") makes them concrete
- Probability estimates force calibration even if rough
- "What triggers it" section prevents passive waiting
- Actions matrix separates "do now" from "monitor" from "if X then Y"

## Variations

**For recovery situations:** Add "Recovery actions" column to matrix showing effort/probability/expected value for each option (see Waza analysis in TIMON-CAPITAL-ANALYSIS.md)

**For time-sensitive decisions:** Add "Decision deadline" and "Cost of waiting" to each scenario
