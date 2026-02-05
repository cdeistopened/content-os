# ffmpeg Integration

Video and audio processing toolkit.

## Install

```bash
brew install ffmpeg
```

## Used By

- **youtube-clip-extractor** — Cut clips from downloaded videos
- **video-caption-creation** — Overlay captions on video
- **short-form-video** — Process short-form content

## Common Commands

```bash
# Cut a clip (no re-encode, fast)
ffmpeg -ss 00:01:30 -to 00:02:45 -i input.mp4 -c copy clip.mp4

# Cut with re-encode (precise timing)
ffmpeg -ss 00:01:30 -to 00:02:45 -i input.mp4 -c:v libx264 -c:a aac clip.mp4

# Extract audio
ffmpeg -i input.mp4 -vn -acodec libmp3lame output.mp3

# Get video info
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4
```
