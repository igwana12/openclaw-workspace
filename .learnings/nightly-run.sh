#!/bin/bash
# Nightly Self-Improving Agent Run
# Scheduled: 02:00 AM ET daily
#
# Setup: crontab -e
# 0 2 * * * /home/user/openclaw-workspace/.learnings/nightly-run.sh >> /home/user/openclaw-workspace/.learnings/nightly.log 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"
EXPERIMENT_RUNNER="$SCRIPT_DIR/run-experiment.py"
LOG_FILE="$SCRIPT_DIR/nightly.log"

echo "============================================="
echo "Nightly Experiment Run: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "============================================="

# Load environment (API key etc.)
if [ -f "$WORKSPACE_DIR/.env" ]; then
    set -a
    source "$WORKSPACE_DIR/.env"
    set +a
fi

cd "$WORKSPACE_DIR"

# Step 1: Refresh baselines (weekly on Sundays)
DAY_OF_WEEK=$(date +%u)
if [ "$DAY_OF_WEEK" -eq 7 ]; then
    echo "Sunday - refreshing baselines..."
    python3 "$EXPERIMENT_RUNNER" --baseline --verbose 2>&1
fi

# Step 2: Run experiments on all priority skills
echo "Running experiment suite..."
python3 "$EXPERIMENT_RUNNER" --report-to-slack --verbose 2>&1

# Step 3: Commit any promoted changes
cd "$WORKSPACE_DIR"
if [ -n "$(git status --porcelain)" ]; then
    echo "Changes detected - committing promotions..."
    git add -A
    git commit -m "chore: nightly experiment promotions $(date +%Y-%m-%d)

Automated by self-improving agent loop.
See .learnings/PROMOTIONS.md for details."
    git push origin HEAD
fi

echo "============================================="
echo "Nightly run complete: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "============================================="
