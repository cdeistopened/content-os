#!/usr/bin/env python3
import argparse
import json
import re
from collections import Counter
from pathlib import Path

STOPWORDS = {
    "the", "and", "for", "that", "with", "this", "from", "they", "their", "have",
    "was", "were", "you", "your", "but", "not", "are", "its", "about", "just",
    "what", "when", "then", "there", "into", "out", "our", "has", "had", "all",
    "she", "him", "her", "himself", "herself", "them", "these", "those", "over",
    "because", "like", "really", "very", "can", "could", "would", "should", "will",
}


def tokenize(text: str):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    for token in text.split():
        if len(token) < 3:
            continue
        if token in STOPWORDS:
            continue
        yield token


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--top", type=int, default=60)
    args = parser.parse_args()

    project_root = Path(args.project_root)
    chunks_dir = project_root / "data" / "chunks"
    ontology_dir = project_root / "wiki" / "ontology"
    ontology_dir.mkdir(parents=True, exist_ok=True)

    counter = Counter()
    for path in chunks_dir.glob("*.json"):
        payload = json.loads(path.read_text(errors="ignore"))
        for chunk in payload.get("chunks", []):
            counter.update(tokenize(chunk.get("text", "")))

    top_terms = [term for term, _ in counter.most_common(args.top)]

    print("Top terms:")
    print(", ".join(top_terms[:30]))
    domains_raw = input("Enter broad domains (comma-separated): ").strip()
    domains = [d.strip() for d in domains_raw.split(",") if d.strip()]

    proposal = {
        "domains": domains,
        "top_terms": top_terms,
        "notes": "Edit domains to match your mental map, then refine into subtopics.",
    }

    out_path = ontology_dir / "phase1_domains.json"
    out_path.write_text(json.dumps(proposal, indent=2))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
