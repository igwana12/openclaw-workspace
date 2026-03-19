# Slack to PR

Convert the current Slack thread context into a GitHub pull request.

## Instructions

1. Check git status and ensure all changes are committed
2. Create or verify the correct branch (should start with `claude/`)
3. Push to remote if needed
4. Create PR with:
   - Title: Under 70 characters, descriptive
   - Body format:
     ```
     ## Summary
     <bullet points summarizing changes>

     ## Test plan
     <how to verify the changes work>

     <slack-thread-url from context>
     https://claude.ai/code/<session-id>
     ```

## Requirements

- MUST include Slack thread URL in PR body
- MUST use `--body` with HEREDOC for proper formatting
- Branch naming: `claude/slack-<description>-<session-id>`

## Example

```bash
gh pr create --title "feat: Add self-improving agent loop" --body "$(cat <<'EOF'
## Summary
- Added .learnings/ infrastructure with experiment runner
- Created eval assertions for 4 skills
- Set up CLAUDE.md with Level 5 integration

## Test plan
- [ ] Run `python .learnings/run-experiment.py --dry-run`
- [ ] Verify all eval files load correctly

https://claw-4m88313.slack.com/archives/C0AHPER2F8B/p1773949909569469
https://claude.ai/code/session_id_here
EOF
)"
```
