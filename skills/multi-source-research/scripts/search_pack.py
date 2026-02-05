#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--max-results", type=int, default=50)
    args = parser.parse_args()

    query = args.query.lower()
    root = Path(args.root)
    results = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in (".md", ".txt", ".json"):
            continue
        try:
            text = path.read_text(errors="ignore")
        except Exception:
            continue
        if query in text.lower():
            idx = text.lower().index(query)
            start = max(0, idx - 120)
            end = min(len(text), idx + 120)
            snippet = text[start:end].replace("\n", " ")
            results.append({"path": str(path), "snippet": snippet})
            if len(results) >= args.max_results:
                break

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
