# Self-Improving Agent Program

This document orchestrates the self-improvement loop for the OpenClaw AI OS. It runs both Layer 1 (activation optimization) and Layer 2 (quality optimization) in parallel as configured.

## Trigger Conditions

- **Scheduled**: Daily at 02:00 UTC
- **Manual**: `/self-improve run`
- **Hook**: Post-session analysis (optional)

---

## Main Loop

### Step 1: Initialize

```python
# Load current state
experiments = load_json("experiments/index.json")
prompts_index = load_json("prompts/index.json")
usage_log = load_jsonl("prompts/usage.jsonl")

# Check for running experiments
running = [e for e in experiments["experiments"] if e["status"] == "running"]
if len(running) >= experiments["config"]["max_concurrent_experiments"]:
    log("Max concurrent experiments reached, waiting...")
    exit()
```

### Step 2: Identify Optimization Targets

```python
# Find prompts/skills with suboptimal KPIs
targets = []

for prompt in prompts_index["prompts"]:
    usage = get_usage_stats(prompt["id"], usage_log)

    # Layer 1: Check activation rate
    if usage.get("activation_rate", 0) < 0.80:
        targets.append({
            "id": prompt["id"],
            "layer": 1,
            "current_kpi": usage.get("activation_rate", 0),
            "target_kpi": 0.80,
            "path": prompt["path"]
        })

    # Layer 2: Check output quality
    if usage.get("output_quality", 0) < 0.90:
        targets.append({
            "id": prompt["id"],
            "layer": 2,
            "current_kpi": usage.get("output_quality", 0),
            "target_kpi": 0.90,
            "path": prompt["path"]
        })

# Sort by improvement potential
targets.sort(key=lambda x: x["target_kpi"] - x["current_kpi"], reverse=True)
```

### Step 3: Generate Variants (Parallel for Both Layers)

```python
for target in targets[:experiments["config"]["max_concurrent_experiments"]]:
    # Read current version
    current_content = read_file(target["path"])

    if target["layer"] == 1:
        # Layer 1: Optimize descriptions
        variants = generate_activation_variants(current_content, n=3)
    else:
        # Layer 2: Optimize content structure
        variants = generate_quality_variants(current_content, n=3)

    # Save baseline
    save_baseline(target["id"], current_content)

    # Save variants
    for i, variant in enumerate(variants):
        experiment_id = generate_experiment_id()
        save_variant(experiment_id, variant)

        # Register experiment
        register_experiment({
            "id": experiment_id,
            "target": target["id"],
            "layer": target["layer"],
            "baseline_version": get_version(target["id"]),
            "variant_content": variant,
            "hypothesis": variant["hypothesis"],
            "status": "pending",
            "started_at": now()
        })
```

### Step 4: Run Evaluations

```python
for experiment in get_pending_experiments():
    experiment["status"] = "running"
    save_experiment(experiment)

    # Load test scenarios
    if experiment["layer"] == 1:
        scenarios = load_json("experiments/test-scenarios/activation-tests.json")
        eval_prompt = read_file("prompts/evaluation/skill-activation-v1.md")
    else:
        scenarios = load_json("experiments/test-scenarios/quality-tests.json")
        eval_prompt = read_file("prompts/evaluation/output-quality-v1.md")

    # Filter scenarios for this target
    relevant_scenarios = [s for s in scenarios["scenarios"]
                          if s["target_skill"] == experiment["target"]]

    results = []
    for scenario in relevant_scenarios:
        if experiment["layer"] == 1:
            # Layer 1: Evaluate activation decision
            result = evaluate_activation(
                skill_description=experiment["variant_content"],
                user_request=scenario["user_request"],
                expected=scenario["expected_activation"]
            )
        else:
            # Layer 2: Evaluate output quality
            output = run_skill(experiment["variant_content"], scenario["input"])
            result = evaluate_quality(
                output=output,
                assertions=scenario["assertions"]
            )

        results.append(result)

    # Calculate KPIs
    experiment["results"] = {
        "samples": len(results),
        "kpis": calculate_kpis(results, experiment["layer"])
    }
    experiment["status"] = "evaluating"
    save_experiment(experiment)
```

