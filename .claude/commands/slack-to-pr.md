# Slack to PR

Convert the current Slack thread context into a properly formatted pull request.

## Instructions

1. **Extract context** from the Slack thread:
   - What was requested?
   - What was the outcome?
   - What files were changed?

2. **Review commits** on the current branch:
   ```bash
   git log origin/master..HEAD --oneline
   git diff origin/master..HEAD --stat
   ```

3. **Create PR** following CLAUDE.md conventions:
   - Title: concise, under 70 chars, describes the change
   - Body: Summary bullets, test plan checklist, Slack thread link

4. **Use this format**:
   ```bash
   gh pr create --title "<title>" --body "$(cat <<'EOF'
   ## Summary
   - <bullet 1>
   - <bullet 2>

   ## Test plan
   - [ ] <verification step>

   Slack thread: <thread_url>

   https://claude.ai/code/session_<id>
   EOF
   )"
   ```

5. **Return the PR URL** to the user.

## Integration

This skill reads PR format conventions from `CLAUDE.md`. If conventions change there, this skill automatically follows them.
