# OpenClaw Workspace

## Purpose
This is the working repository for **Timon Capital** analysis, LP communications, and portfolio management. Content includes investment memos, capital return analysis, legal strategy, and portfolio tracking.

## Conventions

### Document Standards
- All analysis documents use Markdown with clear section headers
- Financial figures use `$` prefix with comma separators (e.g., `$1,250,000`)
- Tables are used for structured data (positions, scenarios, action matrices)
- Every analysis document must include: date, context line, action items section
- Action items use `- [ ]` checkbox format with timeline categories (Immediate, Near-Term, Ongoing)

### File Organization
- Analysis documents live in the repo root as `{TOPIC}-ANALYSIS.md`
- Confidential/sensitive content should never be committed (no `.env`, credentials, API keys)
- Draft LP communications go in `drafts/` directory

### Tone & Style
- Professional but direct — this is internal strategy, not marketing
- Use scenario analysis (Bull/Base/Bear) for investment positions
- Include recommendation with clear rationale
- Flag legal vs. strategic vs. financial considerations separately

## Available Skills

### Project Skills (`.claude/skills/`)
- **`analyze-position`** — Structured analysis of an investment position or situation. Produces standardized output with exposure summary, options matrix, scenario analysis, and action items.
- **`draft-lp-update`** — Draft LP communications based on current portfolio state and recent developments. References existing analysis docs for consistency.

### Global Skills (`~/.claude/skills/`)
- **`session-start-hook`** — For setting up CI/dependency hooks in new repos

## Hooks

### Active Hooks
- **Stop Hook** (global): Ensures all changes are committed and pushed before session ends. Never lose work.
- **Pre-commit Hook** (project): Validates document structure before committing — checks for required sections (date, context, action items).

### How Hooks and Skills Connect
- When using the `analyze-position` skill, the output format is enforced by the pre-commit hook
- The stop hook ensures analysis work is always persisted to the remote
- LP drafts reference analysis docs, so the `draft-lp-update` skill reads existing analyses first

## Working Patterns

### When Creating New Analysis
1. Use the `analyze-position` skill for structured output
2. Reference existing analyses for consistency (check repo root for `*-ANALYSIS.md` files)
3. The pre-commit hook will validate structure before allowing commit

### When Updating LP Communications
1. Use the `draft-lp-update` skill
2. It will read all current analysis docs for context
3. Output goes to `drafts/` directory

### When Asked to Research or Monitor
- Track sources and dates for all claims
- Use action items format for follow-ups
- Flag anything requiring legal review explicitly
