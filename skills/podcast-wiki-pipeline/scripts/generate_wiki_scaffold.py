#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from utils import build_frontmatter, load_manifest, write_text, slugify


def write_stub(path: Path, frontmatter: str, title: str) -> None:
    content = frontmatter + f"# {title}\n\n"
    write_text(path, content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()

    project_root = Path(args.project_root)
    ontology_path = project_root / "wiki" / "ontology" / "approved.json"
    if not ontology_path.exists():
        raise SystemExit("Missing approved ontology: wiki/ontology/approved.json")

    ontology = json.loads(ontology_path.read_text(errors="ignore"))

    content_dir = project_root / "wiki" / "content"
    domains_dir = content_dir / "domains"
    frameworks_dir = content_dir / "frameworks"
    cases_dir = content_dir / "cases"
    people_dir = content_dir / "people"
    episodes_dir = content_dir / "episodes"

    for d in (domains_dir, frameworks_dir, cases_dir, people_dir, episodes_dir):
        d.mkdir(parents=True, exist_ok=True)

    for domain in ontology.get("domains", []):
        slug = domain.get("slug") or slugify(domain.get("title", "domain"))
        frontmatter = build_frontmatter(
            type="domain",
            title=domain.get("title"),
            frameworks=domain.get("frameworks") or [],
        )
        write_stub(domains_dir / f"{slug}.md", frontmatter, domain.get("title", slug))

    for framework in ontology.get("frameworks", []):
        slug = framework.get("slug") or slugify(framework.get("title", "framework"))
        frontmatter = build_frontmatter(
            type="framework",
            title=framework.get("title"),
            domain=framework.get("domain"),
            aliases=framework.get("aliases") or [],
            cases=framework.get("cases") or [],
            people=framework.get("people") or [],
        )
        write_stub(frameworks_dir / f"{slug}.md", frontmatter, framework.get("title", slug))

    for case in ontology.get("cases", []):
        slug = case.get("slug") or slugify(case.get("title", "case"))
        frontmatter = build_frontmatter(
            type="case",
            title=case.get("title"),
            illustrates=case.get("illustrates") or [],
            people=case.get("people") or [],
            episodes=case.get("episodes") or [],
        )
        write_stub(cases_dir / f"{slug}.md", frontmatter, case.get("title", slug))

    for person in ontology.get("people", []):
        slug = person.get("slug") or slugify(person.get("title", "person"))
        frontmatter = build_frontmatter(
            type="person",
            title=person.get("title"),
            aliases=person.get("aliases") or [],
        )
        write_stub(people_dir / f"{slug}.md", frontmatter, person.get("title", slug))

    manifest = load_manifest(project_root / "data" / "manifest.jsonl")
    for entry in manifest:
        title = entry.get("title") or "Episode"
        slug = slugify(f"{entry.get('date')}-{title}")
        frontmatter = build_frontmatter(
            type="episode",
            title=title,
            date=entry.get("date"),
            source_url=entry.get("link"),
            audio_url=entry.get("audio_url"),
            video_id=entry.get("video_id"),
        )
        write_stub(episodes_dir / f"{slug}.md", frontmatter, title)

    print(f"Scaffold written to {content_dir}")


if __name__ == "__main__":
    main()
