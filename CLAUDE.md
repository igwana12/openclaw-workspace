# OpenClaw Workspace

## What This Is

This is the operational workspace for OpenClaw — an AI-native system built on Claude Code, integrated with Slack, MCP servers, and a growing library of skills. It supports investment analysis, content ingestion, and workflow automation for igwana12.

## How The Pieces Connect

```
Slack (commands, threads, conversations)
  ↓
Claude Code (skills, hooks, agents)
  ↓
MCP Servers (GitHub, Slack, file systems)
  ↓
This Workspace (artifacts, analysis, knowledge)
```

### Core Capabilities
- **Slack-native interaction** — conversations trigger skills, ingest content, produce analysis
- **Video ingestion** — TikTok/video links get transcribed, summarized, skill-filed, and indexed
- **Investment analysis** — LP communications, portfolio modeling, scenario analysis
- **Skill system** — reusable AI SOPs that define how to handle specific tasks

## AI OS Framework (from Thaddeus Demeke)

We use this as our organizing principle. Current status:

| Asset | Status | Where It Lives |
|-------|--------|----------------|
| **Playbooks** (the what & why) | This file | `CLAUDE.md` |
| **SOPs** (human instructions) | Partial | Slack threads, conversations |
| **AI SOPs** (skills for Claude) | Active | Skill files (.md) in skills directories |
| **Knowledge Base** (reference docs) | Growing | This workspace, `index.json` files |
| **Prompt Library** (versioned prompts) | Active | `prompts/` directory |
| **Tools Registry** (tech stack catalog) | Active | `TOOLS.md` |
| **Projects & Workflows** (live implementations) | Partial | Scattered across repos |

## Principles

1. **Process before tools.** Document the *why* before automating the *how*.
2. **Make the invisible visible.** If a workflow lives only in someone's head, write it down so Claude can run it.
3. **Skills are AI SOPs.** Every repeatable task should become a skill with clear inputs, steps, and outputs.
4. **Don't over-engineer.** A working skill beats a perfect architecture. Ship, then refine.
5. **Write down what works.** When a prompt, approach, or workflow succeeds, capture it. Stop re-learning.

## Decision Log

| Date | Decision | Reasoning |
|------|----------|-----------|
| 2026-03-17 | Created Timon Capital analysis in workspace | Needed structured LP communication framework for Brighton return + Waza recovery |
| 2026-03-19 | Adopted AI OS framework as organizing principle | Video from Thaddeus Demeke mapped cleanly to what we're already building — gives us a shared vocabulary and gap analysis |
| 2026-03-19 | Created CLAUDE.md as single source of truth | Highest-leverage action: one file that orients every future Claude session on what this system is and how it works |
| 2026-03-19 | Built `prompts/` directory with initial library | Extracted working prompts from Timon analysis: LP updates, scenario matrices, options analysis. Now versioned and reusable. |
| 2026-03-19 | Created `TOOLS.md` and `SKILLS.md` | Centralized tools registry and formalized the 3x rule for skill creation. AI OS framework now 5/7 assets active. |

## What's Next

- [x] Build `prompts/` directory — version prompts that work well so they survive across sessions
- [x] Centralize tools registry — `TOOLS.md` lists all MCP servers, capabilities, and which skills use them
- [x] Formalize the skill creation workflow — `SKILLS.md` defines the 3x rule and skill anatomy
- [ ] Connect the decision log to Slack — decisions made in threads should flow back here

## For Future Claude Sessions

When you start a new session in this workspace:
1. Read this file first
2. Check the decision log for recent context
3. Don't rebuild what exists — extend it
4. If you learn something new, add it to this file before the session ends
