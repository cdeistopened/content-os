# PDF OCR Skill

Agentic PDF-to-Markdown conversion using Gemini 3 Flash Preview.

## When to Use

- Converting scanned books/documents to editable text
- Processing PDFs too large for single API calls
- Latin/scholarly text OCR with diacritical preservation
- Documents needing structure detection (chapters, footnotes, columns)

## Quick Reference

```bash
# Pre-flight (first 20 pages)
python src/ocr_pipeline.py document.pdf

# Full document
python src/ocr_pipeline.py document.pdf --full

# Custom chunk size
python src/ocr_pipeline.py document.pdf --full --chunk-size 8
```

## Agentic Workflow

### 1. Pre-Flight Analysis

Always start with a sample to understand the document:

```bash
python src/ocr_pipeline.py document.pdf --pages 20
```

This produces:
- `{name}_sample.md` - OCR output
- `{name}_analysis.json` - Document structure

**Review analysis for:**
- Language detection (triggers specialized prompts)
- Two-column detection (affects chunk sizing)
- Footnote detection (affects output format)
- Recommended chunk size

### 2. Full Processing

After validating sample quality:

```bash
python src/ocr_pipeline.py document.pdf --full
```

**Monitor progress via:**
- Console output (chunk-by-chunk)
- `{name}_progress.json` (JSON status)

### 3. Quality Review

Check final output for:
- Truncation markers (`...` at chunk ends)
- Missing footnote definitions
- Unbalanced markdown (bold/italic)
- Chapter/section continuity

## Key Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| `--pages` | 20 | Sample size for pre-flight |
| `--full` | false | Process entire document |
| `--chunk-size` | auto | Pages per API call (dense text: 10-12) |
| `--output` | ./output | Output directory |

## Document Types

### Latin/Scholarly
- Automatically detected via language analysis
- Uses specialized LATIN_OCR_PROMPT
- Restores diacriticals: æ, œ
- Chapter structure: CAP. I → ## CAP. I
- Column markers: `<!-- col. 1125 -->`

### General Documents
- Standard Markdown formatting
- Tables, lists, blockquotes preserved
- Page numbers/headers stripped

## Token Limits

**Gemini 3 Flash Preview:**
- Output: 64K tokens (~45-50K chars)
- Dense text yields ~5-6K chars/page
- Safe chunk size: 10-12 pages for dense text

## Error Recovery

Progress saved after each chunk. If processing fails:
1. Check `{name}_progress.json` for last successful chunk
2. Manual intervention needed (future: auto-resume)

## File Locations

```
Creative Intelligence Agency/ocr-tool/
├── src/ocr_pipeline.py    # Main script
├── output/                # Generated files
├── ARCHITECTURE.md        # Full technical docs
├── LEARNING_LOG.md        # Test results and issues
└── .env                   # API key
```

## Model

Always use `gemini-3-flash-preview` for OCR tasks:
- 1M token input (large PDFs ok)
- 64K token output
- Native PDF support
- Best quality/speed ratio for OCR

## Example Session

```
# 1. Analyze document
python src/ocr_pipeline.py book.pdf --pages 20
→ Review sample.md and analysis.json

# 2. If sample looks good, process full document
python src/ocr_pipeline.py book.pdf --full
→ Monitor progress.json

# 3. Review output
→ Check for truncation, quality issues
→ Log findings to LEARNING_LOG.md
```

---

*See ARCHITECTURE.md for full technical documentation.*
