# Book from Sources

Write books from transcripts, interviews, notes, or other source material.

## When to Use

- Converting podcast transcripts into a book
- Writing a book from interview material
- Compiling research notes into chapters
- Creating a book from lecture transcripts
- Any "book from raw material" project

## Workflow

### Phase 1: Prepare Sources

Organize source material in a directory:
```
sources/
├── transcript_01.md
├── transcript_02.md
├── notes.md
└── ...
```

Each file should have clear attribution (speaker name, date, context).

### Phase 2: Create Outline

```bash
python gemini_delegate.py \
  --sources ./sources \
  --output ./book-project \
  --mode agent \
  --prompt "Create a detailed book outline from these sources.

For each chapter:
1. Chapter title
2. Core argument (2-3 sentences)
3. Source files that feed into this chapter
4. 5-10 key quotes (full paragraphs, not snippets) with source attribution
5. How the quotes build the argument

Write 8,000+ words total. This is the foundation for the book."
```

### Phase 3: Write Chapters

Run one chapter at a time, including the outline in context:

```bash
python gemini_delegate.py \
  --sources ./sources \
  --output ./book-project \
  --mode agent \
  --prompt "Write Chapter 3: [Title]

Using the transcripts provided, write a complete 5,000-7,000 word chapter.

Structure:
- Opening hook that draws readers in
- Build the argument through extensive quotes from sources
- Editorial bridges between quotes (your framing)
- End with transition to next chapter

Quote format:
> 'Quote text here.'
> - Source: filename.md

Preserve the speaker's voice. This is them speaking, with your editorial framing.
Include at least 15 substantial quotes (100-500 words each)."
```

### Phase 4: Polish

Run an editorial pass for consistency:

```bash
python gemini_delegate.py \
  --sources ./book-project \
  --output ./book-final \
  --mode agent \
  --prompt "Review these chapter drafts for:
1. Consistency of voice and tone
2. Smooth transitions between chapters
3. Any gaps or redundancies
4. Overall narrative arc

Create revised versions with tracked changes noted."
```

## Prompt Template: Full Outline

```
Create a detailed book outline from these [TYPE] about [TOPIC].

The book should:
- [Core thesis/argument]
- Target audience: [who]
- Tone: [conversational/academic/etc.]

For each chapter:
1. Chapter title (compelling, not generic)
2. Core argument in 2-3 sentences
3. List source files that inform this chapter
4. Include 5-10 key quotes per chapter:
   - Full paragraphs (100-500 words), not snippets
   - Exact source attribution
   - Brief note on how quote supports the argument
5. Chapter transition/connection to next

Target: 8,000-12,000 words total for the outline.
Use write_file for each chapter outline as a separate file.
```

## Prompt Template: Single Chapter

```
Write [CHAPTER TITLE] based on the provided sources.

This chapter argues: [thesis]
Previous chapter ended with: [transition point]
Next chapter will cover: [preview]

Requirements:
- Word count: 5,000-7,000 words
- Include 15-20 substantial quotes from sources
- Maintain [SPEAKER]'s voice in quotes
- Your editorial framing connects the quotes
- Opening hook, developed argument, strong close

Quote format:
> "[Quote text - full paragraph]"
> - [Speaker Name], Source: [filename]

Structure:
1. Opening hook (500 words)
2. Main argument with quotes (4,000-5,000 words)
3. Synthesis and transition (500-1,000 words)

Write the complete chapter. Do not summarize or abbreviate.
```

## Key Principles

1. **Quote Extensively**: The sources are the substance. Use full paragraphs, not pull quotes.

2. **Preserve Voice**: When quoting interviews/transcripts, keep the speaker's authentic voice.

3. **Editorial Framing**: Your job is to structure and contextualize, not replace the source material.

4. **Word Count Matters**: Always specify target word counts. "Write a chapter" produces thin content.

5. **One Chapter at a Time**: Better results than trying to write the whole book at once.

## Word Count Guidelines

| Element | Target |
|---------|--------|
| Book outline | 8,000-12,000 words |
| Single chapter | 5,000-7,000 words |
| Chapter outline | 1,000-2,000 words |
| Quotes per chapter | 15-25 substantial quotes |

## Example: Ray Peat Book

```bash
python gemini_delegate.py \
  --sources ./ray-peat-transcripts \
  --output ./peat-book \
  --mode agent \
  --prompt "Create a book outline from these Ray Peat interview transcripts.

The book explores COVID, vaccines, and authoritarianism through Peat's biological lens.

For each of 8 chapters:
1. Compelling title
2. Core biological argument (2-3 sentences)
3. Which transcripts feed this chapter
4. 8-10 key quotes (full paragraphs with source)
5. How quotes build the argument

Write 10,000+ words. This is the foundation - be thorough."
```
