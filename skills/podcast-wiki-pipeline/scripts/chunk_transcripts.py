#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

from utils import load_manifest, write_text

RX_MARKER = re.compile(r"^\[(\d{1,2}:)?\d{1,2}:\d{2}\]$")


def parse_marked_transcript(text: str):
    lines = text.splitlines()
    segments = []
    current_ts = None
    buffer = []
    in_frontmatter = False

    for line in lines:
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue

        stripped = line.strip()
        if not stripped:
            continue
        if RX_MARKER.match(stripped):
            if buffer:
                segments.append({"timestamp": current_ts, "text": " ".join(buffer).strip()})
                buffer = []
            current_ts = stripped.strip("[]")
            continue
        if stripped.startswith("# "):
            continue
        buffer.append(stripped)

    if buffer:
        segments.append({"timestamp": current_ts, "text": " ".join(buffer).strip()})

    return segments


def chunk_segments(segments, min_words: int, max_words: int):
    chunks = []
    current = []
    current_words = 0
    start_ts = None

    def flush(end_ts=None):
        nonlocal current, current_words, start_ts
        if not current:
            return
        text = " ".join(seg["text"] for seg in current).strip()
        chunks.append(
            {
                "timestamp_start": start_ts,
                "timestamp_end": end_ts or (current[-1].get("timestamp")),
                "word_count": current_words,
                "text": text,
            }
        )
        current = []
        current_words = 0
        start_ts = None

    for seg in segments:
        words = len(seg["text"].split())
        if start_ts is None:
            start_ts = seg.get("timestamp")
        if current_words + words > max_words and current_words >= min_words:
            flush(seg.get("timestamp"))
        current.append(seg)
        current_words += words

    flush()
    return chunks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--min-words", type=int, default=500)
    parser.add_argument("--max-words", type=int, default=1500)
    args = parser.parse_args()

    project_root = Path(args.project_root)
    data_dir = project_root / "data"
    manifest_path = data_dir / "manifest.jsonl"
    chunks_dir = data_dir / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    entries = load_manifest(manifest_path)
    for entry in entries:
        transcript_path = entry.get("transcript_path")
        if not transcript_path:
            continue
        transcript_file = Path(transcript_path)
        if not transcript_file.exists():
            continue

        text = transcript_file.read_text(errors="ignore")
        segments = parse_marked_transcript(text)
        if not segments:
            continue

        chunks = chunk_segments(segments, args.min_words, args.max_words)
        payload = {
            "episode_id": entry.get("id"),
            "title": entry.get("title"),
            "date": entry.get("date"),
            "source_url": entry.get("link"),
            "chunks": [
                {
                    "chunk_index": idx,
                    "timestamp_start": c["timestamp_start"],
                    "timestamp_end": c["timestamp_end"],
                    "word_count": c["word_count"],
                    "text": c["text"],
                }
                for idx, c in enumerate(chunks)
            ],
        }

        out_path = chunks_dir / f"{entry.get('id')}.json"
        write_text(out_path, json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
