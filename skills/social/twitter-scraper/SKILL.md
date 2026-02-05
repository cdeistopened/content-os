---
name: twitter-scraper
description: Fetch audio from an X/Twitter post URL and produce a transcript using yt-dlp + Whisper. Use when a user asks for a transcript of an X post, video, or voice clip, or when you need to download tweet media and transcribe it locally.
---

# Twitter Scraper

## Overview

Download audio from an X/Twitter post and generate a transcript locally with Whisper. Prefer unauthenticated download first; fall back to browser cookies only if needed.

## Workflow

### 1) Download audio (unauthenticated first)

Use yt-dlp to extract the best audio stream and convert to M4A.

```bash
yt-dlp --no-cookies --no-cookies-from-browser -f ba --extract-audio --audio-format m4a \
  -o '/tmp/x_post_audio.%(ext)s' 'https://x.com/<user>/status/<id>'
```

If that fails, retry with Arc cookies via the Chromium loader (Arc stores Chromium profiles).

```bash
yt-dlp --cookies-from-browser "chrome:/Users/charliedeist/Library/Application Support/Arc/User Data/Default" \
  -f ba --extract-audio --audio-format m4a \
  -o '/tmp/x_post_audio.%(ext)s' 'https://x.com/<user>/status/<id>'
```

If the user uses a non-default Arc profile, try `Profile 1`, `Profile 2`, etc. in the Arc `User Data` directory.

### 2) Transcribe with Whisper

Use `tiny` for speed; retry with `small` if accuracy is insufficient.

```bash
whisper /tmp/x_post_audio.m4a --model tiny --output_dir /tmp --output_format txt
```

Optional higher accuracy:

```bash
whisper /tmp/x_post_audio.m4a --model small --output_dir /tmp --output_format txt
```

### 3) Return results

Share the transcript from `/tmp/x_post_audio.txt`. Mention the output path and offer a higher-accuracy pass if needed.

## Notes

- Ensure `yt-dlp`, `ffmpeg`, and `whisper` are installed before running.
- Keep temporary artifacts in `/tmp` unless the user requests a workspace path.
- Avoid printing or storing cookies or API keys in logs or files.
