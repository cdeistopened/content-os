#!/usr/bin/env python3
"""
MFM Gemini Audio Transcription - PARALLEL VERSION

Runs multiple transcriptions concurrently for 3-5x speedup.
"""

import json
import os
import re
import tempfile
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional
from urllib.request import urlopen, Request
from dotenv import load_dotenv
from threading import Lock

from google import genai
from google.genai import types

# Load API key
load_dotenv(Path(__file__).parent.parent.parent / "shared-backend" / ".env", override=True)

# Paths
PROJECT_DIR = Path(__file__).parent.parent
RSS_PATH = Path("/Users/charliedeist/Desktop/New Root Docs/Creative Intelligence Agency/doodle-reader/public/feeds/mfm.xml")
AUDIO_TRANSCRIPTS_DIR = PROJECT_DIR / "data" / "audio-transcripts"

# Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Thread-safe logging
print_lock = Lock()
csv_lock = Lock()

# Progress tracking
completed_count = 0
total_count = 0

# MFM context for speaker identification
MFM_CONTEXT = """
# My First Million Podcast

## Hosts
- Sam Parr: Co-founder of The Hustle (sold to HubSpot), business/sales focused, often does sponsor reads
- Shaan Puri: Former Twitch/Bebo product lead, investor, more analytical/tech focused, usually does episode intros

## Format
- Usually Sam and Shaan discussing business ideas, trends, and stories
- Guest episodes follow pattern: one host interviews a guest
- Casual, conversational tone with tangents and jokes

## Common Topics
Business ideas, startups, entrepreneurship, wealth building, interesting people/stories
"""

TRANSCRIPTION_PROMPT = """You are a professional transcriptionist for the My First Million podcast.

Episode: "{title}"
{description}

{context}

## PRIORITY REASONING TASKS (spend thinking time here)

### 1. Speaker Identification
Listen carefully for:
- How speakers address each other by name ("Sam, what do you think?" / "Shaan, tell me about...")
- Voice characteristics (pitch, pace, energy level)
- Introduction of guests ("Welcome back, [Name]" / "Today we have [Name]")
- Self-references ("When I sold The Hustle..." = Sam)

Known hosts:
- **Sam Parr**: Founded The Hustle, sold to HubSpot. Louder, sales-focused, does sponsor reads.
- **Shaan Puri**: Former Twitch/Bebo. Calmer, analytical, usually opens episodes.

For guests: Identify from introductions. If unclear, use **Guest:** until name is revealed.

### 2. Topic Segmentation for Chunking
Add `## Section Header [MM:SS]` at NATURAL BREAK POINTS:
- New topic introduction ("Let's talk about..." / "Next category...")
- Guest introductions
- Major subject changes
- After sponsor breaks (which you'll remove)

Aim for 8-15 sections per hour. Each section = one semantic chunk for RAG retrieval.

## Output Format

1. One paragraph summary (2-3 sentences)
2. **Topics:** comma-separated tags
3. **Speakers:** list all identified speakers
4. Full transcript with:
   - `## Section Title [MM:SS]` headers at topic breaks
   - `**Name:**` speaker labels
   - Clean paragraphs

## Rules

- Transcribe EVERYTHING verbatim - do NOT summarize content
- REMOVE sponsor/ad reads entirely (don't wrap, just omit)
- Fix obvious speech-to-text errors
- Preserve speaker's natural voice and word choices

---

Begin transcription:
"""


def safe_print(*args, **kwargs):
    """Thread-safe print."""
    with print_lock:
        print(*args, **kwargs, flush=True)


def download_audio(url: str, max_size_mb: int = 200) -> Optional[bytes]:
    """Download audio file from URL."""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=120) as response:
            content_length = response.headers.get('Content-Length')
            if content_length and int(content_length) > max_size_mb * 1024 * 1024:
                return None
            return response.read()
    except Exception as e:
        return None


def transcribe_audio(audio_data: bytes, title: str, description: str) -> tuple[str, dict]:
    """Transcribe audio using Gemini 3 Flash Preview."""

    prompt = TRANSCRIPTION_PROMPT.format(
        title=title,
        description=f"Description: {description}" if description else "",
        context=MFM_CONTEXT
    )

    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        f.write(audio_data)
        temp_path = f.name

    try:
        uploaded_file = client.files.upload(file=temp_path)

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_uri(file_uri=uploaded_file.uri, mime_type="audio/mpeg"),
                        types.Part.from_text(text=prompt),
                    ],
                ),
            ],
            config=types.GenerateContentConfig(
                max_output_tokens=65536,
                temperature=0.1,
                thinking_config=types.ThinkingConfig(thinking_budget=8192),
            ),
        )

        token_info = {
            "input_tokens": getattr(response.usage_metadata, 'prompt_token_count', 0) if response.usage_metadata else 0,
            "output_tokens": getattr(response.usage_metadata, 'candidates_token_count', 0) if response.usage_metadata else 0,
        }

        try:
            client.files.delete(name=uploaded_file.name)
        except:
            pass

        return response.text, token_info

    finally:
        os.unlink(temp_path)


