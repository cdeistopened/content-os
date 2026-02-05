# Vellum Prep

Convert markdown manuscripts to Vellum-ready Word documents.

## When to Use

Use this skill when you have a markdown manuscript (from OCR, writing, or conversion) that needs to be formatted for import into Vellum book formatting software.

## What It Does

**Programmatic cleanup (no AI tokens):**
- Removes OCR metadata headers
- Converts `---` to `***` (Vellum ornamental breaks)
- Removes duplicate running headers (e.g., repeated book title)
- Removes `[Image: ...]` placeholder descriptions
- Strips publisher front matter (catalogs, copyright boilerplate)
- Normalizes chapter headings to `# Chapter X: Title` format
- Cleans common artifacts (page numbers, ellipses, broken hyphenation)
- Converts to .docx via pandoc

## Usage

```bash
# From the manuscript directory:
python3 /path/to/vellum_prep.py manuscript.md

# Output: manuscript_vellum.md + manuscript.docx (if pandoc available)
```

Or invoke via Claude:
```
/vellum-prep manuscript.md
```

## Vellum Formatting Rules

| Markdown | Word Style | Vellum Element |
|----------|-----------|----------------|
| `# Chapter 1: Title` | Heading 1 | Chapter |
| `# Dedication` | Heading 1 | Dedication |
| `# Prologue` | Heading 1 | Prologue |
| `## Section` | Heading 2 | Level 1 Subhead |
| `***` | Centered asterisks | Ornamental Break |
| Single blank line | Blank paragraph | Scene Break |

## Configuration

Edit the script to customize:
- `header_patterns`: List of regex patterns for headers to remove
- `remove_images`: Whether to strip `[Image: ...]` tags
- `clean_for_vellum`: Apply Vellum-specific formatting

## Requirements

- Python 3.x
- pandoc (for .docx conversion)

## Handling Complex Manuscripts

For manuscripts with special requirements (Notion exports, external images, nested chapters), create a **book-specific preprocessing script**. See `Personal/Guide Abrege/prep_guide_abrege.py` for an example that handles:

### Notion Export Issues
- **Missing image folders**: Notion exports reference `FolderName/image.png` but don't always include the folder
- **Substack CDN images**: Can be downloaded with curl and remapped to local paths
- **Image mapping pattern**:
  ```python
  IMAGE_MAP = {
      "substack-uuid_dimensions.png": "images/01-descriptive-name.png",
  }
  ```

### Nested Chapter Headings
When a document has nested "CHAPTER I/II/III" within sections (e.g., each movement family has its own Chapter I, II, III):
- Keep top-level sections as `#` (Vellum chapters)
- Demote internal "CHAPTER X:" labels to `##` subheadings
- Strip the "CHAPTER X:" prefix, keep just the descriptive title

### Tables
- Multi-line cells in markdown tables **don't convert well** via pandoc - convert to numbered lists instead
- See `prep_guide_abrege.py` for regex pattern to match and replace specific tables

### Bold Labels as Headings
Instructional books often use `**FIRST TYPE:**` or `**Method A:**` as implicit subheadings. Convert these to actual headings (`####`) for proper Vellum hierarchy.

### Workflow for Complex Books
1. Run exploratory agent to analyze structure
2. Create book-specific prep script
3. Download/remap external images
4. Run prep script → intermediate `.md`
5. Run `pandoc` directly (not vellum_prep.py) to preserve images
6. Review in Vellum, fix Parts/special elements manually

## Files

- `SKILL.md` - This file
- `vellum_prep.py` - Main conversion script (OCR cleanup focus)
