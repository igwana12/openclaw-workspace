#!/usr/bin/env python3
"""
Self-Improving Agent Experiment Runner

Based on Karpathy's autoresearch pattern applied to Claude Code skills.
Runs experiments, compares against baseline, promotes improvements.

Usage:
    python run-experiment.py --dry-run                    # Test without changes
    python run-experiment.py --skill video-ingestor       # Run specific skill
    python run-experiment.py --report-to-slack            # Post results to Slack
    python run-experiment.py --baseline                   # Refresh baseline metrics
    python run-experiment.py --verbose                    # Detailed logging
"""

import argparse
import json
import os
import subprocess
import sys
import time
import yaml
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

SOFT_COST_LIMIT = 10.0  # USD per day
HARD_COST_LIMIT = 50.0  # USD per day
PER_EXPERIMENT_LIMIT = 2.0  # USD per experiment
IMPROVEMENT_THRESHOLD = 0.10  # 10% improvement required for promotion
MIN_RUNS_PER_VARIATION = 3  # Reduce noise

LEARNINGS_DIR = Path(__file__).parent
EVALS_DIR = LEARNINGS_DIR.parent / "evals"
SKILLS_DIR = LEARNINGS_DIR.parent / ".claude" / "commands"

# Weight-3 safety blockers - these hard-reject any experiment
SAFETY_BLOCKERS = [
    "stop_loss_present",
    "position_sizing_valid",
    "max_drawdown_check",
    "no_secrets_exposed",
    "no_destructive_git",
]


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class ExperimentResult:
    skill_name: str
    variation_id: str
    timestamp: str
    metrics: dict
    passed: bool
    safety_blocked: bool = False
    cost_usd: float = 0.0
    notes: str = ""


@dataclass
class Baseline:
    skill_name: str
    metrics: dict
    timestamp: str


@dataclass
class Assertion:
    name: str
    description: str
    weight: int
    check: str  # Python expression or callable name


@dataclass
class ExperimentConfig:
    dry_run: bool = False
    verbose: bool = False
    report_to_slack: bool = False
    skill: Optional[str] = None
    baseline_mode: bool = False


# ============================================================================
# COST TRACKING
# ============================================================================

class CostTracker:
    """Track daily experiment costs against guardrails."""

    def __init__(self):
        self.cost_file = LEARNINGS_DIR / ".daily_costs.json"
        self.load()

    def load(self):
        if self.cost_file.exists():
            data = json.loads(self.cost_file.read_text())
            if data.get("date") == datetime.now().strftime("%Y-%m-%d"):
                self.daily_total = data.get("total", 0.0)
            else:
                self.daily_total = 0.0
        else:
            self.daily_total = 0.0

    def save(self):
        data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total": self.daily_total
        }
        self.cost_file.write_text(json.dumps(data))

    def add(self, cost: float) -> bool:
        """Add cost. Returns False if hard limit exceeded."""
        self.daily_total += cost
        self.save()

        if self.daily_total >= HARD_COST_LIMIT:
            log_error(f"HARD COST LIMIT EXCEEDED: ${self.daily_total:.2f} >= ${HARD_COST_LIMIT}")
            return False

        if self.daily_total >= SOFT_COST_LIMIT:
            log_warning(f"Soft cost limit reached: ${self.daily_total:.2f} >= ${SOFT_COST_LIMIT}")

        return True

    def can_run(self, estimated_cost: float) -> bool:
        """Check if we can run an experiment with estimated cost."""
        if estimated_cost > PER_EXPERIMENT_LIMIT:
            log_warning(f"Experiment cost ${estimated_cost:.2f} exceeds per-experiment limit ${PER_EXPERIMENT_LIMIT}")
            return False

        if self.daily_total + estimated_cost > HARD_COST_LIMIT:
            log_error(f"Would exceed hard limit: ${self.daily_total:.2f} + ${estimated_cost:.2f} > ${HARD_COST_LIMIT}")
            return False

        return True


# ============================================================================
# LOGGING
# ============================================================================

