#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

RX_MARKER = re.compile(r"^\[(\d{1,2}:)?\d{1,2}:\d{2}\]$")


def parse_markers(text: str):
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


def infer_topic_type(text: str) -> str:
    lower = text.lower()
    if "welcome" in lower or "thanks for" in lower:
        return "intro"
    if "in summary" in lower or "takeaway" in lower or "wrap up" in lower:
        return "summary"
    if "question" in lower and "answer" in lower:
        return "qa"
    if "framework" in lower or "model" in lower:
        return "framework"
    if "story" in lower or "example" in lower:
        return "story"
    return "tactical"


def chunk_segments(segments, min_words: int, max_words: int):
    chunks = []
    current = []
    current_words = 0
    start_ts = None

    def flush():
        nonlocal current, current_words, start_ts
        if not current:
            return
        text = " ".join(seg["text"] for seg in current).strip()
        chunks.append(
            {
                "timestamp_start": start_ts,
                "timestamp_end": current[-1].get("timestamp"),
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
            flush()
        current.append(seg)
        current_words += words

    flush()
    return chunks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--min-words", type=int, default=500)
    parser.add_argument("--max-words", type=int, default=1500)
    args = parser.parse_args()

    text = Path(args.input).read_text(errors="ignore")
    segments = parse_markers(text)
    chunks = chunk_segments(segments, args.min_words, args.max_words)

    out_chunks = []
    for idx, chunk in enumerate(chunks):
        words = chunk["text"].split()
        topic_title = " ".join(words[:8]).strip() or "Topic"
        out_chunks.append(
            {
                "chunk_index": idx,
                "topic_title": topic_title,
                "topic_type": infer_topic_type(chunk["text"]),
                "key_concepts": [],
                "timestamp_start": chunk["timestamp_start"],
                "timestamp_end": chunk["timestamp_end"],
                "word_count": chunk["word_count"],
                "text": chunk["text"],
            }
        )

    Path(args.output).write_text(json.dumps({"chunks": out_chunks}, indent=2))


if __name__ == "__main__":
    main()
