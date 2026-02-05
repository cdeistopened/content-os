#!/usr/bin/env python3
"""
Scrape YouTube captions for MFM episodes.

Uses yt-dlp to download auto-generated captions from YouTube videos.
Stores as placeholder transcripts until Gemini audio transcription is done.
"""

import subprocess
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Optional

# Paths
BASE_DIR = Path(__file__).parent.parent
AUDIO_TRANSCRIPTS_DIR = BASE_DIR / "data" / "audio-transcripts"
YOUTUBE_CAPTIONS_DIR = BASE_DIR / "data" / "youtube-captions"
VIDEO_CACHE_FILE = BASE_DIR / "pipeline" / "youtube_videos.json"

# MFM YouTube channel
CHANNEL_URL = "https://www.youtube.com/@MyFirstMillionPod"


def get_existing_transcripts() -> set[str]:
    """Get IDs of episodes that already have Gemini transcripts."""
    existing = set()
    if AUDIO_TRANSCRIPTS_DIR.exists():
        for f in AUDIO_TRANSCRIPTS_DIR.glob("*.md"):
            existing.add(f.stem)
    return existing


def slugify(title: str) -> str:
    """Convert title to filename-safe slug."""
    # Remove special characters, lowercase, replace spaces with underscores
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s-]+', '_', slug)
    return slug[:30]  # Match the truncation in transcribe_audio.py


def get_channel_videos(limit: int = 100) -> list[dict]:
    """Get list of videos from the MFM YouTube channel."""
    print(f"Fetching up to {limit} videos from MFM YouTube channel...")

    # Use yt-dlp to get video list
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--print", '{"id": "%(id)s", "title": "%(title)s", "upload_date": "%(upload_date)s"}',
        "--playlist-end", str(limit),
        f"{CHANNEL_URL}/videos"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    videos = []
    for line in result.stdout.strip().split('\n'):
        if line:
            try:
                video = json.loads(line)
                videos.append(video)
            except json.JSONDecodeError:
                continue

    print(f"Found {len(videos)} videos")
    return videos


def download_captions(video_id: str, title: str) -> Optional[str]:
    """Download captions for a single video. Returns VTT content or None."""
    print(f"  Downloading captions for: {title[:50]}...")

    # Create temp dir for download
    temp_dir = Path("/tmp/yt_captions")
    temp_dir.mkdir(exist_ok=True)

    cmd = [
        "yt-dlp",
        "--write-auto-sub",
        "--sub-lang", "en",
        "--skip-download",
        "--sub-format", "vtt",
        "-o", str(temp_dir / "%(id)s"),
        f"https://www.youtube.com/watch?v={video_id}"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Look for the downloaded subtitle file
    vtt_file = temp_dir / f"{video_id}.en.vtt"
    if vtt_file.exists():
        content = vtt_file.read_text()
        vtt_file.unlink()  # Clean up
        return content

    # Try alternative naming
    for f in temp_dir.glob(f"{video_id}*.vtt"):
        content = f.read_text()
        f.unlink()
        return content

    print(f"    No captions found for {video_id}")
    return None


def vtt_to_text(vtt_content: str) -> str:
    """Convert VTT captions to plain text, removing timestamps and duplicates."""
    lines = []
    seen = set()

    for line in vtt_content.split('\n'):
        # Skip VTT header, timestamps, and empty lines
        if line.startswith('WEBVTT') or '-->' in line or not line.strip():
            continue
        # Skip numeric cue identifiers
        if line.strip().isdigit():
            continue
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', line).strip()
        if clean and clean not in seen:
            seen.add(clean)
            lines.append(clean)

    return ' '.join(lines)


def save_caption_transcript(video_id: str, title: str, text: str, upload_date: str):
    """Save caption transcript as markdown file."""
    slug = slugify(title)

    # Format date
    if upload_date and len(upload_date) == 8:
        date_str = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")

    content = f"""---
title: "{title}"
source: youtube_captions
youtube_id: "{video_id}"
date: "{date_str}"
status: placeholder
---

# {title}

> **Note:** This transcript was auto-generated from YouTube captions. It may contain errors and lacks speaker identification. A full Gemini audio transcript will replace this.

{text}
"""

    YOUTUBE_CAPTIONS_DIR.mkdir(parents=True, exist_ok=True)
    output_file = YOUTUBE_CAPTIONS_DIR / f"{slug}.md"
    output_file.write_text(content)
    print(f"    Saved: {slug}.md ({len(text):,} chars)")
    return output_file


def main(limit: int = 100, skip_existing: bool = True):
    """Main function to scrape YouTube captions."""
    print(f"\n{'='*60}")
    print("MFM YouTube Caption Scraper")
    print(f"{'='*60}\n")

    # Get existing Gemini transcripts to skip
    existing_gemini = get_existing_transcripts()
    print(f"Found {len(existing_gemini)} existing Gemini transcripts")

    # Get existing YouTube captions to skip
    existing_yt = set()
    if YOUTUBE_CAPTIONS_DIR.exists():
        for f in YOUTUBE_CAPTIONS_DIR.glob("*.md"):
            existing_yt.add(f.stem)
    print(f"Found {len(existing_yt)} existing YouTube caption files")

    # Get videos from channel
    videos = get_channel_videos(limit)

    # Process each video
    processed = 0
    skipped_gemini = 0
    skipped_yt = 0
    failed = 0

    for i, video in enumerate(videos, 1):
        video_id = video.get('id', '')
        title = video.get('title', 'Unknown')
        upload_date = video.get('upload_date', '')
        slug = slugify(title)

        print(f"\n[{i}/{len(videos)}] {title[:60]}...")

        # Skip if we have a Gemini transcript
        if skip_existing and slug in existing_gemini:
            print(f"  Skipping (has Gemini transcript)")
            skipped_gemini += 1
            continue

        # Skip if we already have YouTube captions
        if skip_existing and slug in existing_yt:
            print(f"  Skipping (has YouTube captions)")
            skipped_yt += 1
            continue

        # Download captions
        vtt_content = download_captions(video_id, title)
        if not vtt_content:
            failed += 1
            continue

        # Convert to text
        text = vtt_to_text(vtt_content)
        if len(text) < 100:
            print(f"  Skipping (caption too short: {len(text)} chars)")
            failed += 1
            continue

        # Save
        save_caption_transcript(video_id, title, text, upload_date)
        processed += 1

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"  Processed: {processed}")
    print(f"  Skipped (Gemini exists): {skipped_gemini}")
    print(f"  Skipped (YT captions exist): {skipped_yt}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(videos)}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scrape YouTube captions for MFM episodes")
    parser.add_argument("--limit", type=int, default=100, help="Max videos to process")
    parser.add_argument("--no-skip", action="store_true", help="Don't skip existing files")
    args = parser.parse_args()

    main(limit=args.limit, skip_existing=not args.no_skip)
