#!/bin/bash
set -euo pipefail

# Pre-commit hook: Validates analysis document structure
# Integrates with CLAUDE.md conventions and analyze-position skill output format

# Get list of staged markdown files
staged_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '.*-ANALYSIS\.md$' || true)

if [[ -z "$staged_files" ]]; then
    exit 0
fi

errors=()

for file in $staged_files; do
    # Check for required date line
    if ! grep -q "^\*\*Date:\*\*" "$file" && ! grep -q "^## .*Date" "$file"; then
        errors+=("$file: Missing date field (expected **Date:** or date header)")
    fi

    # Check for context line
    if ! grep -q "^\*\*Context:\*\*" "$file" && ! grep -q "^## .*Context" "$file"; then
        errors+=("$file: Missing context field (expected **Context:** or context header)")
    fi

    # Check for action items section
    if ! grep -q "^## Action Items" "$file" && ! grep -q "^### Action Items" "$file"; then
        errors+=("$file: Missing 'Action Items' section")
    fi
done

if [[ ${#errors[@]} -gt 0 ]]; then
    echo "Document structure validation failed:" >&2
    for err in "${errors[@]}"; do
        echo "  - $err" >&2
    done
    echo "" >&2
    echo "All analysis documents must include: date, context, and action items." >&2
    echo "See CLAUDE.md for document standards." >&2
    exit 1
fi

exit 0
