# LP Update Communication

**Version:** v1
**Last used:** 2026-03-17 (Brighton/Timon)
**Status:** Working

## When to Use

When you need to communicate portfolio status, capital return options, or situation updates to LPs. Works for quarterly updates, ad-hoc situations, and recovery scenarios.

## The Prompt

```
I need to draft an LP communication. Context:

Fund: [fund name]
LP: [LP name and relationship context]
Situation: [what's happening - capital return, write-down, liquidity event, etc.]

Key data points:
- [list relevant numbers: NAV, positions, cash, obligations]

Please produce:
1. Options analysis with pros/cons for each path
2. Recommendation with reasoning
3. Messaging framework - the actual language to use with this LP
4. Action items with timeline

Tone should be: direct, transparent about risks, confident about path forward.
```

## Example Output Structure

See `TIMON-CAPITAL-ANALYSIS.md` for full example. Key sections:

- **Options table** with clear tradeoffs
- **Recommendation** leading with the action, then justification
- **LP Messaging Framework** — actual quotable language
- **Action Items** split by timeline (immediate / 30-day / ongoing)

## What Works

- Leading with options before recommendation lets LP feel ownership of decision
- Explicit pros/cons prevent "why didn't you consider X" conversations
- Quotable messaging framework saves drafting time later
- Timeline-based action items create accountability

## What to Avoid

- Don't bury bad news — lead with situation, then pivot to options
- Don't over-explain legal complexity — summarize, offer detail if asked
- Don't promise specific amounts without hedging ("~$X" or "up to $X")
