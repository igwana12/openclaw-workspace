# draft-lp-update

Draft LP communications based on current portfolio state and recent developments.

## When to Use
Invoke this skill when asked to:
- Draft an LP letter or update
- Prepare quarterly communications
- Summarize portfolio status for investors
- Communicate capital return plans

## Process

1. **Read all existing analysis docs** - Glob for `*-ANALYSIS.md` in repo root
2. **Extract key data points:**
   - Portfolio positions and valuations
   - Recent developments (positive and negative)
   - Upcoming liquidity events
   - Action items that affect LPs
3. **Draft communication** following tone guidelines

## Output Location
All drafts go to `drafts/` directory with naming: `LP-UPDATE-{YYYY-MM-DD}.md`

## Tone Guidelines
- Professional but direct
- Lead with portfolio performance context
- Be transparent about challenges (Waza-type situations)
- Frame write-downs alongside recovery optionality
- Emphasize monitoring and governance actions taken
- Include specific timelines for capital return where applicable

## Template Structure

```markdown
# LP Update: [Quarter/Date]

## Portfolio Summary
[High-level MOIC, key positions, concentration]

## Recent Developments
[Material changes since last update]

## Liquidity Outlook
[Expected events with timeline ranges]

## Capital Return
[Status of distributions, timing expectations]

## Watchlist Items
[Positions requiring attention, actions being taken]

---
*Questions? [Contact info]*
```

## Integration Notes
- References analysis docs created via `analyze-position` skill
- LP messaging frameworks from analysis docs should be incorporated
- Scenario analysis (Bull/Base/Bear) can be summarized for sophisticated LPs
