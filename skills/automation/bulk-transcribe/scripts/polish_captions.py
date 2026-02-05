#!/usr/bin/env python3
"""
Polish YouTube captions with Gemini - add speaker ID and formatting.

Much cheaper than audio transcription (~$0.05 vs $0.10 per episode)
since we're only processing text, not audio.
"""

import os
import re
from pathlib import Path
from dotenv import load_dotenv

from google import genai
from google.genai import types

# Load API key
load_dotenv(Path(__file__).parent.parent.parent / "shared-backend" / ".env", override=True)

# Paths
PROJECT_DIR = Path(__file__).parent.parent
YOUTUBE_CAPTIONS_DIR = PROJECT_DIR / "data" / "youtube-captions"
POLISHED_DIR = PROJECT_DIR / "data" / "polished-transcripts"

# Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

POLISH_PROMPT = """You are editing a raw YouTube auto-caption transcript for the My First Million podcast.

## Podcast Context

**Hosts:**
- **Sam Parr**: Co-founder of The Hustle (sold to HubSpot). Energetic, sales-focused. Does sponsor reads.
- **Shaan Puri**: Former Twitch/Bebo. Calmer, analytical. Usually opens episodes.

**Format:** Conversational podcast. Usually Sam and Shaan, sometimes with guests.

## Your Task

Clean up the transcript while preserving the conversational voice.

### 1. Speaker Identification
- Add `**Sam:**` or `**Shaan:**` labels based on context clues
- "When I sold The Hustle" = Sam, references to Twitch/Bebo = Shaan
- For guests, use their name once identified, otherwise `**Guest:**`

### 2. Section Headers
- Add `## Descriptive Topic Name` at natural topic breaks
- Aim for 8-15 sections per hour

### 3. Cleanup Rules

**ALWAYS REMOVE:**
- Stutters and repeated words: "I I think" → "I think", "the the" → "the"
- Filler sounds: um, uh, ah
- False starts: "I was going to— actually let me say it this way"
- `>>` markers and HTML entities (&gt; &amp; etc.)
- Excessive "like" (keep some, remove when it's every other word)

**ALWAYS KEEP:**
- Natural phrases: "you know", "right?", "man", "dude"
- The speaker's actual words and meaning
- Conversational rhythm and back-and-forth
- Short interjections: "Yeah", "Right", "Exactly", "Okay"

**FIX:**
- Obvious transcription errors
- Run-on sentences - break into readable chunks
- Missing punctuation

### 4. COMPLETELY REMOVE Sponsors/Ads

This is critical. DELETE ENTIRELY any:
- Sponsor reads ("So I got something cool to share...", "thanks to our sponsors")
- HubSpot mentions, MFM vault plugs
- Promo codes, "check out X", "click the link"
- Product pitches mid-episode

Just cut them out completely. Don't leave any trace.

### 5. Formatting
- Break up long speaker turns into paragraphs
- Each speaker turn should be readable, not a wall of text
- New paragraph within a speaker turn when topic shifts

## Quality Standard

Should read like a podcast transcript that's been cleaned for publication - natural and conversational, but without the verbal clutter.

**CRITICAL: This is NOT a summarization task.**
- Keep ALL dialogue exchanges - don't merge or condense conversations
- Keep the back-and-forth rhythm intact
- If someone says 5 sentences, output should have ~5 sentences (just cleaned)
- Output length should be 70-90% of input length, not 20%

## Output Format

2-3 sentence summary, then:

**Topics:** tag1, tag2, tag3
**Speakers:** Name1, Name2

---

## Section Title

**Speaker:** Cleaned content in readable paragraphs...

---

## Raw Transcript to Polish

Title: {title}

{transcript}
"""


def extract_transcript_text(file_path: Path) -> tuple[str, str]:
    """Extract title and transcript text from YouTube caption file."""
    content = file_path.read_text()

    # Extract title from frontmatter
    title_match = re.search(r'title:\s*"([^"]+)"', content)
    title = title_match.group(1) if title_match else file_path.stem

    # Get transcript (everything after the note about auto-generation)
    parts = content.split("> **Note:**")
    if len(parts) > 1:
        # Get everything after the note line
        transcript = parts[1].split("\n", 2)[-1].strip()
    else:
        # Just get the body
        transcript = content.split("---", 2)[-1].strip()

    return title, transcript


