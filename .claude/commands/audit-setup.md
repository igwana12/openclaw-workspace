# Audit Setup

Run a maturity assessment against the 5-level Claude Code framework.

## The 5 Levels

| Level | Name | Key Characteristics |
|-------|------|---------------------|
| 0 | Nothing | No CLAUDE.md, no skills, no hooks |
| 1 | CLAUDE.md Only | Basic instructions, no integration |
| 2 | Skills & Commands | Reusable prompts, but isolated |
| 3 | Hooks | Event-driven automation, still disconnected |
| 4 | Integrated Systems | Everything talks to everything |
| 5 | Self-Improving | Systems that build/improve your systems |

## Audit Checklist

### 1. CLAUDE.md Audit
- [ ] Is it specific or generic? (Vague = Level 1)
- [ ] Does it reference skills/hooks?
- [ ] Does it encode project-specific patterns?

### 2. Skills Audit
- [ ] Are skills isolated or composable?
- [ ] Do they share context?
- [ ] Are they discoverable from CLAUDE.md?

### 3. Hooks Audit
- [ ] Do hooks communicate with skills?
- [ ] Do they update CLAUDE.md or config?
- [ ] Is there a feedback loop?

### 4. Integration Check
Ask: "If I change one component, do others benefit automatically?"
- No → Level 1-3
- Yes → Level 4+

### 5. Meta-System Check
- [ ] Skills that generate/improve other skills?
- [ ] Hooks that update CLAUDE.md based on patterns?
- [ ] System getting better without manual intervention?

## Instructions

1. Check for CLAUDE.md existence and quality
2. Scan .claude/commands/ for skills
3. Check .claude/settings.json for hooks
4. Assess integration between components
5. Check .learnings/ for self-improvement infrastructure
6. Report current level with recommendations

## Output Format

```
## Current Level: X

### CLAUDE.md: [Good/Fair/Poor]
<assessment>

### Skills: [Good/Fair/Poor]
<assessment>

### Hooks: [Good/Fair/Poor]
<assessment>

### Integration: [Good/Fair/Poor]
<assessment>

### Recommendations
1. <priority 1>
2. <priority 2>
3. <priority 3>
```
