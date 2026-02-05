# yt-dlp Integration

Download video, audio, and transcripts from YouTube and 1000+ other sites.

## Install

```bash
brew install yt-dlp
# or
pip install yt-dlp
```

## Used By

- **youtube-downloader** — Download transcripts as clean text
- **youtube-clip-extractor** — Download full videos for clipping
- **twitter-scraper** — Download audio from X/Twitter posts

## Common Commands

```bash
# Download transcript only
yt-dlp --write-auto-sub --sub-lang en --skip-download -o "%(title)s" URL

# Download video (best quality)
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" URL

# Download audio only
yt-dlp -x --audio-format mp3 URL

# List available formats
yt-dlp -F URL
```

## Troubleshooting

- **"Video unavailable"**: Check if the video is region-locked or private
- **Slow downloads**: Add `--concurrent-fragments 4`
- **Update**: `brew upgrade yt-dlp` or `pip install -U yt-dlp`
