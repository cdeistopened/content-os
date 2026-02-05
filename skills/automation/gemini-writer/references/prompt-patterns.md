# Gemini Prompt Patterns

Effective prompts for delegating context-heavy tasks to Gemini 3 Flash.

## Analysis Patterns

### Codebase Analysis

```
Analyze this codebase and provide:
1. Architecture overview (main components and their relationships)
2. Key patterns used (state management, routing, data fetching)
3. Potential issues or anti-patterns
4. Dependencies and their purposes

Structure your response with clear headings. Be specific with file paths.
```

### Document Synthesis

```
Synthesize these documents into a comprehensive summary:

1. Main themes across all sources
2. Key facts and data points (with source attribution)
3. Areas of agreement
4. Contradictions or tensions
5. Gaps or questions that remain unanswered

Output format: Markdown with citations like [Source: filename.md]
```

### Pattern Detection

```
Search for patterns in this codebase:
1. All API endpoints (method, path, handler)
2. Database queries and their locations
3. Error handling patterns
4. Authentication/authorization checks

Return as structured JSON with file paths and line numbers.
```

## Transform Patterns

### Bulk Document Conversion

```
Convert each source document into [target format].

Requirements:
- Maintain the original meaning and tone
- Apply consistent formatting
- Include source attribution in metadata
- Output one file per source document

Naming convention: [original_name]_converted.md
```

### Content Extraction

```
Extract all substantive content about [topic] from these sources.

For each relevant passage:
1. Full quote (preserve original wording)
2. Source file and context
3. Theme or category
4. Relevance score (1-5)

Organize by theme. Include 10,000+ words of quoted material.
```

### Research Compilation

```
Compile a research document from these sources:

Structure:
1. Executive Summary (500 words)
2. Key Findings (bullet points with citations)
3. Detailed Analysis (organized by theme)
4. Methodology Notes
5. Source Bibliography

Word count target: 5,000-8,000 words
Citation format: [Author, Source, Page/Section]
```

## Agent Mode Patterns

### Book Outline Creation

```
Create a detailed book outline from these source materials.

For each chapter:
1. Chapter title
2. Core argument (2-3 sentences)
3. Source files that inform this chapter
4. 5-10 key quotes with full attribution
5. How quotes build the argument

Total output: 8,000+ words
Use write_file for each chapter outline separately.
```

### Long-Form Writing

```
Write [chapter/article/report] based on the provided sources.

Requirements:
- Word count: [X,000]-[Y,000] words
- Use extensive quotes from sources
- Maintain [voice/style] throughout
- Include smooth transitions
- End with [conclusion type]

Quote format:
> "Quote text here."
> - Source: filename.md

Use write_file to save incrementally (every 2,000 words).
```

### Multi-File Project

```
Create a complete [project type] from these sources.

Output structure:
project_name/
  README.md (overview)
  01_[section].md
  02_[section].md
  ...
  appendix.md (sources and references)

Create each file fully before moving to the next.
Use write_file for each file.
Call task_complete with summary when done.
```

## Output Format Specifications

### Structured JSON

```
Return analysis as JSON:
{
  "summary": "...",
  "findings": [
    {"category": "...", "items": [...], "severity": "..."}
  ],
  "recommendations": [...],
  "sources_analyzed": [...]
}
```

### Markdown Report

```
Format as Markdown with:
- H1 for main title
- H2 for major sections
- H3 for subsections
- Bullet points for lists
- Code blocks for code/data
- > for quotes
- Tables where appropriate
```

### File Markers (Transform Mode)

```
For each output file, use:

<<<FILE: path/to/file.ext>>>
[file content]
<<<END FILE>>>

Multiple files in single response are supported.
```

## Word Count Guidelines

| Content Type | Target Words |
|--------------|--------------|
| Summary | 300-500 |
| Article | 1,500-3,000 |
| Chapter | 3,000-5,000 |
| Deep Analysis | 5,000-8,000 |
| Full Report | 8,000-15,000 |
| Book Outline | 10,000+ |

Always specify word counts in prompts to prevent thin output.

## Quality Markers

Include these in prompts for better output:

- "Be thorough - don't abbreviate"
- "Include specific examples"
- "Quote extensively from sources"
- "Cite sources for all claims"
- "Write complete sentences, not bullet points"
- "Include actionable recommendations"
- "Acknowledge limitations or gaps"
