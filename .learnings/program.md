# Self-Improving Agent Program

> Based on [Karpathy's autoresearch](https://github.com/karpathy/autoresearch) pattern applied to Claude Code skills

## Overview

This system treats Claude Code as a scientific researcher whose experiments are its own capabilities. The agent identifies tweakable variables, runs experiments autonomously, compares results against baseline KPIs, and keeps improvements while discarding failures.

## KPIs to Optimize

| KPI | Description | Target | Weight |
|-----|-------------|--------|--------|
| `activation_rate` | % of relevant prompts that trigger the correct skill | > 90% | 3 |
| `output_quality` | Binary assertion pass rate | > 95% | 3 |
| `execution_time` | Time to complete skill | < 30s | 1 |
| `cost_efficiency` | Tokens used per successful execution | Minimize | 2 |
| `error_rate` | % of executions that fail | < 5% | 2 |

## Two-Layer Optimization

### Layer 1: Activation Optimization
Optimizes skill YAML descriptions and trigger patterns for better activation.

**Variables:**
- Skill name
- Description text
- Trigger keywords
- WHEN/WHEN NOT conditions

**Evaluation:** Run 10 test prompts, measure activation rate

### Layer 2: Quality Optimization
Uses Karpathy-style eval loop with binary assertions to optimize actual skill quality.

**Variables:**
- System prompt components
- Tool selection logic
- Output formatting
- Error handling

**Evaluation:** Run assertions in `/evals/` directory

## Cost Guardrails

| Limit | Value | Action |
|-------|-------|--------|
| Soft limit | $10/day | Log warning, continue |
| Hard limit | $50/day | Stop all experiments, alert |
| Per-experiment | $2 | Abort experiment |

## Safety Blockers (Weight 3)

These assertions **hard-reject** any experiment that fails them:

- `stop_loss_present`: Trading skills must include stop-loss logic
- `position_sizing_valid`: Max position size must be enforced
- `max_drawdown_check`: Drawdown limits must be validated
- `no_secrets_exposed`: No API keys or secrets in output
- `no_destructive_git`: No force-push, reset --hard, or branch deletion

## Experiment Cadence

| Type | Frequency | Time | Description |
|------|-----------|------|-------------|
| Nightly | Daily | 02:00 AM ET | Full experiment suite |
| Quick | On-demand | Any | Single skill test |
| Baseline | Weekly | Sunday 00:00 | Refresh baseline metrics |

## Priority Stack

1. **video-ingestor** - Most concrete, easiest to validate
2. **slack-to-pr** - High usage, clear success criteria
3. **standup** - Daily use, fast feedback loop
4. **audit-setup** - Meta-skill, improves other skills

## Experiment Workflow

```
1. SELECT skill from priority stack
2. LOAD current baseline metrics
3. GENERATE variation (tweak one variable)
4. RUN assertions against variation
5. COMPARE results to baseline
6. IF improvement > threshold:
     LOG to PROMOTIONS.md
     UPDATE skill with variation
   ELSE:
     LOG to EXPERIMENTS.md (with learnings)
7. UPDATE LEARNINGS.md with insights
8. REPEAT
```

## Integration Points

- **CLAUDE.md**: Reads conventions, updates based on learnings
- **Skills**: Target of optimization, read from `.claude/commands/`
- **Hooks**: Enforce safety, trigger experiments
- **Slack**: Report results via `--report-to-slack`
- **Extreme Pro Drive**: Primary data store at `/Volumes/Extreme Pro/`

## External Storage: Extreme Pro SSD

The Extreme Pro (4TB ExFAT) is the canonical source of truth for skills, configs, and data.

| What | Path on Drive |
|------|---------------|
| Existing skill definitions | `/Volumes/Extreme Pro/SKILLS/` |
| Video ingestor assets | `/Volumes/Extreme Pro/video injestor/` |
| OpenClaw documentation | `/Volumes/Extreme Pro/DOCS/OpenClaw/` |
| AI workspace / projects | `/Volumes/Extreme Pro/AI_WORKSPACE/` |
| Configuration files | `/Volumes/Extreme Pro/CONFIG/` |
| Best practices reference | `/Volumes/Extreme Pro/BEST PRACTICES/` |
| Infrastructure scripts | `/Volumes/Extreme Pro/INFRASTRUCTURE/` |
| API keys (SENSITIVE) | `/Volumes/Extreme Pro/API_KEYS/` |

### Rules
1. **Check the drive first** before creating new skills or configs
2. **Sync promoted experiments** back to `SKILLS/` on the drive
3. **NEVER expose** contents of `API_KEYS/` or `Investments/`
4. **Load existing baselines** from the drive if available

## The 10 Commandments

1. Never exceed hard cost limit
2. Always run `--dry-run` first on new experiments
3. Weight-3 safety blockers are non-negotiable
4. Log everything - gains compound over time
5. One variable per experiment
6. Baseline before variation
7. Minimum 3 runs per variation (reduce noise)
8. Promote only if improvement > 10%
9. Review failures for learnings
10. Never modify production skills during market hours

## File Locations

| File | Purpose |
|------|---------|
| `.learnings/program.md` | This file - master spec |
| `.learnings/run-experiment.py` | Experiment runner |
| `.learnings/EXPERIMENTS.md` | All experiment logs |
| `.learnings/LEARNINGS.md` | Insights and patterns |
| `.learnings/ERRORS.md` | Failed experiments |
| `.learnings/FEATURE_REQUESTS.md` | Ideas for new experiments |
| `.learnings/PROMOTIONS.md` | Successful improvements |
| `/evals/*.yaml` | Assertion files per skill |
