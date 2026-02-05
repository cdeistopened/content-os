# Transcript Frontmatter Standard

Every transcript markdown file should start with YAML frontmatter:

```yaml
---
type: episode
show: "Show Name"
title: "Episode Title"
date: "YYYY-MM-DD"
source_url: "https://..."
audio_url: "https://..."  # null if missing
transcript_source: "rss_transcript|youtube_vtt|audio_stt"
transcript_quality: "raw|polished"
video_id: "YouTube ID"     # optional
---
```

Rules:
- Always include `type`, `show`, `title`, `date`, `source_url`.
- `audio_url` can be null.
- `transcript_quality` is `raw` for initial ingest.
