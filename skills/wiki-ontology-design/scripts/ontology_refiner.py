#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


def parse_list(prompt: str):
    raw = input(prompt).strip()
    return [item.strip() for item in raw.split(",") if item.strip()]


def slugify(value: str, max_len: int = 80) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:max_len] or "topic"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    payload = json.loads(input_path.read_text(errors="ignore"))
    domains = payload.get("domains", [])

    refined_domains = []
    frameworks = []

    for domain in domains:
        title = domain if isinstance(domain, str) else domain.get("title")
        slug = slugify(title)
        subtopics = parse_list(f"Subtopics for {title} (comma-separated): ")
        refined_domains.append(
            {
                "slug": slug,
                "title": title,
                "frameworks": [slugify(s) for s in subtopics],
            }
        )

        for sub in subtopics:
            frameworks.append(
                {
                    "slug": slugify(sub),
                    "title": sub,
                    "domain": slug,
                    "aliases": [],
                    "cases": [],
                    "people": [],
                }
            )

    cases = []
    people = []
    case_list = parse_list("Optional cases (comma-separated, blank to skip): ")
    for case in case_list:
        cases.append(
            {
                "slug": slugify(case),
                "title": case,
                "illustrates": [],
                "people": [],
                "episodes": [],
            }
        )

    people_list = parse_list("Optional people (comma-separated, blank to skip): ")
    for person in people_list:
        people.append(
            {
                "slug": slugify(person),
                "title": person,
                "aliases": [],
            }
        )

    output = {
        "domains": refined_domains,
        "frameworks": frameworks,
        "cases": cases,
        "people": people,
    }

    Path(args.output).write_text(json.dumps(output, indent=2))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
