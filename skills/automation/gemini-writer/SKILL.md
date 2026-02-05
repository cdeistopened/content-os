---
name: gemini-writer
description: Delegate context-heavy tasks to Gemini 3 Flash's 1M token context window. This skill should be used when Claude's context is insufficient for large-scale reading, analysis, or synthesis tasks. Handles document analysis, codebase exploration, research synthesis, and long-form writing from extensive source material.
---

# Gemini Writer

Autonomous writing and analysis agent leveraging Gemini 3 Flash's 1M token context window.

## Credits

Based on [gemini-writer](https://github.com/Doriandarko/gemini-writer) by **Pietro Schirano** ([@Doriandarko](https://github.com/Doriandarko)).

Pietro's key insight: use Gemini's massive context window + tool use for autonomous long-form writing. The agent reads all your sources, then iteratively writes and saves files until the task is complete.

---

## When to Use This Skill

Delegate to Gemini when:
- Processing more content than fits in Claude's context
- Analyzing entire codebases or large document sets
- Writing from extensive source material (transcripts, research, notes)
- Synthesizing research from many sources
- Any task where "I need to read all of X" and X is huge

**Triggers:**
- "Analyze all files in this directory"
- "Write a book from these transcripts"
- "Summarize these 50 documents"
- "Find patterns across this entire codebase"

**Not for:** Simple tasks, small files, or anything that fits comfortably in Claude's context.

---

## Critical: Model Configuration

**ALWAYS use `gemini-3-flash-preview`** - This is the correct model name.

```python
MODEL_NAME = "gemini-3-flash-preview"  # Correct
# NOT "gemini-2.5-flash" or other variants
```

Docs: https://ai.google.dev/gemini-api/docs/models#gemini-3-flash

---

## Operation Modes

### Mode 1: Analyze (Read-Only)

Gemini reads sources and returns analysis to stdout. No files created.

```bash
python scripts/gemini_delegate.py \
  --sources ./large-codebase \
  --prompt "Identify all API endpoints and their purposes" \
  --mode analyze
```

Use for: Code analysis, document summarization, pattern detection, research synthesis.

### Mode 2: Transform (Read + Write)

Gemini reads sources and writes transformed outputs using file markers.

```bash
python scripts/gemini_delegate.py \
  --sources ./transcripts \
  --output ./processed \
  --prompt "Convert each transcript into a polished article" \
  --mode transform
```

Use for: Bulk document conversion, content generation, structured extraction.

### Mode 3: Agent (Autonomous)

Full agentic loop with tool access. Best for complex multi-step tasks.

```bash
python scripts/gemini_delegate.py \
  --sources ./research-materials \
  --output ./book-project \
  --prompt "Write a book outline with chapter summaries and key quotes" \
  --mode agent
```

Use for: Book writing, complex multi-file projects, iterative refinement.

---

## Script Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--sources`, `-s` | Yes | Path to source file or directory |
| `--output`, `-o` | No | Output directory (default: ./output) |
| `--prompt`, `-p` | Yes | Task description for Gemini |
| `--mode`, `-m` | No | `analyze`, `transform`, or `agent` (default: analyze) |
| `--recover`, `-r` | No | Path to context summary for recovery |
| `--max-tokens` | No | Max output tokens (default: 8192) |
| `--extensions` | No | File extensions to include (e.g., .py .md) |

---

## Task-Specific References

See `references/` for optimized workflows:

| Reference | Use Case |
|-----------|----------|
| `prompt-patterns.md` | General prompt templates |
| `book-from-sources.md` | Writing books from transcripts/notes |
| `encyclopedia-article.md` | Creating encyclopedia/wiki entries |
| `research-synthesis.md` | Compiling research reports |

---

## Prompt Engineering Tips

### Be Specific About Output Format

```
Bad:  "Summarize these documents"
Good: "Create a structured summary with:
       1. Key themes (bullet points)
       2. Notable quotes (with source attribution)
       3. Contradictions or tensions between sources
       Output as markdown with clear headings."
```

### Request Word Counts for Writing Tasks

```
"Write a 5,000-7,000 word chapter..."
"Provide at least 10 key quotes per section..."
"Create a comprehensive 3,000+ word analysis..."
```

### Include Context About Purpose

```
"This analysis will be used for [purpose].
 The audience is [audience].
 Focus on [specific aspects]."
```

---

## Token Management

- **Context window**: 1,000,000 tokens
- **Compression threshold**: 900,000 tokens (90%)
- **Rough estimate**: ~4 characters per token

The script automatically:
1. Counts tokens before each API call
2. Warns when approaching limits
3. Saves recovery summaries for interrupted sessions

---

## Recovery Mode

If a session is interrupted, recover using the saved context:

```bash
python scripts/gemini_delegate.py \
  --recover ./output/.context_summary_20250107_143022.md \
  --mode agent
```

The script saves context summaries:
- Every 50 iterations (auto-backup)
- On keyboard interrupt (Ctrl+C)

---

## Environment Setup

Requires `GEMINI_API_KEY`:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or create `.env` file in scripts directory.

Install dependencies:

```bash
pip install google-genai python-dotenv
```

---

## Cost Awareness

Gemini 3 Flash pricing (approximate):
- Input: ~$0.075 per 1M tokens
- Output: ~$0.30 per 1M tokens

A typical large analysis (500k input, 10k output): **~$0.04**

The script reports token usage after each run.

---

## Architecture

```
gemini-writer/
├── SKILL.md                  # This file
├── scripts/
│   ├── gemini_delegate.py    # Main entry point
│   └── tools/                # Tool implementations
│       ├── writer.py         # File writing
│       ├── project.py        # Project management
│       └── compression.py    # Context compression
└── references/               # Task-specific workflows
    ├── prompt-patterns.md
    ├── book-from-sources.md
    ├── encyclopedia-article.md
    └── research-synthesis.md
```

---

## Integration with Claude

### Handoff Pattern

1. Claude identifies task exceeding context
2. Claude prepares sources and crafts prompt
3. Claude invokes gemini_delegate.py
4. Gemini processes and outputs results
5. Claude reads results and continues work

### Example

```bash
# Claude runs this when sources are too large
python ~/.claude/skills/gemini-writer/scripts/gemini_delegate.py \
  --sources ~/project/transcripts \
  --output ~/project/output \
  --prompt "Create a detailed book outline with chapter summaries" \
  --mode agent
```

---

*Based on [gemini-writer](https://github.com/Doriandarko/gemini-writer) by Pietro Schirano. Gemini 3 Flash: 1M tokens of context for the heavy lifting.*
