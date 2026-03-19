---
name: self-improving-agent
version: 1.0.0
description: Autonomous self-improvement loop based on Karpathy's autoresearch pattern
category: ai-os
triggers:
  - /self-improve
  - /improve
  - /experiment
author: OpenClaw AI OS
---

# Self-Improving Agent

An autonomous agent that continuously improves skills and prompts through experimentation, evaluation, and promotion of successful variants.

## When to Use

- When you want to optimize skill activation rates (Layer 1)
- When you want to improve output quality (Layer 2)
- When running overnight improvement cycles
- When analyzing experiment results
- When promoting successful variants to production

## When NOT to Use

- For one-off manual edits (use direct editing instead)
- When you need immediate changes (experiments take time)
- For non-skill/non-prompt improvements

## Commands

### Status Check
```
/self-improve status
```
Shows current experiment status, recent results, and cumulative improvements.

### Run Improvement Cycle
```
/self-improve run [--dry-run] [--layer=1|2|both]
```
Runs a full improvement cycle. Use `--dry-run` to preview without making changes.

### View Experiments
```
/self-improve experiments [--status=running|completed|failed|promoted]
```
Lists experiments with optional status filter.

### Promote Variant
```
/self-improve promote <experiment-id>
```
Manually promotes a successful variant to production.

### Rollback
```
/self-improve rollback <experiment-id>
```
Rolls back a promoted variant to its baseline.

### Generate Report
```
/self-improve report [--period=7d|30d|all]
```
Generates an improvement report for the specified period.

## Two-Layer Approach

### Layer 1: Activation Optimization
Optimizes skill descriptions for better trigger accuracy:
- Analyzes `when_to_use` and `when_not_to_use` sections
- Generates clearer, more specific descriptions
- Tests against activation scenarios
- Measures activation rate and false positive rate

### Layer 2: Quality Optimization
Optimizes actual output quality:
- Runs skills against test inputs
- Evaluates output with binary assertions
- Measures quality KPIs
- Identifies improvement opportunities

## Configuration

Located in `experiments/index.json`:

```json
{
  "config": {
    "run_frequency": "daily",
    "run_time": "02:00",
    "timezone": "UTC",
    "max_concurrent_experiments": 3,
    "min_samples_per_experiment": 10,
    "promotion_threshold": 0.15
  }
}
```

## Experiment Lifecycle

```
PENDING → RUNNING → EVALUATING → [PROMOTED | FAILED | DISCARDED]
```

1. **PENDING**: Variant generated, awaiting evaluation
2. **RUNNING**: Experiment actively collecting data
3. **EVALUATING**: Comparing results against baseline
4. **PROMOTED**: Variant passed threshold, now in production
5. **FAILED**: Variant did not improve on baseline
6. **DISCARDED**: Variant caused regression, rolled back

## Directory Structure

```
experiments/
├── index.json          # Experiment registry and config
├── baselines/          # Baseline snapshots before experiments
├── variants/           # Experimental variations
├── results/            # Experiment results and metrics
└── test-scenarios/     # Test cases for evaluation
    ├── activation-tests.json
    └── quality-tests.json
```

## Integration with AI OS

This skill integrates with the OpenClaw AI OS framework:

- **Process Bucket**: Operates as an AI SOP for continuous improvement
- **Context Bucket**: Uses prompt library for evaluation prompts
- **Systems Bucket**: Registered in tools registry, logs to usage.jsonl

## Example Workflow

```bash
# 1. Check current status
/self-improve status

# 2. Run a dry-run to see what would be optimized
/self-improve run --dry-run

# 3. Run full improvement cycle (both layers)
/self-improve run --layer=both

# 4. Check experiment results
/self-improve experiments --status=completed

# 5. Manually promote a successful variant
/self-improve promote exp-001

# 6. Generate weekly report
/self-improve report --period=7d
```

## Overnight Automation

The agent runs automatically at 02:00 UTC daily when configured with hooks:

```json
{
  "hooks": {
    "scheduled": [
      {
        "name": "overnight-improvement",
        "schedule": "0 2 * * *",
        "command": "/self-improve run --layer=both"
      }
    ]
  }
}
```

## KPIs Tracked

| KPI | Target | Direction |
|-----|--------|-----------|
| activation_rate | 80% | Maximize |
| false_positive_rate | 5% | Minimize |
| output_quality | 90% | Maximize |
| task_completion_rate | 85% | Maximize |
| assertion_pass_rate | 90% | Maximize |

## Logging

All experiments are logged to `prompts/usage.jsonl` with the following format:

```json
{
  "timestamp": "2026-03-19T02:00:00Z",
  "event": "experiment_run",
  "experiment_id": "exp-001",
  "layer": 1,
  "target": "prompts/extraction/video-transcript-v1.md",
  "baseline_kpi": 0.65,
  "variant_kpi": 0.82,
  "improvement": 0.17,
  "status": "promoted"
}
```

## References

- [Karpathy's Autoresearch](https://github.com/karpathy/autoresearch) - Original pattern
- [OpenClaw Skills](https://github.com/openclaw/skills) - Community skills
- [TikTok: @agentic.james](https://www.tiktok.com/@agentic.james) - Implementation inspiration