def polish_transcript(title: str, transcript: str) -> tuple[str, dict]:
    """Polish transcript using Gemini."""

    prompt = POLISH_PROMPT.format(title=title, transcript=transcript)

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=65536,
            temperature=0.1,
            thinking_config=types.ThinkingConfig(
                thinking_budget=4096,  # Reasoning for cleanup decisions
            ),
        ),
    )

    token_info = {
        "input_tokens": getattr(response.usage_metadata, 'prompt_token_count', 0) if response.usage_metadata else 0,
        "output_tokens": getattr(response.usage_metadata, 'candidates_token_count', 0) if response.usage_metadata else 0,
    }

    return response.text, token_info


def save_polished(file_id: str, title: str, polished_text: str, youtube_id: str = ""):
    """Save polished transcript."""
    POLISHED_DIR.mkdir(parents=True, exist_ok=True)

    frontmatter = f"""---
title: "{title.replace('"', "'")}"
source: youtube_captions_polished
youtube_id: "{youtube_id}"
status: polished
---

"""
    output_path = POLISHED_DIR / f"{file_id}.md"
    output_path.write_text(frontmatter + polished_text)
    return output_path


def process_file(file_path: Path) -> bool:
    """Process a single YouTube caption file."""
    file_id = file_path.stem
    print(f"\n[{file_id}] Processing...")

    try:
        title, transcript = extract_transcript_text(file_path)
        print(f"  Title: {title[:50]}...")
        print(f"  Input: {len(transcript):,} chars")

        polished, tokens = polish_transcript(title, transcript)

        # Calculate cost
        input_cost = (tokens["input_tokens"] / 1_000_000) * 0.10  # Flash text input
        output_cost = (tokens["output_tokens"] / 1_000_000) * 0.40  # Flash text output
        total_cost = input_cost + output_cost

        print(f"  Tokens: {tokens['input_tokens']:,} in / {tokens['output_tokens']:,} out")
        print(f"  Cost: ${total_cost:.4f}")
        print(f"  Output: {len(polished):,} chars")

        # Extract youtube_id from original file
        content = file_path.read_text()
        yt_match = re.search(r'youtube_id:\s*"([^"]+)"', content)
        youtube_id = yt_match.group(1) if yt_match else ""

        output_path = save_polished(file_id, title, polished, youtube_id)
        print(f"  Saved: {output_path.name}")

        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def main(limit: int = 5, skip_existing: bool = True):
    """Polish YouTube caption files."""
    print(f"\n{'='*60}")
    print("YOUTUBE CAPTION POLISHER")
    print(f"{'='*60}\n")

    # Get existing polished files
    existing = set()
    if skip_existing and POLISHED_DIR.exists():
        for f in POLISHED_DIR.glob("*.md"):
            existing.add(f.stem)
        print(f"Found {len(existing)} existing polished files")

    # Get caption files to process
    caption_files = sorted(YOUTUBE_CAPTIONS_DIR.glob("*.md"))
    to_process = [f for f in caption_files if f.stem not in existing][:limit]

    print(f"Found {len(caption_files)} caption files, {len(to_process)} to process")

    success = 0
    total_cost = 0.0

    for i, file_path in enumerate(to_process, 1):
        print(f"\n[{i}/{len(to_process)}]")
        if process_file(file_path):
            success += 1

    print(f"\n{'='*60}")
    print(f"COMPLETE: {success}/{len(to_process)} polished")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=5, help="Max files to process")
    parser.add_argument("--no-skip", action="store_true", help="Don't skip existing")
    parser.add_argument("--file", type=str, help="Process a single file by name")
    args = parser.parse_args()

    if args.file:
        file_path = YOUTUBE_CAPTIONS_DIR / f"{args.file}.md"
        if file_path.exists():
            process_file(file_path)
        else:
            print(f"File not found: {file_path}")
    else:
        main(limit=args.limit, skip_existing=not args.no_skip)
