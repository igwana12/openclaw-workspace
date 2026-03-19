# Tools Registry

Central catalog of MCP servers, integrations, and capabilities available to OpenClaw.

## Core Stack

| Tool | Type | Purpose | Status |
|------|------|---------|--------|
| Claude Code | Runtime | AI execution environment, skill system, hooks | Active |
| GitHub MCP | MCP Server | Repo management, PRs, issues | Active |
| Slack MCP | MCP Server | Message reading, thread context, posting | Active |
| File System | MCP Server | Read/write workspace files | Active |

## MCP Server Details

### GitHub (`github`)
- **Capabilities:** Read repos, create branches, commit, PR management, issue tracking
- **Auth:** OAuth via Claude Code
- **Used by:** All development workflows, PR review skills

### Slack (`slack`)
- **Capabilities:** Read channels/threads, post messages, react, file upload
- **Auth:** OAuth via Claude Code
- **Used by:** Video ingestion trigger, conversation capture, notification skills

### File System (`filesystem`)
- **Capabilities:** Read/write files in workspace
- **Auth:** Local filesystem access
- **Used by:** All skills that produce artifacts

## Skills Using Tools

| Skill | Tools Required | Description |
|-------|---------------|-------------|
| (future) video-ingest | Slack, Filesystem | Capture video links, transcribe, summarize, file |
| (future) pr-review | GitHub | Review PRs, suggest changes, approve |
| (future) slack-capture | Slack, Filesystem | Save conversations to workspace |

## Adding New Tools

When adding an MCP server:

1. **Document here first** — add to the table with purpose and auth method
2. **Configure in Claude** — add to `.mcp.json` or project settings
3. **Test capabilities** — verify what it can/cannot do
4. **Update skills** — note which skills can now use this tool

## Tool Selection Guidelines

- **GitHub tasks** → Use GitHub MCP (not raw git commands when possible)
- **Slack context** → Use Slack MCP to read threads before responding
- **File operations** → Prefer MCP filesystem for audit trail
- **Web fetching** → Use WebFetch tool for public URLs

## Known Limitations

| Tool | Limitation | Workaround |
|------|-----------|------------|
| Slack MCP | Cannot access private channels without invite | Request access or use shared channels |
| GitHub MCP | Rate limited on large repos | Batch operations, use caching |
| WebFetch | No authenticated URLs | Use specialized MCP for private resources |
