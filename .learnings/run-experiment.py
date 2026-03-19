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

import anthropic

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
# CLAUDE API CLIENT
# ============================================================================

def get_client() -> anthropic.Anthropic:
    """Get Anthropic client. Reads API key from env or .env file."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        env_file = LEARNINGS_DIR.parent / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip("'\"")
                    break

    if not api_key:
        log_error("No ANTHROPIC_API_KEY found. Set it in environment or .env file.")
        sys.exit(1)

    return anthropic.Anthropic(api_key=api_key)


# Token-to-cost estimate (Haiku pricing for cost efficiency)
INPUT_COST_PER_MTOK = 0.25   # $/million input tokens
OUTPUT_COST_PER_MTOK = 1.25  # $/million output tokens


def estimate_cost(usage) -> float:
    """Estimate cost from API usage object."""
    input_cost = (usage.input_tokens / 1_000_000) * INPUT_COST_PER_MTOK
    output_cost = (usage.output_tokens / 1_000_000) * OUTPUT_COST_PER_MTOK
    return input_cost + output_cost


# ============================================================================
# EXPERIMENT EXECUTION - WIRED TO CLAUDE API
# ============================================================================

def load_skill_content(skill_name: str) -> str:
    """Load the skill markdown file content."""
    skill_file = SKILLS_DIR / f"{skill_name}.md"
    if not skill_file.exists():
        return f"[Skill file not found: {skill_file}]"
    return skill_file.read_text()


def load_eval_data(skill_name: str) -> dict:
    """Load the full eval YAML data for a skill."""
    eval_file = EVALS_DIR / f"{skill_name}.yaml"
    if not eval_file.exists():
        return {}
    return yaml.safe_load(eval_file.read_text())


def generate_variation(skill_name: str, variable: str) -> dict:
    """
    Generate a variation of the skill by tweaking one variable via Claude API.

    Reads the current skill file, asks Claude to improve the specified variable,
    and returns the variation with a hypothesis for why it should improve KPIs.
    """
    variation_id = generate_id("VAR")
    skill_content = load_skill_content(skill_name)
    eval_data = load_eval_data(skill_name)

    # Build context about what we're optimizing
    test_prompts = eval_data.get("test_prompts", [])
    activation_keywords = eval_data.get("activation_keywords", [])

    prompt = f"""You are optimizing a Claude Code skill file. Your goal is to improve its {variable}.

## Current Skill File ({skill_name}.md)
```markdown
{skill_content}
```

## Eval Context
- Test prompts that should activate this skill: {json.dumps(test_prompts)}
- Expected activation keywords: {json.dumps(activation_keywords)}

## Variable to Optimize: {variable}

## Rules
- Change ONLY the {variable} - keep everything else the same
- The change should improve activation rate (skill triggers on relevant prompts)
- The change should improve output quality (assertions pass more often)
- Be specific and actionable, not vague

