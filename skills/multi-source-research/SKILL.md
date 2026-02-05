---
name: multi-source-research
version: 1.0.0
description: "When the user wants to build encyclopedia pages from multiple sources with quote weaving and source logging. Also use when synthesizing research from diverse source types into structured wiki content. For wiki structure, see wiki-ontology-design."
---

# Multi-Source Research

Use this skill to build encyclopedia pages from multiple source types.

## Workflow
1. Define 5-10 semantic queries for the entity.
2. Run RAG search against chunked data.
3. Run keyword grep across newsletters, articles, emails, transcripts.
4. Collect passages with file paths for citations.
5. Synthesize using the style rules in `references/style-guide.md`.

## Script
```bash
python3 scripts/search_pack.py --query "your topic" --root <corpus-root>
```

## References
- `references/search-protocol.md`
- `references/style-guide.md`

## Related Skills

- **Enhanced by**: **local-markdown-search**, **semantic-chunking-rules**
- **Feeds into**: **wiki-ontology-design**, **podcast-wiki-pipeline**