def log(msg: str, level: str = "INFO"):
    """Log message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")


def log_error(msg: str):
    log(msg, "ERROR")


def log_warning(msg: str):
    log(msg, "WARN")


def log_verbose(msg: str, config: ExperimentConfig):
    if config.verbose:
        log(msg, "DEBUG")


def generate_id(prefix: str) -> str:
    """Generate ID in TYPE-YYYYMMDD-XXX format."""
    date = datetime.now().strftime("%Y%m%d")
    # Simple incrementing counter based on existing IDs
    existing = list(LEARNINGS_DIR.glob(f"*.md"))
    counter = len(existing) + 1
    return f"{prefix}-{date}-{counter:03d}"


# ============================================================================
# FILE OPERATIONS
# ============================================================================

def append_to_log(filename: str, entry: str):
    """Append entry to a log file."""
    filepath = LEARNINGS_DIR / filename
    with open(filepath, "a") as f:
        f.write(f"\n{entry}\n")


def log_experiment(result: ExperimentResult):
    """Log experiment to EXPERIMENTS.md."""
    entry = f"""
## {result.variation_id}

- **Skill:** {result.skill_name}
- **Timestamp:** {result.timestamp}
- **Passed:** {"Yes" if result.passed else "No"}
- **Safety Blocked:** {"Yes" if result.safety_blocked else "No"}
- **Cost:** ${result.cost_usd:.4f}

### Metrics
```json
{json.dumps(result.metrics, indent=2)}
```

### Notes
{result.notes}

---
"""
    append_to_log("EXPERIMENTS.md", entry)


def log_learning(skill: str, insight: str):
    """Log learning to LEARNINGS.md."""
    entry = f"""
## {generate_id("LEARN")}

- **Skill:** {skill}
- **Timestamp:** {datetime.now().isoformat()}

### Insight
{insight}

---
"""
    append_to_log("LEARNINGS.md", entry)


def log_promotion(result: ExperimentResult, improvement_pct: float):
    """Log successful promotion to PROMOTIONS.md."""
    entry = f"""
## {generate_id("PROMO")}

- **Skill:** {result.skill_name}
- **Variation:** {result.variation_id}
- **Improvement:** {improvement_pct:.1f}%
- **Timestamp:** {datetime.now().isoformat()}

### Metrics
```json
{json.dumps(result.metrics, indent=2)}
```

---
"""
    append_to_log("PROMOTIONS.md", entry)


def log_error_entry(skill: str, error: str, context: str = ""):
    """Log error to ERRORS.md."""
    entry = f"""
## {generate_id("ERR")}

- **Skill:** {skill}
- **Timestamp:** {datetime.now().isoformat()}

### Error
```
{error}
```

### Context
{context}

