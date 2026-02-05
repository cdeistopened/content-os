import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional

RX_WS = re.compile(r"\s+")


def slugify(value: str, max_len: int = 80) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:max_len] or "episode"


def iso_date(value: str) -> Optional[str]:
    if not value:
        return None
    value = value.strip()
    for fmt in ("%Y-%m-%d", "%Y%m%d", "%a, %d %b %Y %H:%M:%S %z"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def yaml_escape(value: Optional[str]) -> str:
    if value is None:
        return "null"
    value = str(value)
    if value == "":
        return '""'
    if any(ch in value for ch in [":", "#", "\n", "\r", "\t", "\""]):
        return json.dumps(value)
    if value.strip() != value:
        return json.dumps(value)
    return value


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run(cmd: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def load_manifest(path: Path) -> List[dict]:
    if not path.exists():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entries.append(json.loads(line))
    return entries


def write_manifest(path: Path, entries: Iterable[dict]) -> None:
    lines = [json.dumps(e, ensure_ascii=False) for e in entries]
    write_text(path, "\n".join(lines) + "\n")


def parse_timestamp_seconds(ts: str) -> float:
    parts = ts.replace(",", ".").split(":")
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    if len(parts) == 2:
        m, s = parts
        return int(m) * 60 + float(s)
    return 0.0


def format_timestamp_marker(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"[{h}:{m:02d}:{s:02d}]"
    return f"[{m}:{s:02d}]"


def overlap_len(a: str, b: str, min_overlap: int = 4, max_overlap: int = 80) -> int:
    max_k = min(len(a), len(b), max_overlap)
    for k in range(max_k, min_overlap - 1, -1):
        if a[-k:] == b[:k]:
            return k
    return 0


def parse_vtt_cues(path: Path) -> List[dict]:
    cues = []
    lines = path.read_text(errors="ignore").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("WEBVTT"):
            i += 1
            continue
        if re.match(r"^\d+$", line):
            i += 1
            continue
        if "-->" in line:
            start, end = [p.strip() for p in line.split("-->")[:2]]
            end = end.split()[0]
            i += 1
            text_lines = []
            while i < len(lines) and lines[i].strip():
                text_lines.append(lines[i].strip())
                i += 1
            text = " ".join(text_lines)
            text = re.sub(r"<[^>]+>", "", text)
            text = RX_WS.sub(" ", text).strip()
            if text:
                cues.append({"start": start, "end": end, "text": text})
            continue
        i += 1
    return cues


def parse_srt_cues(path: Path) -> List[dict]:
    cues = []
    lines = path.read_text(errors="ignore").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if re.match(r"^\d+$", line):
            i += 1
            continue
        if "-->" in line:
            start, end = [p.strip() for p in line.split("-->")[:2]]
            end = end.split()[0]
            i += 1
            text_lines = []
            while i < len(lines) and lines[i].strip():
                text_lines.append(lines[i].strip())
                i += 1
            text = " ".join(text_lines)
            text = re.sub(r"<[^>]+>", "", text)
            text = RX_WS.sub(" ", text).strip()
            if text:
                cues.append({"start": start, "end": end, "text": text})
            continue
        i += 1
    return cues


def merge_cues_with_timestamps(cues: List[dict], interval_sec: int = 60) -> str:
    if not cues:
        return ""

    output_parts: List[str] = []
    last_marker_time = -interval_sec
    current_text = ""

    for cue in cues:
        text = cue.get("text", "").strip()
        start = parse_timestamp_seconds(cue.get("start", "0:00"))
        if not text:
            continue

        if start - last_marker_time >= interval_sec:
            if current_text:
                output_parts.append(current_text)
                current_text = ""
            marker = format_timestamp_marker(start)
            output_parts.append(f"\n{marker}\n")
            last_marker_time = start

        if not current_text:
            current_text = text
            continue
        if text == current_text or text in current_text:
            continue
        if current_text in text:
            current_text = text
            continue
        overlap = overlap_len(current_text, text)
        if overlap:
            current_text = current_text + text[overlap:]
            continue
        output_parts.append(current_text)
        current_text = text

    if current_text:
        output_parts.append(current_text)

    return "\n".join(output_parts).strip() + "\n"


def build_frontmatter(**fields: Optional[str]) -> str:
    lines = ["---"]
    for key, value in fields.items():
        lines.append(f"{key}: {yaml_escape(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"
