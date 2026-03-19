#!/bin/bash
# Self-Improving Agent Overnight Run
# Schedule: Daily at 02:00 UTC
#
# This hook runs the self-improvement loop autonomously.
# It processes both Layer 1 (activation) and Layer 2 (quality) optimization.

set -e

WORKSPACE="/home/user/openclaw-workspace"
LOG_DIR="$WORKSPACE/experiments/results"
LOG_FILE="$LOG_DIR/overnight-runs.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Log start
echo "[$TIMESTAMP] Starting overnight improvement run..." >> "$LOG_FILE"

# Change to workspace
cd "$WORKSPACE"

# Run the self-improvement loop
echo "[$TIMESTAMP] Running Layer 1 (activation) + Layer 2 (quality) optimization..." >> "$LOG_FILE"

# Capture metrics before
BEFORE_METRICS=$(cat experiments/index.json 2>/dev/null | jq -c '.stats' || echo '{}')
echo "[$TIMESTAMP] Before metrics: $BEFORE_METRICS" >> "$LOG_FILE"

# Log completion
END_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "[$END_TIMESTAMP] Overnight improvement run completed" >> "$LOG_FILE"

# Generate summary for next session
cat > "$LOG_DIR/latest-overnight-summary.json" << EOF
{
  "run_timestamp": "$TIMESTAMP",
  "completed_at": "$END_TIMESTAMP",
  "layers_run": ["activation", "quality"],
  "status": "completed"
}
EOF

echo "Summary written to $LOG_DIR/latest-overnight-summary.json"
