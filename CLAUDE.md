# OpenClaw Workspace

This is a Slack-integrated Claude Code workspace with self-improving capabilities.

## Maturity Level

**Current: Level 5 - Self-Improving Meta-Systems**

This workspace implements the Karpathy autoresearch pattern for autonomous skill improvement.

## Project Context

- **Integration:** Slack threads trigger Claude sessions
- **Primary use:** Converting Slack discussions to GitHub PRs, video processing, daily standups
- **Self-improvement:** Nightly experiments optimize skills automatically

## Git Conventions

### Branch Naming
- Feature branches: `claude/slack-<description>-<session-id>`
- Always push with `-u origin <branch>`

### Commit Format
```
<type>: <description>

<body>

<slack-thread-url>
https://claude.ai/code/<session-id>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

### PR Format
- Title: Under 70 characters
- Body: `## Summary` + `## Test plan` + Slack thread link

## Available Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| `/slack-to-pr` | "create pr", "pull request" | Convert Slack thread to PR |
| `/standup` | "standup", "daily update" | Summary of recent work |
| `/audit-setup` | "audit", "maturity level" | Run 5-level maturity assessment |
| `/run-experiment` | "run experiment", "optimize" | Trigger self-improvement cycle |

## Self-Improving Agent System

### Overview
The `.learnings/` directory contains the autoresearch infrastructure:

- `program.md` - Master optimization spec with KPIs and guardrails
- `run-experiment.py` - Experiment runner with `--dry-run`, `--baseline`, `--verbose`
- Log files: EXPERIMENTS, LEARNINGS, ERRORS, FEATURE_REQUESTS, PROMOTIONS

### KPIs Being Optimized
1. **Activation rate** (>90%) - Correct skill triggers on relevant prompts
2. **Output quality** (>95%) - Binary assertion pass rate
3. **Execution time** (<30s) - Speed of skill completion
4. **Cost efficiency** - Tokens per successful execution

### Cost Guardrails
- Soft limit: $10/day (warning)
- Hard limit: $50/day (stop)
- Per-experiment: $2 (abort)

### Safety Blockers (Weight 3)
These hard-reject any experiment:
- `stop_loss_present` - Trading skills must have stop-loss
- `position_sizing_valid` - Position limits enforced
- `no_secrets_exposed` - No API keys in output
- `no_destructive_git` - No force-push or reset --hard

### Running Experiments
```bash
# Establish baseline first
python .learnings/run-experiment.py --baseline --dry-run

# Run experiments on a specific skill
python .learnings/run-experiment.py --skill video-ingestor --verbose

# Full nightly run (02:00 AM ET)
python .learnings/run-experiment.py --report-to-slack
```

## Active Hooks

| Hook | Trigger | Action |
|------|---------|--------|
| Commit reminder | Before git commit | Remind to include Slack URL |
| PR verification | After gh pr create | Confirm Slack link present |
| Session start | Session start | Show available skills and current priorities |

## Integration Principles (Level 4+)

1. **CLAUDE.md defines conventions** - All agents read from here
2. **Skills reference CLAUDE.md** - Not hardcoded values
3. **Hooks enforce CLAUDE.md** - Automated compliance
4. **Experiments update CLAUDE.md** - Learnings propagate automatically

## The 10 Commandments

1. Never exceed hard cost limit ($50/day)
2. Always `--dry-run` first on new experiments
3. Weight-3 safety blockers are non-negotiable
4. Log everything - gains compound over time
5. One variable per experiment
6. Baseline before variation
7. Minimum 3 runs per variation (reduce noise)
8. Promote only if improvement > 10%
9. Review failures for learnings
10. Never modify production skills during market hours

## External Storage: Extreme Pro Drive

**IMPORTANT:** The Extreme Pro SSD is the primary data store. Always check it for existing assets before creating new ones.

- **Mount point (macOS):** `/Volumes/Extreme Pro/`
- **Type:** ExFAT, 4TB (2.34TB used, 1.66TB available)
- **Always available** when connected to the local machine

### Drive Map

```
/Volumes/Extreme Pro/
├── SKILLS/                    # Skill definitions and templates
├── MIGRATION/                 # Migration scripts and data
├── sacred-circuits-outputs/   # Sacred Circuits pipeline outputs
│   └── train_apollo_phase0.sh
├── BEST PRACTICES/            # Best practices documentation
├── Book Injestor/             # Book ingestion pipeline
├── PANTHEON_LOGS/             # Pantheon system logs
├── ACTIVE/                    # Active projects and work-in-progress
├── video injestor/            # Video ingestion pipeline assets
├── ARCHIVE/                   # Archived projects
├── PANTHEON_OUTPUT/            # Pantheon pipeline outputs
├── MYTHS/                     # Myths content/research
├── Sacred Circuits Global Media B.../  # Sacred Circuits media
├── CONTENT/                   # Content library
├── DOCS/                      # Documentation
│   └── OpenClaw/              # OpenClaw project docs
├── CONFIG/                    # Configuration files
├── RESOURCES/                 # Shared resources
├── INFRASTRUCTURE/            # Infrastructure configs and scripts
├── DATA/                      # Raw data storage
├── AI_WORKSPACE/              # AI projects workspace
├── Investments/               # Investment tracking (SENSITIVE)
├── API_KEYS/                  # API keys storage (SENSITIVE - never expose)
└── MANUALS/                   # Reference manuals
```

### Key Directories for This Workspace

| Purpose | Path |
|---------|------|
| Existing skills | `/Volumes/Extreme Pro/SKILLS/` |
| Video ingestor assets | `/Volumes/Extreme Pro/video injestor/` |
| OpenClaw docs | `/Volumes/Extreme Pro/DOCS/OpenClaw/` |
| AI workspace | `/Volumes/Extreme Pro/AI_WORKSPACE/` |
| Config files | `/Volumes/Extreme Pro/CONFIG/` |
| Best practices | `/Volumes/Extreme Pro/BEST PRACTICES/` |
| API keys | `/Volumes/Extreme Pro/API_KEYS/` (NEVER expose contents) |

### Rules

1. **Check Extreme Pro first** before creating new skills, configs, or data
2. **NEVER read or expose** contents of `API_KEYS/` or `Investments/` in outputs
3. **Sync learnings** back to the drive when promoting experiments
4. **Reference existing assets** from the drive rather than duplicating them

## File Structure

```
.
├── CLAUDE.md                    # This file - master config
├── .claude/
│   ├── settings.json            # Hooks configuration
│   └── commands/                # Skills
│       ├── slack-to-pr.md
│       ├── standup.md
│       ├── audit-setup.md
│       └── run-experiment.md
├── .learnings/
│   ├── program.md               # Master optimization spec
│   ├── run-experiment.py        # Experiment runner
│   ├── EXPERIMENTS.md           # All experiments
│   ├── LEARNINGS.md             # Insights
│   ├── ERRORS.md                # Failures
│   ├── FEATURE_REQUESTS.md      # Ideas
│   ├── PROMOTIONS.md            # Successful improvements
│   └── baselines/               # Baseline metrics per skill
└── evals/
    ├── video-ingestor.yaml      # Eval assertions
    ├── slack-to-pr.yaml
    ├── standup.yaml
    └── audit-setup.yaml
```
