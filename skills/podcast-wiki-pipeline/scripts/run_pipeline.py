#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from utils import run


def find_root(start: Path) -> Path:
    for parent in [start] + list(start.parents):
        if parent.name == "wiki-projects":
            return parent
    raise SystemExit("Could not locate wiki-projects root")


def confirm(prompt: str, auto_yes: bool) -> None:
    if auto_yes:
        return
    resp = input(f"{prompt} [y/N]: ").strip().lower()
    if resp not in ("y", "yes"):
        raise SystemExit("Aborted by user")


def run_step(cmd: list[str]) -> None:
    proc = run(cmd)
    if proc.returncode != 0:
        print(proc.stderr)
        raise SystemExit("Step failed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed-url", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--skip-chunk", action="store_true")
    parser.add_argument("--skip-ontology", action="store_true")
    args = parser.parse_args()

    root = find_root(Path(__file__).resolve())
    project_root = root / "projects" / args.slug
    project_root.mkdir(parents=True, exist_ok=True)

    config_path = project_root / "config.json"
    if not config_path.exists():
        config_path.write_text(json.dumps({"feed_url": args.feed_url}, indent=2))

    scripts_dir = Path(__file__).resolve().parent

    print("Discovering sources...")
    run_step(
        [
            sys.executable,
            str(scripts_dir / "discover_sources.py"),
            "--feed-url",
            args.feed_url,
            "--project-root",
            str(project_root),
        ]
    )

    report_path = project_root / "data" / "sources_report.json"
    if report_path.exists():
        report = json.loads(report_path.read_text(errors="ignore"))
        print(json.dumps(report, indent=2))

    confirm("Proceed with these sources", args.yes)

    print("Fetching transcripts...")
    run_step(
        [
            sys.executable,
            str(scripts_dir / "fetch_transcripts.py"),
            "--project-root",
            str(project_root),
            "--limit",
            str(args.limit),
        ]
    )

    sample_dir = project_root / "data" / "transcripts" / "raw"
    samples = list(sample_dir.glob("*.md"))[:3]
    if samples:
        print("Sample transcripts:")
        for sample in samples:
            print(f"- {sample}")

    confirm("Inspect sample transcripts and continue", args.yes)

    if not args.skip_chunk:
        print("Chunking transcripts...")
        run_step(
            [
                sys.executable,
                str(scripts_dir / "chunk_transcripts.py"),
                "--project-root",
                str(project_root),
            ]
        )

    if not args.skip_ontology:
        confirm("Proceed to ontology proposal", args.yes)
        print("Proposing ontology...")
        run_step(
            [
                sys.executable,
                str(scripts_dir / "propose_ontology.py"),
                "--project-root",
                str(project_root),
            ]
        )

    print("Next: review wiki/ontology/phase1_domains.json and write approved.json")


if __name__ == "__main__":
    main()