def log_tokens(episode_id: str, title: str, input_tokens: int, output_tokens: int, output_chars: int):
    """Thread-safe token logging."""
    csv_path = PROJECT_DIR / "pipeline" / "token_usage.csv"

    with csv_lock:
        write_header = not csv_path.exists()
        with open(csv_path, 'a') as f:
            if write_header:
                f.write("episode_id,title,input_tokens,output_tokens,output_chars,input_cost,output_cost,total_cost\n")
            input_cost = (input_tokens / 1_000_000) * 1.00
            output_cost = (output_tokens / 1_000_000) * 3.00
            total_cost = input_cost + output_cost
            f.write(f'"{episode_id}","{title[:50]}",{input_tokens},{output_tokens},{output_chars},{input_cost:.4f},{output_cost:.4f},{total_cost:.4f}\n')


def process_episode(episode: dict, index: int, total: int) -> bool:
    """Process a single episode (called from thread)."""
    global completed_count

    video_id = episode["video_id"]
    title = episode["title"]

    safe_print(f"[{index}/{total}] Starting: {title[:50]}...")

    # Download
    audio_data = download_audio(episode["audio_url"])
    if not audio_data:
        safe_print(f"[{index}/{total}] FAILED download: {title[:40]}")
        return False

    size_mb = len(audio_data) / 1024 / 1024
    safe_print(f"[{index}/{total}] Downloaded {size_mb:.1f}MB: {title[:40]}")

    # Transcribe
    try:
        transcript, tokens = transcribe_audio(audio_data, title, episode["description"])

        # Save
        AUDIO_TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        output_path = AUDIO_TRANSCRIPTS_DIR / f"{video_id}.md"

        frontmatter = f"""---
title: "{title.replace('"', "'")}"
video_id: {video_id}
source: gemini-audio
---

"""
        output_path.write_text(frontmatter + transcript)

        log_tokens(video_id, title, tokens["input_tokens"], tokens["output_tokens"], len(transcript))

        completed_count += 1
        safe_print(f"[{index}/{total}] ✓ DONE ({tokens['input_tokens']:,} in / {tokens['output_tokens']:,} out): {title[:40]}")

        return True

    except Exception as e:
        safe_print(f"[{index}/{total}] ERROR: {title[:40]} - {e}")
        return False


def get_rss_episodes_direct(limit: int = 5, offset: int = 0, skip_existing: bool = True) -> list[dict]:
    """Get episodes with audio directly from RSS."""
    tree = ET.parse(RSS_PATH)
    root = tree.getroot()

    existing_ids = set()
    if skip_existing and AUDIO_TRANSCRIPTS_DIR.exists():
        for f in AUDIO_TRANSCRIPTS_DIR.glob("*.md"):
            existing_ids.add(f.stem)
        safe_print(f"Found {len(existing_ids)} existing transcripts")

    episodes = []
    skipped = 0

    for item in root.findall('.//item'):
        if len(episodes) >= limit:
            break

        title = item.find('title').text if item.find('title') is not None else ""
        description = item.find('description').text if item.find('description') is not None else ""

        enclosure = item.find('enclosure')
        if enclosure is not None:
            audio_url = enclosure.get('url')
            audio_type = enclosure.get('type', '')
            if audio_url and ('audio' in audio_type or audio_url.endswith('.mp3')):
                simple_id = re.sub(r'[^\w]', '_', title[:30]).lower()

                if skipped < offset:
                    skipped += 1
                    continue

                if skip_existing and simple_id in existing_ids:
                    safe_print(f"  Skipping (exists): {title[:40]}...")
                    continue

                episodes.append({
                    "video_id": simple_id,
                    "title": title,
                    "audio_url": audio_url,
                    "description": description[:500] if description else "",
                })

    return episodes


def main(limit: int = 5, workers: int = 3, offset: int = 0, skip_existing: bool = True):
    """Run parallel Gemini audio transcription."""
    global total_count, completed_count

    print(f"\n{'='*60}")
    print(f"PARALLEL TRANSCRIPTION ({workers} workers)")
    print(f"{'='*60}\n")

    episodes = get_rss_episodes_direct(limit, offset, skip_existing)
    total_count = len(episodes)
    completed_count = 0

    print(f"\nFound {total_count} episodes to transcribe")
    if not episodes:
        print("No episodes found!")
        return

    start_time = time.time()
    success = 0

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(process_episode, ep, i, total_count): ep
            for i, ep in enumerate(episodes, 1)
        }

        for future in as_completed(futures):
            try:
                if future.result():
                    success += 1
            except Exception as e:
                safe_print(f"Task exception: {e}")

    elapsed = time.time() - start_time

    print(f"\n{'='*60}")
    print(f"COMPLETE")
    print(f"{'='*60}")
    print(f"  Success: {success}/{total_count}")
    print(f"  Time: {elapsed/60:.1f} minutes")
    print(f"  Avg: {elapsed/max(success,1):.1f}s per episode")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=5, help="Max episodes")
    parser.add_argument("--workers", type=int, default=3, help="Concurrent workers (default: 3)")
    parser.add_argument("--offset", type=int, default=0, help="Skip first N episodes")
    parser.add_argument("--no-skip", action="store_true", help="Don't skip existing")
    args = parser.parse_args()

    main(limit=args.limit, workers=args.workers, offset=args.offset, skip_existing=not args.no_skip)
