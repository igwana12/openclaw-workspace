# OpenClaw Workspace

Multi-repository workspace for OpenClaw and Timon Capital projects, integrated with Slack for task coordination.

## Context

This workspace receives tasks via Slack threads. Each thread maps to a feature branch and potentially a PR. The Slack thread URL should be included in commits and PR descriptions for traceability.

## Git Conventions

### Branch Naming
- Feature branches: `claude/<description>-<session-id>`
- Always push with `-u origin <branch-name>`

### Commit Messages
- First line: imperative mood, under 72 chars (e.g., "Add user authentication")
- Body: explain *why*, not *what* (the diff shows what)
- Include Slack thread URL when work originated from Slack
- End with session URL: `https://claude.ai/code/session_<id>`

### Pull Requests
- Title: concise, under 70 chars
- Body format:
  ```
  ## Summary
  <1-3 bullet points>

  ## Test plan
  <checklist>

  Slack thread: <url>
  ```

## Available Skills

Use these for common workflows:

| Skill | When to Use |
|-------|-------------|
| `/slack-to-pr` | Convert current Slack thread context into a PR |
| `/audit-setup` | Run maturity audit against the 5-level framework |
| `/standup` | Summarize recent work across the workspace |

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | This file - workspace conventions and context |
| `CLAUDE-CODE-MATURITY-AUDIT.md` | Audit checklist and action plan |
| `TIMON-CAPITAL-ANALYSIS.md` | Timon Capital strategy analysis |

## Active Hooks

Configured in `.claude/settings.json`:

| Hook | Event | What It Does |
|------|-------|--------------|
| Commit reminder | PreToolUse (git commit) | Reminds to include Slack thread URL |
| PR verification | PostToolUse (gh pr create) | Confirms Slack thread is linked |
| Session context | SessionStart | Shows available skills and points here |

## Principles

1. **Traceability**: Every change links back to its Slack origin
2. **Integration**: Skills read conventions from this file, hooks enforce them
3. **Simplicity**: Don't over-engineer; solve the task at hand

## Maturity Level

Current: **Level 4 (Integrated Systems)**

- CLAUDE.md defines conventions
- Skills reference CLAUDE.md for formatting
- Hooks enforce CLAUDE.md conventions
- Everything talks to everything

Next: Level 5 requires self-improving behaviors (skills that generate skills, hooks that update this file).
