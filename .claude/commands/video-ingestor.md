# Video Ingestor

Ingest and process video content from URLs (TikTok, YouTube, etc.) to extract transcripts, key frames, and summaries.

## Instructions

1. **Validate the video URL**
   - Accept TikTok, YouTube, Vimeo, and direct video URLs
   - Return clear error if URL is invalid or unsupported

2. **Extract transcript**
   - Use available transcription services or APIs
   - Handle videos without captions gracefully

3. **Extract key frames**
   - Identify 3-5 representative frames from the video
   - Capture at significant scene changes or key moments

4. **Generate summary**
   - Summarize the video content in 2-3 sentences
   - Include key topics, speakers, or themes

## Output Format

Return a JSON object with the following structure:

```json
{
  "url": "<original video url>",
  "transcript": "<full transcript text>",
  "frames": ["<frame1_path>", "<frame2_path>", "<frame3_path>"],
  "summary": "<2-3 sentence summary>",
  "metadata": {
    "duration_seconds": 120,
    "platform": "tiktok|youtube|other",
    "title": "<video title if available>"
  }
}
```

## Error Handling

If processing fails, return:

```json
{
  "error": "<descriptive error message>",
  "url": "<original url>",
  "stage": "validation|transcript|frames|summary"
}
```

## Requirements

- MUST validate URL before processing
- MUST extract transcript (even if empty for audio-only)
- MUST extract at least 3 key frames
- MUST generate summary
- MUST NOT expose any API keys in output
- MUST NOT include user credentials or tokens

## Integration

- Check Extreme Pro drive for cached video assets: `/Volumes/Extreme Pro/video injestor/`
- Save processed outputs for future reference
- Reference CLAUDE.md for output conventions

## Example Usage

User: "Process this TikTok video: https://vm.tiktok.com/ZMrExample123/"

Response: Process the video and return structured JSON with transcript, frames, and summary.
