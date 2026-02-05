#!/usr/bin/env python3
import argparse
import json
import re
import shlex
import tempfile
import urllib.request
from pathlib import Path

from utils import (
    build_frontmatter,
    load_manifest,
    merge_cues_with_timestamps,
    parse_srt_cues,
    parse_vtt_cues,
    run,
    slugify,
    write_manifest,
    write_text,
)

RX_AUDIO_EXT = re.compile(r"\.(mp3|m4a|aac|wav|flac)(\?|$)", re.I)


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as resp:
        dest.write_bytes(resp.read())


def infer_text_from_transcript(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".vtt":
        cues = parse_vtt_cues(path)
        return merge_cues_with_timestamps(cues)
    if ext == ".srt":
        cues = parse_srt_cues(path)
        return merge_cues_with_timestamps(cues)
    return path.read_text(errors="ignore")


def find_vtt_in_dir(directory: Path) -> Path | None:
    for path in directory.glob("*.vtt"):
        return path
    return None


def render_transcript(frontmatter: str, content: str) -> str:
    content = content.strip()
    return frontmatter + (content + "\n" if content else "")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--marker-interval", type=int, default=60)
    parser.add_argument("--stt-command", default="")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    project_root = Path(args.project_root)
    data_dir = project_root / "data"
    manifest_path = data_dir / "manifest.jsonl"

    raw_dir = data_dir / "transcripts" / "raw"
    vtt_dir = data_dir / "vtt"
    cues_dir = data_dir / "cues"

    entries = load_manifest(manifest_path)
    processed = 0

    for entry in entries:
        if processed >= args.limit:
            break
        status = entry.get("status")
        if status not in ("pending", "needs_stt") and not args.force:
            continue

        title = entry.get("title") or "Untitled"
        date = entry.get("date") or ""
        slug_base = f"{date}-{slugify(title)}".strip("-")
        slug = slug_base or slugify(title)

        transcript_path = raw_dir / f"{slug}.md"
        if transcript_path.exists() and not args.force:
            entry["status"] = "done"
            entry["transcript_path"] = str(transcript_path)
            continue

        transcript_source = None
        content = ""

        transcript_url = entry.get("transcript_url")
        youtube_url = entry.get("youtube_url")
        audio_url = entry.get("audio_url")

        if transcript_url:
            ext = Path(transcript_url.split("?")[0]).suffix or ".txt"
            temp_path = vtt_dir / f"{entry.get('id')}{ext}"
            download(transcript_url, temp_path)
            content = infer_text_from_transcript(temp_path)
            transcript_source = "rss_transcript"
        elif youtube_url:
            vtt_dir.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory() as tmp:
                tmp_dir = Path(tmp)
                cmd = [
                    "yt-dlp",
                    "--skip-download",
                    "--write-auto-subs",
                    "--write-subs",
                    "--sub-format",
                    "vtt",
                    "--sub-langs",
                    "en",
                    "-o",
                    str(tmp_dir / "%(id)s.%(ext)s"),
                    youtube_url,
                ]
                proc = run(cmd)
                if proc.returncode != 0:
                    entry.setdefault("notes", []).append(
                        proc.stderr.strip() or "yt-dlp failed"
                    )
                vtt_path = find_vtt_in_dir(tmp_dir)
                if vtt_path and vtt_path.exists():
                    target_vtt = vtt_dir / f"{entry.get('id')}.vtt"
                    target_vtt.write_bytes(vtt_path.read_bytes())
                    cues = parse_vtt_cues(target_vtt)
                    write_text(
                        cues_dir / f"{entry.get('id')}.json", json.dumps(cues, indent=2)
                    )
                    content = merge_cues_with_timestamps(
                        cues, interval_sec=args.marker_interval
                    )
                    transcript_source = "youtube_vtt"
        elif audio_url and args.stt_command:
            with tempfile.TemporaryDirectory() as tmp:
                tmp_dir = Path(tmp)
                audio_name = Path(audio_url.split("?")[0]).name
                if not RX_AUDIO_EXT.search(audio_name):
                    audio_name = "audio.bin"
                audio_path = tmp_dir / audio_name
                download(audio_url, audio_path)
                output_path = tmp_dir / "transcript.txt"
                cmd = args.stt_command.format(
                    audio=str(audio_path), output=str(output_path)
                )
                proc = run(shlex.split(cmd))
                if proc.returncode == 0 and output_path.exists():
                    content = output_path.read_text(errors="ignore")
                    transcript_source = "audio_stt"
                else:
                    entry.setdefault("notes", []).append("stt-command failed")
        else:
            entry["status"] = "needs_stt"
            continue

        if not content:
            entry.setdefault("notes", []).append("no transcript content")
            entry["status"] = "needs_stt"
            continue

        frontmatter = build_frontmatter(
            type="episode",
            show=entry.get("show") or entry.get("show_title") or "",
            title=title,
            date=entry.get("date") or "",
            source_url=entry.get("link") or "",
            audio_url=entry.get("audio_url") or "",
            transcript_source=transcript_source,
            transcript_quality="raw",
            video_id=entry.get("video_id") or "",
        )
        transcript_text = render_transcript(frontmatter, content)
        write_text(transcript_path, transcript_text)

        entry["status"] = "done"
        entry["transcript_path"] = str(transcript_path)
        entry["transcript_source"] = transcript_source
        processed += 1

    write_manifest(manifest_path, entries)
    print(f"Processed {processed} entries")


if __name__ == "__main__":
    main()
