---
name: slack-thread-summarization
version: 2
category: summarization
description: Summarize Slack threads extracting decisions, action items, and key discussion points
author: openclaw
created_at: 2026-03-19
updated_at: 2026-03-19
tags: [slack, thread, summarization, action-items, decisions]
status: active
context_requirements:
  - thread_messages (required)
  - channel_context (optional)
output_format: structured_markdown
---

# Slack Thread Summarization

## Purpose

Summarize Slack threads to extract decisions made, action items assigned, key discussion points, and unresolved questions. Designed to turn long async conversations into scannable summaries.

## Input Requirements

- **thread_messages** (required): The Slack thread content, including:
  - Message text
  - Author/sender
  - Timestamps
  - Reactions (if available)
- **channel_context** (optional): What channel this is from, for context
- **participants** (optional): List of people in the thread

## Instructions

Analyze the Slack thread and produce a structured summary:

1. **TL;DR**: One-sentence summary of what this thread is about

2. **Decisions Made**: Any explicit or implicit decisions reached
   - Include who made/approved the decision
   - Note any dissenting opinions

3. **Action Items**: Tasks mentioned or assigned
   - Format: `[ ] Task description (@owner, deadline if mentioned)`
   - Mark completed items with `[x]`

4. **Key Discussion Points**: Main topics covered
   - Summarize different viewpoints if there was debate

5. **Unresolved Questions**: Open items needing follow-up

6. **Stakeholders**: Key people involved and their roles in the discussion

7. **Links & References**: Any URLs, docs, or external resources mentioned

## Output Format

```markdown
## Thread Summary: [Brief Title]

**Channel:** #channel-name
**Date:** YYYY-MM-DD
**Participants:** @person1, @person2, @person3

### TL;DR
[One sentence summary]

### Decisions
- ✅ [Decision 1] (decided by @person)
- ✅ [Decision 2]

### Action Items
- [ ] [Task 1] (@owner, due: date)
- [ ] [Task 2] (@owner)
- [x] [Completed task]

### Key Points
1. **[Topic 1]**: Summary of discussion
2. **[Topic 2]**: Summary of discussion

### Open Questions
- ❓ [Question that needs follow-up]

### References
- [Link title](url)
- Document: [doc name]
```

## Example

**Input:**
```
@alice: Should we use React or Vue for the new dashboard?
@bob: React - we have more experience with it
@charlie: +1 for React, but let's consider Vue's learning curve
@alice: OK let's go with React. @bob can you set up the project?
@bob: Sure, I'll have it ready by Friday
```

**Output:**
```markdown
## Thread Summary: Frontend Framework Decision

**Participants:** @alice, @bob, @charlie

### TL;DR
Team decided to use React for the new dashboard based on existing experience.

### Decisions
- ✅ Use React for new dashboard (decided by @alice after team input)

### Action Items
- [ ] Set up React project (@bob, due: Friday)

### Key Points
1. **Framework choice**: React chosen over Vue due to team's existing experience
2. **Considerations**: Vue's learning curve was noted but not a deciding factor
```

## Notes

- v2 improvements over v1: Added reactions parsing, better action item detection
- Handles threads with 50+ messages well
- For very long threads, consider asking for the most recent N messages

## Feedback Log

<!-- Append usage feedback below this line -->
