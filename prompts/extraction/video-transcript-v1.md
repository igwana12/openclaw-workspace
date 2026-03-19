---
name: video-transcript-extraction
version: 1
category: extraction
description: Extract key points, speakers, timestamps, and actionable items from video transcripts
author: openclaw
created_at: 2026-03-19
updated_at: 2026-03-19
tags: [video, transcript, extraction, tiktok, youtube]
status: active
context_requirements:
  - transcript_text (required)
  - video_metadata (optional)
output_format: structured_json
---

# Video Transcript Extraction

## Purpose

Extract structured information from raw video transcripts, including key points, speaker identification, timestamps, and actionable items. Works with transcripts from TikTok, YouTube, podcasts, and other video sources.

## Input Requirements

- **transcript_text** (required): Raw transcript text, ideally with timestamps
- **video_title** (optional): Title of the video for context
- **video_url** (optional): Source URL for reference
- **speaker_list** (optional): Known speakers if available

## Instructions

Analyze the provided video transcript and extract the following:

1. **Core Message**: What is the main point or thesis of the video?

2. **Key Points**: List 3-7 key takeaways in order of importance

3. **Speakers**: Identify speakers if multiple people are talking

4. **Action Items**: What actionable steps does the video suggest?

5. **Quotes**: Notable quotable statements

6. **Framework/Model**: If the video presents a framework (like "3 buckets, 7 assets"), document it clearly

7. **Timestamps**: Key moments with their approximate timestamps

8. **Classification**: Categorize the content type:
   - SKILL: Teaches a repeatable process
   - KNOWLEDGE: Provides information/context
   - OPINION: Shares perspective/viewpoint
   - ENTERTAINMENT: Primarily for engagement

## Output Format

```json
{
  "title": "string",
  "source_url": "string | null",
  "classification": "SKILL | KNOWLEDGE | OPINION | ENTERTAINMENT",
  "core_message": "string",
  "key_points": [
    "string"
  ],
  "speakers": [
    {
      "name": "string",
      "role": "string | null"
    }
  ],
  "action_items": [
    "string"
  ],
  "quotes": [
    {
      "text": "string",
      "speaker": "string | null"
    }
  ],
  "framework": {
    "name": "string | null",
    "components": ["string"]
  },
  "timestamps": [
    {
      "time": "string",
      "event": "string"
    }
  ],
  "tags": ["string"],
  "summary": "string (2-3 sentences)"
}
```

## Example

**Input:**
```
[0:00] Everyone is hoarding AI tools and still stuck.
[0:03] The teams winning built an AI Operating System before tools.
[0:07] Here's the framework: 3 buckets, 7 assets...
```

**Output:**
```json
{
  "title": "AI Operating System Framework",
  "classification": "SKILL",
  "core_message": "Build systematic AI infrastructure before adopting individual tools",
  "key_points": [
    "Teams fail by collecting tools without a system",
    "Success requires an 'AI Operating System' foundation",
    "Framework has 3 buckets containing 7 assets"
  ],
  "framework": {
    "name": "AI OS Framework",
    "components": ["Process bucket", "Context bucket", "Systems bucket"]
  }
}
```

## Notes

- Works best with transcripts that include speaker labels or timestamps
- For auto-generated captions without punctuation, accuracy may be lower
- Long videos (>30 min) benefit from chunking into segments first

## Feedback Log

<!-- Append usage feedback below this line -->
