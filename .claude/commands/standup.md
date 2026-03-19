# Standup

Summarize recent work across the workspace for a quick status update.

## Instructions

1. **Gather recent activity**:
   ```bash
   # Recent commits (last 7 days)
   git log --since="7 days ago" --oneline --all

   # Current branch status
   git status --short

   # Open PRs (if gh available)
   gh pr list --state open 2>/dev/null || echo "No gh CLI or no PRs"
   ```

2. **Summarize in standup format**:

   ```markdown
   ## Standup - <date>

   ### Done
   - <completed work from commits>

   ### In Progress
   - <uncommitted changes, open branches>

   ### Blocked/Next
   - <any blockers or planned next steps>
   ```

3. **Keep it brief** - This is a quick status, not a detailed report.

## Integration

Uses git conventions from `CLAUDE.md` to interpret commit messages and branch names.
