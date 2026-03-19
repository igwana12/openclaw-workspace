# Standup

Generate a quick summary of recent work for daily standup.

## Instructions

1. Check recent git commits (last 24 hours or since last standup)
2. Summarize what was accomplished
3. Identify any blockers
4. List next priorities

## Output Format

```
## Yesterday
- <completed items from git log>

## Today
- <planned work based on context>

## Blockers
- <any issues blocking progress, or "None">
```

## Context Sources

- `git log --oneline --since="24 hours ago"`
- Open PRs: `gh pr list --author @me`
- Recent Slack threads if available

## Keep It Concise

- Under 500 words
- Bullet points preferred
- Focus on outcomes, not activities