### Step 5: Compare and Promote

```python
for experiment in get_evaluating_experiments():
    baseline_kpi = get_baseline_kpi(experiment["target"], experiment["layer"])
    variant_kpi = experiment["results"]["kpis"]["primary"]

    improvement = variant_kpi - baseline_kpi
    threshold = experiments["config"]["promotion_threshold"]

    if improvement >= threshold:
        # Promote variant
        promote_variant(experiment)
        experiment["status"] = "promoted"
        experiment["improvement"] = improvement

        log_promotion({
            "experiment_id": experiment["id"],
            "target": experiment["target"],
            "improvement": improvement,
            "new_baseline": variant_kpi
        })

    elif improvement < 0:
        # Variant caused regression
        experiment["status"] = "discarded"
        log_regression(experiment)

    else:
        # No significant improvement
        experiment["status"] = "failed"
        log_failure(experiment)

    experiment["completed_at"] = now()
    save_experiment(experiment)
```

### Step 6: Generate Report

```python
report = {
    "run_timestamp": now(),
    "experiments_run": count_experiments_this_run(),
    "promotions": count_promotions_this_run(),
    "failures": count_failures_this_run(),
    "cumulative_improvement": {
        "activation_rate": calculate_cumulative_improvement("activation_rate"),
        "output_quality": calculate_cumulative_improvement("output_quality")
    },
    "next_targets": identify_next_targets(),
    "recommendations": generate_recommendations()
}

save_json("experiments/results/latest-report.json", report)
append_jsonl("prompts/usage.jsonl", {
    "timestamp": now(),
    "event": "improvement_run_completed",
    "report": report
})

# Optional: Post to Slack
if config.get("slack_notifications"):
    post_to_slack(format_report(report))
```

---

## Helper Functions

### generate_activation_variants

Generates variants with improved `when_to_use` and `when_not_to_use` sections:

1. Analyze current activation failures
2. Identify ambiguous language
3. Add specific examples
4. Clarify edge cases
5. Generate 3 distinct variants with different approaches

### generate_quality_variants

Generates variants with improved prompt structure:

1. Analyze output quality failures
2. Identify structural issues
3. Improve input/output specifications
4. Add examples or constraints
5. Generate 3 distinct variants

### evaluate_activation

Uses `prompts/evaluation/skill-activation-v1.md` to determine:
- Should the skill activate? (boolean)
- Confidence score (0-1)
- Reasoning

### evaluate_quality

Uses `prompts/evaluation/binary-assertion-v1.md` for each assertion:
- PASS or FAIL
- One-sentence justification

Then aggregates into overall quality score.

### promote_variant

1. Backup current production version
2. Replace production file with variant
3. Update version number
4. Update prompts/index.json
5. Clear variant from experiments/variants/

### rollback_variant

1. Read backup from experiments/baselines/
2. Replace production file
3. Revert version number
4. Log rollback event

---

## Safety Measures

1. **Baseline Preservation**: Always save baseline before experimenting
2. **Minimum Samples**: Require at least 10 samples before evaluation
3. **Threshold Guard**: Only promote if improvement > 15%
4. **Regression Protection**: Immediately discard variants causing regression
5. **Max Concurrent**: Limit to 3 concurrent experiments
6. **Rollback Ready**: All promotions can be rolled back

---

## Monitoring

Check status anytime with:

```bash
/self-improve status
```

View detailed logs:

```bash
cat experiments/results/latest-report.json | jq .
tail -f prompts/usage.jsonl | grep improvement
```

---

## Scheduling

For cron-based scheduling (optional):

```cron
# Run at 2am daily
0 2 * * * cd /home/user/openclaw-workspace && claude --skill self-improving-agent run
```

Or use Claude Code hooks for integrated scheduling.