---
"""
    append_to_log("ERRORS.md", entry)


# ============================================================================
# EVAL LOADING
# ============================================================================

def load_eval(skill_name: str) -> list[Assertion]:
    """Load eval assertions for a skill."""
    eval_file = EVALS_DIR / f"{skill_name}.yaml"

    if not eval_file.exists():
        log_warning(f"No eval file found for {skill_name}")
        return []

    data = yaml.safe_load(eval_file.read_text())
    assertions = []

    for item in data.get("assertions", []):
        assertions.append(Assertion(
            name=item["name"],
            description=item.get("description", ""),
            weight=item.get("weight", 1),
            check=item["check"]
        ))

    return assertions


def load_baseline(skill_name: str) -> Optional[Baseline]:
    """Load baseline metrics for a skill."""
    baseline_file = LEARNINGS_DIR / "baselines" / f"{skill_name}.json"

    if not baseline_file.exists():
        return None

    data = json.loads(baseline_file.read_text())
    return Baseline(
        skill_name=skill_name,
        metrics=data["metrics"],
        timestamp=data["timestamp"]
    )


def save_baseline(baseline: Baseline):
    """Save baseline metrics for a skill."""
    baseline_dir = LEARNINGS_DIR / "baselines"
    baseline_dir.mkdir(exist_ok=True)

    baseline_file = baseline_dir / f"{baseline.skill_name}.json"
    data = {
        "skill_name": baseline.skill_name,
        "metrics": baseline.metrics,
        "timestamp": baseline.timestamp
    }
    baseline_file.write_text(json.dumps(data, indent=2))


# ============================================================================
# EXPERIMENT EXECUTION - STUBS TO WIRE
# ============================================================================

def generate_variation(skill_name: str, variable: str) -> dict:
    """
    STUB: Generate a variation of the skill by tweaking one variable.

    Wire this to actual LLM calls to generate variations.

    Args:
        skill_name: Name of the skill to vary
        variable: The variable to tweak (e.g., "description", "system_prompt")

    Returns:
        dict with variation details
    """
    # TODO: Wire to Claude API
    # Example structure:
    # return {
    #     "variation_id": generate_id("VAR"),
    #     "variable": variable,
    #     "original_value": "...",
    #     "new_value": "...",
    #     "hypothesis": "Why this might improve the KPI"
    # }

    log_warning(f"generate_variation() is a stub - wire to LLM calls")
    return {
        "variation_id": generate_id("VAR"),
        "variable": variable,
        "original_value": "[STUB]",
        "new_value": "[STUB]",
        "hypothesis": "Stub variation - wire generate_variation() to LLM"
    }


def run_assertions(skill_name: str, assertions: list[Assertion], variation: dict) -> dict:
    """
    STUB: Run assertions against a skill variation.

    Wire this to actual skill execution and assertion checking.

    Args:
        skill_name: Name of the skill
        assertions: List of assertions to run
        variation: The variation being tested

    Returns:
        dict with metrics including pass_rate, safety_passed, execution_time
    """
    # TODO: Wire to actual skill execution
    # Example structure:
    # 1. Load skill with variation applied
    # 2. Run test prompts
    # 3. Check each assertion
    # 4. Return metrics

    log_warning(f"run_assertions() is a stub - wire to actual execution")

    results = {
        "pass_rate": 0.0,
        "safety_passed": True,
        "execution_time_ms": 0,
        "assertions_run": len(assertions),
        "assertions_passed": 0,
        "cost_usd": 0.001,  # Stub cost
    }

    # Check for safety blockers
    for assertion in assertions:
        if assertion.weight == 3 and assertion.name in SAFETY_BLOCKERS:
            # In real implementation, actually run the check
            # For stub, assume all safety checks pass
            pass

    return results


# ============================================================================
# MAIN EXPERIMENT LOGIC
# ============================================================================

def run_single_experiment(
    skill_name: str,
    config: ExperimentConfig,
    cost_tracker: CostTracker
) -> Optional[ExperimentResult]:
    """Run a single experiment on a skill."""

    log(f"Running experiment on: {skill_name}")

    # Load assertions
    assertions = load_eval(skill_name)
    if not assertions:
        log_warning(f"No assertions for {skill_name}, skipping")
        return None

    log_verbose(f"Loaded {len(assertions)} assertions", config)

    # Load baseline
    baseline = load_baseline(skill_name)
    if not baseline and not config.baseline_mode:
        log_warning(f"No baseline for {skill_name}, run with --baseline first")
        return None

    # Check cost budget
    estimated_cost = 0.10  # Estimate - adjust based on actual usage
    if not cost_tracker.can_run(estimated_cost):
        log_error("Cost budget exceeded, skipping experiment")
        return None

    # Generate variation
    variation = generate_variation(skill_name, "description")
    log_verbose(f"Generated variation: {variation['variation_id']}", config)

    if config.dry_run:
        log(f"DRY RUN - would test variation: {variation['variation_id']}")
        return ExperimentResult(
            skill_name=skill_name,
            variation_id=variation["variation_id"],
            timestamp=datetime.now().isoformat(),
            metrics={"dry_run": True},
            passed=False,
            notes="Dry run - no actual execution"
        )

    # Run multiple times to reduce noise
    all_metrics = []
    for run_num in range(MIN_RUNS_PER_VARIATION):
        log_verbose(f"Run {run_num + 1}/{MIN_RUNS_PER_VARIATION}", config)
        metrics = run_assertions(skill_name, assertions, variation)
        all_metrics.append(metrics)

    # Aggregate metrics
    avg_metrics = {
        "pass_rate": sum(m["pass_rate"] for m in all_metrics) / len(all_metrics),
        "safety_passed": all(m["safety_passed"] for m in all_metrics),
        "execution_time_ms": sum(m["execution_time_ms"] for m in all_metrics) / len(all_metrics),
        "total_cost_usd": sum(m["cost_usd"] for m in all_metrics),
    }

    # Track cost
    cost_tracker.add(avg_metrics["total_cost_usd"])

    # Check safety blockers
    safety_blocked = not avg_metrics["safety_passed"]
    if safety_blocked:
        log_error(f"SAFETY BLOCKED: {skill_name}")

    # Compare to baseline
    passed = False
    improvement_pct = 0.0

    if baseline and not safety_blocked:
        baseline_pass_rate = baseline.metrics.get("pass_rate", 0)
        new_pass_rate = avg_metrics["pass_rate"]

        if baseline_pass_rate > 0:
            improvement_pct = (new_pass_rate - baseline_pass_rate) / baseline_pass_rate
        else:
            improvement_pct = 1.0 if new_pass_rate > 0 else 0.0

        passed = improvement_pct >= IMPROVEMENT_THRESHOLD
        log(f"Improvement: {improvement_pct:.1%} (threshold: {IMPROVEMENT_THRESHOLD:.1%})")

    result = ExperimentResult(
        skill_name=skill_name,
        variation_id=variation["variation_id"],
        timestamp=datetime.now().isoformat(),
        metrics=avg_metrics,
        passed=passed,
        safety_blocked=safety_blocked,
        cost_usd=avg_metrics["total_cost_usd"],
        notes=f"Improvement: {improvement_pct:.1%}" if baseline else "Baseline run"
    )

    # Log results
    log_experiment(result)

    if passed:
        log_promotion(result, improvement_pct * 100)
        log(f"PROMOTED: {variation['variation_id']}")

    if safety_blocked:
        log_error_entry(skill_name, "Safety blocker triggered", str(avg_metrics))

    return result


def run_baseline(skill_name: str, config: ExperimentConfig) -> bool:
    """Run baseline measurement for a skill."""

    log(f"Running baseline for: {skill_name}")

    assertions = load_eval(skill_name)
    if not assertions:
        log_warning(f"No assertions for {skill_name}")
        return False

    if config.dry_run:
        log(f"DRY RUN - would establish baseline for: {skill_name}")
        return True

    # Run assertions with no variation (current state)
    metrics = run_assertions(skill_name, assertions, {})

    baseline = Baseline(
        skill_name=skill_name,
        metrics=metrics,
        timestamp=datetime.now().isoformat()
    )

    save_baseline(baseline)
    log(f"Baseline saved for {skill_name}: pass_rate={metrics.get('pass_rate', 0):.1%}")

    return True


def get_priority_skills() -> list[str]:
    """Get skills in priority order."""
    # Read from program.md or use defaults
    return [
        "video-ingestor",
        "slack-to-pr",
        "standup",
        "audit-setup",
    ]


def report_to_slack(results: list[ExperimentResult]):
    """Post experiment summary to Slack."""
    # TODO: Implement Slack reporting
    log_warning("Slack reporting not implemented yet")

    summary = f"""
