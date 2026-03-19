# Skill Creation Workflow

When a task repeats 3+ times, it becomes a skill. This doc defines when and how.

## The 3x Rule

**Before creating a skill, ask:**
1. Have I done this exact task 3+ times?
2. Are the steps consistent enough to automate?
3. Will this save time over the next 10 uses?

If yes to all three → create a skill.

## Skill Anatomy

Every skill needs:

```markdown
# Skill Name

## Trigger
When to invoke this skill (slash command, keyword, context)

## Inputs
What information the skill needs to run

## Steps
1. First action
2. Second action
3. ...

## Outputs
What the skill produces (files, messages, analysis)

## Tools Required
Which MCP servers/tools this skill uses
```

## Creating a Skill

### Step 1: Document the Manual Process
Before automating, write down exactly what you do manually. Include:
- Trigger conditions ("when I see a TikTok link...")
- Information gathering ("I copy the URL, look up the topic...")
- Actions taken ("I transcribe, summarize, save to...")
- Output format ("markdown file with sections for...")

### Step 2: Create the Skill File
```bash
# For user-global skills
~/.claude/skills/skill-name/SKILL.md

# For project-specific skills
.claude/skills/skill-name.md
```

### Step 3: Define the Trigger
Choose how the skill activates:
- **Slash command:** `/skill-name` — explicit invocation
- **Keyword match:** "review this PR" — natural language trigger
- **Context match:** When certain file types or URLs appear

### Step 4: Test and Iterate
1. Run the skill manually 3 times
2. Note what breaks or needs adjustment
3. Update the skill file
4. Document edge cases in the skill

## Skill Categories

| Category | Examples | Location |
|----------|----------|----------|
| Investment | LP updates, scenario analysis, deal memo | `skills/investment/` |
| Ingestion | Video processing, article capture, thread save | `skills/ingestion/` |
| Development | PR review, commit, deploy | `skills/dev/` |
| Communication | Slack response, email draft, meeting prep | `skills/comms/` |

## Skill Quality Checklist

Before shipping a skill:
- [ ] Has clear trigger conditions
- [ ] Lists all required inputs
- [ ] Steps are numbered and specific
- [ ] Output format is defined
- [ ] Tools/MCP servers are documented
- [ ] Tested with 3+ real examples
- [ ] Edge cases noted

## Graduating Prompts to Skills

When a prompt from `prompts/` gets used 3+ times:

1. Copy the prompt to a new skill file
2. Add trigger, inputs, outputs sections
3. Reference the original prompt: "Based on `prompts/analysis/scenario-matrix.md`"
4. Mark the prompt as "graduated" with link to skill

## Current Skills

| Skill | Status | Location | Last Updated |
|-------|--------|----------|--------------|
| session-start-hook | Active | `~/.claude/skills/` | System default |
| (more to come) | — | — | — |

## Skill Ideas Backlog

Tasks that have repeated but aren't skills yet:

- [ ] **video-ingest** — TikTok/video link → transcribe → summarize → file
- [ ] **thread-capture** — Slack thread → markdown → workspace
- [ ] **lp-update** — context + data → LP communication (graduate from prompt)
- [ ] **decision-log** — capture decision in thread → add to CLAUDE.md
