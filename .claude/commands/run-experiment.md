# Run Experiment

Trigger a self-improvement experiment cycle on a skill.

## Quick Start

```bash
# Dry run first (always!)
python .learnings/run-experiment.py --dry-run

# Establish baseline for a skill
python .learnings/run-experiment.py --baseline --skill video-ingestor

# Run experiment on specific skill
python .learnings/run-experiment.py --skill video-ingestor --verbose

# Full nightly run
python .learnings/run-experiment.py --report-to-slack
```

## Flags

| Flag | Description |
|------|-------------|
| `--dry-run` | Test without making changes |
| `--skill <name>` | Target specific skill |
| `--baseline` | Establish baseline metrics |
| `--report-to-slack` | Post results to Slack |
| `--verbose` | Detailed logging |

## How It Works

1. **Load** skill's eval assertions from `/evals/<skill>.yaml`
2. **Generate** variation by tweaking one variable
3. **Run** assertions 3x to reduce noise
4. **Compare** to baseline
5. **Promote** if improvement > 10%
6. **Log** everything

## Priority Stack

1. video-ingestor (most concrete)
2. slack-to-pr (high usage)
3. standup (daily feedback)
4. audit-setup (meta-skill)

## Cost Guardrails

- Soft limit: $10/day (warning)
- Hard limit: $50/day (stop)
- Per-experiment: $2 (abort)

## Safety Blockers

Weight-3 assertions that hard-reject experiments:
- stop_loss_present
- position_sizing_valid
- no_secrets_exposed
- no_destructive_git

## Instructions

When user asks to run experiments:
1. Always start with `--dry-run`
2. Establish baseline if none exists
3. Run verbose for first attempts
4. Check cost tracker status
5. Review results in EXPERIMENTS.md