## Output Format (JSON)
Return ONLY a JSON object with these fields:
- "original_value": the current value of the variable you're changing
- "new_value": your improved version
- "hypothesis": one sentence explaining why this should improve KPIs
- "changed_skill_content": the full skill file with your change applied"""

    try:
        client = get_client()
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        cost = estimate_cost(response.usage)
        response_text = response.content[0].text

        # Extract JSON from response (handle markdown code blocks)
        json_text = response_text
        if "```json" in json_text:
            json_text = json_text.split("```json")[1].split("```")[0]
        elif "```" in json_text:
            json_text = json_text.split("```")[1].split("```")[0]

        parsed = json.loads(json_text.strip())

        return {
            "variation_id": variation_id,
            "variable": variable,
            "original_value": parsed.get("original_value", ""),
            "new_value": parsed.get("new_value", ""),
            "hypothesis": parsed.get("hypothesis", ""),
            "changed_skill_content": parsed.get("changed_skill_content", ""),
            "cost_usd": cost,
        }

    except json.JSONDecodeError as e:
        log_error(f"Failed to parse Claude response as JSON: {e}")
        return {
            "variation_id": variation_id,
            "variable": variable,
            "original_value": "[PARSE ERROR]",
            "new_value": "[PARSE ERROR]",
            "hypothesis": f"JSON parse error: {e}",
            "cost_usd": 0.0,
        }
    except anthropic.APIError as e:
        log_error(f"Claude API error: {e}")
        return {
            "variation_id": variation_id,
            "variable": variable,
            "original_value": "[API ERROR]",
            "new_value": "[API ERROR]",
            "hypothesis": f"API error: {e}",
            "cost_usd": 0.0,
        }


def run_assertions(skill_name: str, assertions: list[Assertion], variation: dict) -> dict:
    """
    Run assertions against a skill variation by simulating skill execution
    with Claude and evaluating each assertion against the output.
    """
    eval_data = load_eval_data(skill_name)
    test_prompts = eval_data.get("test_prompts", [])

    # Use the varied skill content if available, otherwise the original
    skill_content = variation.get("changed_skill_content", "") or load_skill_content(skill_name)

    if not test_prompts:
        log_warning(f"No test prompts for {skill_name}")
        return {
            "pass_rate": 0.0,
            "safety_passed": True,
            "execution_time_ms": 0,
            "assertions_run": len(assertions),
            "assertions_passed": 0,
            "cost_usd": 0.0,
        }

    # Pick a random test prompt for this run
    import random
    test_prompt = random.choice(test_prompts)

    start_time = time.time()
    total_cost = 0.0

    # Simulate skill execution via Claude
    execution_prompt = f"""You are a Claude Code skill executing a user request. Follow the skill instructions exactly.

## Skill Instructions
```markdown
{skill_content}
```

## User Request
{test_prompt}

## Output Format
Return a JSON object representing the skill's output. Include fields that match what the skill would produce.
For example, if the skill extracts transcripts, include a "transcript" field.
If the skill creates PRs, include "pr_url", "title", "pr_body", "branch" fields.
If the skill generates summaries, include "summary", "commits", "blockers" fields.

Return ONLY the JSON object, no markdown formatting."""

    try:
        client = get_client()
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1500,
            messages=[{"role": "user", "content": execution_prompt}]
        )

        total_cost += estimate_cost(response.usage)
        response_text = response.content[0].text

        # Parse the simulated output
        json_text = response_text
        if "```json" in json_text:
            json_text = json_text.split("```json")[1].split("```")[0]
        elif "```" in json_text:
            json_text = json_text.split("```")[1].split("```")[0]

        try:
            output = json.loads(json_text.strip())
        except json.JSONDecodeError:
            output = {"raw_output": response_text}

    except anthropic.APIError as e:
        log_error(f"Claude API error during execution: {e}")
        output = {"error": str(e)}

    execution_time_ms = (time.time() - start_time) * 1000

    # Evaluate assertions against the output
    passed_count = 0
    safety_passed = True
    assertion_results = []

    for assertion in assertions:
        try:
            # Evaluate the check expression with output and execution_time_ms in scope
            result = eval(assertion.check, {"__builtins__": {
                "len": len, "str": str, "int": int, "float": float,
                "isinstance": isinstance, "any": any, "all": all,
                "sum": sum, "dict": dict, "list": list, "set": set,
            }}, {"output": output, "execution_time_ms": execution_time_ms})

            if result:
                passed_count += 1
            elif assertion.weight == 3:
                safety_passed = False
                log_warning(f"SAFETY BLOCKER FAILED: {assertion.name}")

            assertion_results.append({
                "name": assertion.name,
                "passed": bool(result),
                "weight": assertion.weight,
            })

        except Exception as e:
            log_warning(f"Assertion {assertion.name} raised error: {e}")
            if assertion.weight == 3:
                safety_passed = False
            assertion_results.append({
                "name": assertion.name,
                "passed": False,
                "weight": assertion.weight,
                "error": str(e),
            })

    pass_rate = passed_count / len(assertions) if assertions else 0.0

    return {
        "pass_rate": pass_rate,
        "safety_passed": safety_passed,
        "execution_time_ms": execution_time_ms,
        "assertions_run": len(assertions),
        "assertions_passed": passed_count,
        "cost_usd": total_cost,
        "test_prompt": test_prompt,
        "assertion_results": assertion_results,
    }


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
