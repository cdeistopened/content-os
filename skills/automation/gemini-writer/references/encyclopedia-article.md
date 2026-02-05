# Encyclopedia Article

Create comprehensive encyclopedia or wiki-style entries from source material.

## When to Use

- Building a knowledge base from research
- Creating wiki entries from corpus material
- Writing definitive reference articles
- Compiling biographical entries
- Any "comprehensive reference" project

## Characteristics

Encyclopedia articles differ from books:
- **Neutral tone**: Informative, not argumentative
- **Comprehensive**: Cover all aspects of the topic
- **Well-structured**: Clear sections, easy to navigate
- **Cited**: Every claim attributed to sources
- **Cross-referenced**: Links to related topics

## Workflow

### Phase 1: Extract Key Topics

```bash
python gemini_delegate.py \
  --sources ./corpus \
  --mode analyze \
  --prompt "Identify all distinct topics that could become encyclopedia entries.

For each topic, note:
1. Topic name
2. Source files that discuss it
3. Estimated depth (stub/article/comprehensive)
4. Related topics

Return as structured list."
```

### Phase 2: Write Individual Entries

```bash
python gemini_delegate.py \
  --sources ./corpus \
  --output ./wiki \
  --mode agent \
  --prompt "Write an encyclopedia article about [TOPIC].

Structure:
1. Lead section (definition + summary, 200 words)
2. Background/History
3. Main content sections (3-5 as appropriate)
4. See Also (related topics)
5. References (source citations)

Requirements:
- Neutral, encyclopedic tone
- Every factual claim cited: [Source: filename]
- 2,000-4,000 words depending on topic depth
- Include relevant quotes where they add value
- Cross-reference related topics in [[brackets]]"
```

### Phase 3: Build Index

```bash
python gemini_delegate.py \
  --sources ./wiki \
  --output ./wiki \
  --mode agent \
  --prompt "Create an index file linking all encyclopedia entries.

Include:
1. Alphabetical listing with brief descriptions
2. Category groupings
3. Cross-reference map showing connections"
```

## Prompt Template: Single Entry

```
Write an encyclopedia article about [TOPIC] based on the provided sources.

Structure:
## [Topic Name]
[Lead: 2-3 sentence definition and summary]

### Background
[Historical context, origins, development]

### [Main Section 1]
[Core content with citations]

### [Main Section 2]
[Additional content]

### [Main Section 3]
[If needed]

### See Also
- [[Related Topic 1]]
- [[Related Topic 2]]

### References
[List of sources cited]

Requirements:
- Encyclopedic tone (neutral, informative)
- Cite every factual claim: [Source: filename.md]
- 2,000-4,000 words
- Use direct quotes sparingly but effectively
- Cross-reference related topics with [[brackets]]
```

## Prompt Template: Batch Generation

```
Create encyclopedia entries for these topics: [LIST]

For each entry:
1. Lead section (definition + 2-3 sentence summary)
2. 2-4 content sections as appropriate
3. See Also links
4. Source citations

Write each entry as a separate file: [topic_name].md
Target 1,500-3,000 words per entry depending on source depth.
Maintain consistent formatting across all entries.
```

## Citation Format

In-text citations:
```
The process involves cellular respiration [Source: metabolism.md] which converts glucose into ATP.
```

Quotes:
```
As noted in the research: "Direct quote here" [Source: study.md]
```

References section:
```
### References
- metabolism.md - Interview on cellular processes
- study.md - Research paper on ATP production
```

## Quality Checklist

- [ ] Lead section provides complete summary
- [ ] All claims have source citations
- [ ] Tone is neutral and encyclopedic
- [ ] Sections are logically organized
- [ ] Related topics are cross-referenced
- [ ] Word count meets target for topic depth
- [ ] No original research (only source-based claims)

## Example: Ray Peat Wiki Entry

```bash
python gemini_delegate.py \
  --sources ./ray-peat-corpus \
  --output ./peat-wiki \
  --mode agent \
  --prompt "Write an encyclopedia article about 'Estrogen and Stress'.

Structure the article with:
1. Lead (definition of estrogen-stress relationship)
2. Biological mechanisms
3. Research history
4. Practical implications
5. Related concepts
6. References

Use Ray Peat's explanations but maintain encyclopedic tone.
Cite specific sources for each claim.
Cross-reference related wiki entries.
Target 3,000 words."
```
