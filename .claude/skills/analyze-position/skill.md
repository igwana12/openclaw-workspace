# analyze-position

Structured analysis of an investment position or situation.

## When to Use
Invoke this skill when asked to analyze:
- A portfolio company situation
- Capital return scenarios
- Legal/strategic options for a position
- Any investment-related decision requiring structured analysis

## Output Format

The analysis MUST follow this structure (enforced by pre-commit hook):

```markdown
# [Topic]: [Brief Description]

**Date:** [Current Date]
**Context:** [One-line summary of why this analysis exists]

---

## 1. [Primary Topic]

### Current Position
| Item | Amount/Status |
|------|---------------|
| ... | ... |

### Options Analysis

**Option A: [Name]**
- [Description]
- **Pro:** [Benefit]
- **Con:** [Drawback]

**Option B: [Name]**
...

### Recommendation
[Clear recommendation with rationale]

---

## 2. [Secondary Topic if applicable]
...

---

## Action Items

### Immediate (This Week)
- [ ] [Action item with owner if applicable]

### Near-Term (30 Days)
- [ ] [Action item]

### Ongoing
- [ ] [Monitoring/recurring item]

---

*Analysis prepared for internal discussion. Not legal or financial advice.*
```

## Integration Notes
- Output is validated by `.claude/hooks/pre-commit-validate.sh`
- Reference existing `*-ANALYSIS.md` files in repo root for consistency
- Use scenario analysis (Bull/Base/Bear) for valuation-dependent positions
- Separate legal vs. strategic vs. financial considerations
