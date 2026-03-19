# Prompt Library

Versioned prompts that work. When a prompt produces good output, capture it here so we stop re-learning.

## Structure

```
prompts/
├── investment/       # LP comms, portfolio analysis, deal memos
├── analysis/         # Scenario modeling, option matrices, decision frameworks
└── ingestion/        # Content processing, summarization, skill extraction
```

## How to Use

**Adding a prompt:**
1. Create a `.md` file in the appropriate category
2. Include: context, the prompt itself, example output, and when to use it
3. Tag with version (v1, v2, etc.) when you improve it

**Using a prompt:**
- Reference by path: `prompts/investment/lp-update.md`
- Copy the prompt section and adapt for your context
- If you improve it, update the file with a new version

## What Makes a Good Prompt

- **Specific context** — what situation triggers this prompt
- **Clear structure** — the prompt itself, formatted for copy/paste
- **Example output** — what good looks like
- **Iteration notes** — what you tried that didn't work
