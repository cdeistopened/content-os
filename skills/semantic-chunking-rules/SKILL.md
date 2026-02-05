---
name: semantic-chunking-rules
version: 1.0.0
description: "When the user wants to split transcripts into RAG-ready semantic chunks with timestamps. Also use when segmenting long documents for retrieval-augmented generation. For transcript cleanup, see transcript-polisher."
---

# Semantic Chunking Rules

Use this skill when splitting transcripts into RAG-ready chunks.

## Chunk targets
- Size: 500-1500 words (or tokens).
- Break at topic shifts and timestamp markers.
- Preserve episode metadata in each chunk.

## Output schema
See `references/chunk_schema.json`.

## Script
```bash
python3 scripts/semantic_chunker.py --input <transcript.md> --output <chunks.json>
```

## Heuristics
- Treat intro/outro and ads as separate chunks.
- Prefer clean boundaries over exact length.
- Keep timestamps on every chunk for citations.

## References
- `references/chunk_schema.json`
- `references/topic_types.md`

## Related Skills

- **Upstream**: **transcript-polisher**
- **Feeds into**: **local-markdown-search**, **podcast-wiki-pipeline**, **multi-source-research**
