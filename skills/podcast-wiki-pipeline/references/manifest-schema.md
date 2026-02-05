# Manifest Schema (JSONL)

Each line is one JSON object:

```json
{
  "id": "unique-id",
  "title": "Episode title",
  "date": "YYYY-MM-DD",
  "link": "https://...",
  "audio_url": "https://...",
  "transcript_url": "https://...",
  "youtube_url": "https://...",
  "video_id": "YouTube ID",
  "status": "pending|done|skipped|needs_stt",
  "transcript_path": "data/transcripts/raw/...md",
  "notes": []
}
```

Status meanings:
- `pending` not processed
- `done` transcript saved
- `needs_stt` no transcript found
- `skipped` excluded by user
