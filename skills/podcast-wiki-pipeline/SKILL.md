---
name: podcast-wiki-pipeline
version: 1.0.0
description: "When the user wants to run an end-to-end pipeline to ingest podcast or YouTube feeds into transcripts, chunks, ontology, and wiki scaffolds. Also use for manifest-driven batch processing of audio/video content. For wiki ontology design, see wiki-ontology-design."
---

# Podcast Wiki Pipeline

Use this skill to run a repeatable pipeline on a podcast or YouTube feed.

## Quick start
```bash
python3 scripts/run_pipeline.py --feed-url "https://example.com/feed.xml" --slug "my-podcast"
```

This writes output to `wiki-projects/projects/<slug>/`.

## What this skill includes
- A manifest-first pipeline with checkpoints.
- Overlap-aware VTT cleanup and timestamp markers.
- Standardized transcript frontmatter.
- Chunking into 500-1500 word segments.
- Ontology proposal with approval gates.
- Wiki scaffold generation (domains/frameworks/cases/people/episodes).

## Approval gates (built into the scripts)
1. **Source selection**: confirm discovered transcript sources before ingest.
2. **Transcript quality**: inspect a small sample and approve.
3. **Ontology**: approve a high-level domain map before scaffolding.

## Data layout (per project)
```
projects/<slug>/
├── config.json
├── data/
│   ├── manifest.jsonl
│   ├── transcripts/
│   │   ├── raw/
│   │   └── polished/
│   ├── vtt/
│   ├── cues/
│   ├── chunks/
│   └── extracted/
└── wiki/
    ├── ontology/
    └── content/
        ├── domains/
        ├── frameworks/
        ├── cases/
        ├── people/
        └── episodes/
```

## Scripts
- `scripts/run_pipeline.py` — Orchestrates the workflow with approval gates.
- `scripts/discover_sources.py` — Parses RSS/YouTube links and builds manifest.
- `scripts/fetch_transcripts.py` — Downloads transcript sources and builds markdown.
- `scripts/chunk_transcripts.py` — Splits transcripts into semantic chunks.
- `scripts/propose_ontology.py` — Generates a high-level ontology proposal.
- `scripts/generate_wiki_scaffold.py` — Builds wiki stub pages from approved ontology.

## Audio-only feeds (optional STT)
If transcripts are missing and you want local STT:

```bash
python3 scripts/fetch_transcripts.py \
  --project-root projects/<slug> \
  --stt-command "whisper --model small --language en --output_format txt --output_dir {output} {audio}"
```

Replace the command with your preferred speech-to-text tool.

## References (kept inside this skill)
- `references/field-notes.md`
- `references/frontmatter.md`
- `references/ontology-blur-to-focus.md`
- `references/manifest-schema.md`

## Related Skills

- **Upstream**: **transcript-polisher**, **multi-source-research**, **wiki-ontology-design**
- **Enhanced by**: **semantic-chunking-rules**, **local-markdown-search**
