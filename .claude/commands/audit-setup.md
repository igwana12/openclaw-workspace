# Audit Setup

Run a maturity audit of this workspace's Claude Code setup against the 5-level framework.

## Instructions

1. **Check for components**:
   ```bash
   # CLAUDE.md exists and has content?
   test -s CLAUDE.md && echo "CLAUDE.md: EXISTS" || echo "CLAUDE.md: MISSING"

   # Skills directory has files?
   ls -la .claude/commands/ 2>/dev/null || echo "Skills: NONE"

   # Settings with hooks?
   cat .claude/settings.json 2>/dev/null || echo "Hooks: NONE"
   ```

2. **Score against framework**:

   | Level | Requirement | Check |
   |-------|-------------|-------|
   | 1 | CLAUDE.md exists and is project-specific | Read and evaluate |
   | 2 | Skills exist and are purposeful | Count and review |
   | 3 | Hooks exist and automate real tasks | Check settings.json |
   | 4 | Components reference each other | Cross-check files |
   | 5 | Self-improving behaviors exist | Look for meta-skills |

3. **Report findings**:
   - Current level (0-5)
   - What's working well
   - Specific gaps to address
   - Next recommended action

4. **Update audit document** if `CLAUDE-CODE-MATURITY-AUDIT.md` exists:
   - Mark completed checklist items
   - Note the audit date and findings

## Integration

This skill references the maturity framework defined in `CLAUDE-CODE-MATURITY-AUDIT.md` and validates against conventions in `CLAUDE.md`.