## Experiment Run Summary

- **Timestamp:** {datetime.now().isoformat()}
- **Experiments Run:** {len(results)}
- **Passed:** {sum(1 for r in results if r.passed)}
- **Safety Blocked:** {sum(1 for r in results if r.safety_blocked)}
- **Total Cost:** ${sum(r.cost_usd for r in results):.4f}
"""
    log(summary)


# ============================================================================
# CLI
# ============================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Self-Improving Agent Experiment Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Test without making changes"
    )

    parser.add_argument(
        "--skill",
        type=str,
        help="Run experiments on specific skill only"
    )

    parser.add_argument(
        "--baseline",
        action="store_true",
        help="Establish baseline metrics (run before experiments)"
    )

    parser.add_argument(
        "--report-to-slack",
        action="store_true",
        help="Post results to Slack"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    config = ExperimentConfig(
        dry_run=args.dry_run,
        verbose=args.verbose,
        report_to_slack=args.report_to_slack,
        skill=args.skill,
        baseline_mode=args.baseline,
    )

    cost_tracker = CostTracker()

    log("=" * 60)
    log("Self-Improving Agent Experiment Runner")
    log("=" * 60)

    if config.dry_run:
        log("DRY RUN MODE - no changes will be made")

    log(f"Daily cost so far: ${cost_tracker.daily_total:.2f}")

    # Get skills to process
    if config.skill:
        skills = [config.skill]
    else:
        skills = get_priority_skills()

    log(f"Skills to process: {', '.join(skills)}")

    results = []

    for skill in skills:
        if config.baseline_mode:
            run_baseline(skill, config)
        else:
            result = run_single_experiment(skill, config, cost_tracker)
            if result:
                results.append(result)

    if config.report_to_slack and results:
        report_to_slack(results)

    log("=" * 60)
    log("Experiment run complete")
    log(f"Total cost: ${cost_tracker.daily_total:.2f}")
    log("=" * 60)


if __name__ == "__main__":
    main()
