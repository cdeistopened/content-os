# Research Synthesis

Compile research from multiple sources into comprehensive reports.

## When to Use

- Synthesizing academic papers into a literature review
- Combining expert interviews into a research report
- Analyzing multiple perspectives on a topic
- Creating briefing documents from diverse sources
- Any "make sense of all this research" project

## Workflow

### Phase 1: Initial Survey

```bash
python gemini_delegate.py \
  --sources ./research \
  --mode analyze \
  --prompt "Survey these research sources and identify:

1. Main themes/topics covered
2. Key findings across sources
3. Areas of agreement
4. Contradictions or tensions
5. Gaps in the research

Return as structured analysis."
```

### Phase 2: Deep Synthesis

```bash
python gemini_delegate.py \
  --sources ./research \
  --output ./synthesis \
  --mode agent \
  --prompt "Create a comprehensive research synthesis.

Structure:
1. Executive Summary (500 words)
2. Methodology (how sources were analyzed)
3. Key Themes (organized by topic)
4. Findings with Evidence (extensive quotes)
5. Points of Consensus
6. Unresolved Questions
7. Recommendations
8. Source Bibliography

Requirements:
- 5,000-10,000 words
- Every finding supported by source quotes
- Note which sources support/contradict each point
- Acknowledge limitations and gaps"
```

### Phase 3: Extract Actionable Insights

```bash
python gemini_delegate.py \
  --sources ./synthesis \
  --mode analyze \
  --prompt "From this synthesis, extract:

1. Top 10 actionable insights
2. Key decisions that need to be made
3. Questions requiring further research
4. Recommended next steps

Format as executive brief (1,000 words)."
```

## Prompt Template: Literature Review

```
Create a literature review from these sources on [TOPIC].

Structure:
## Literature Review: [Topic]

### Introduction
- Research question
- Scope and boundaries
- Methodology

### Theoretical Framework
- Key concepts and definitions
- Relevant theories

### Thematic Analysis
[Organize by themes, not by source]

#### Theme 1: [Name]
- Synthesis of findings
- Supporting evidence from sources
- Contradictions or debates

#### Theme 2: [Name]
[etc.]

### Discussion
- Points of consensus
- Ongoing debates
- Gaps in research

### Conclusions
- Summary of key findings
- Implications
- Future research directions

### References
[All sources cited]

Requirements:
- 5,000-8,000 words
- Synthesize, don't summarize each source separately
- Use direct quotes to support key points
- Note source agreement/disagreement explicitly
```

## Prompt Template: Expert Synthesis

```
Synthesize these expert interviews/perspectives on [TOPIC].

Create a report showing:
1. Where experts agree
2. Where they disagree and why
3. Unique insights from each source
4. Overall picture that emerges

Structure:
- Executive Summary (300 words)
- Areas of Consensus (with supporting quotes)
- Debates and Tensions (contrasting perspectives)
- Novel Insights (unique contributions)
- Synthesis: The Bigger Picture
- Implications and Recommendations

Use extensive quotes to let experts speak directly.
Note which expert holds which position.
Target 4,000-6,000 words.
```

## Synthesis Techniques

### Thematic Organization
Don't summarize source-by-source. Organize by theme:

```
Bad:  "Source A says X. Source B says Y."
Good: "On the topic of X, researchers agree that...
       [Source A quote] However, [Source B] notes a key exception..."
```

### Contrast Mapping
When sources disagree:

```
The question of [topic] reveals a key tension in the literature.

Position A (held by [sources]):
> "[Supporting quote]" - Source

Position B (held by [sources]):
> "[Contrasting quote]" - Source

This disagreement may stem from [analysis of why].
```

### Evidence Weighting
Note strength of evidence:

```
Strong consensus: [claim] - supported by [N] sources
Emerging evidence: [claim] - noted by [sources] but limited data
Contested: [claim] - disputed between [sources]
```

## Quality Markers

- Every claim attributed to sources
- Themes emerge from evidence, not imposed
- Contradictions explicitly acknowledged
- Gaps and limitations noted
- Quotes used as evidence, not decoration
- Synthesis adds value beyond individual sources

## Example: Multi-Expert Analysis

```bash
python gemini_delegate.py \
  --sources ./expert-interviews \
  --output ./analysis \
  --mode agent \
  --prompt "Synthesize these expert interviews on [TOPIC].

Create a comprehensive analysis showing:
1. Where experts converge (with quotes)
2. Key disagreements (contrasting quotes)
3. Unique insights from each expert
4. The overall picture that emerges
5. What remains unresolved

Write 6,000+ words. Use extensive quotes.
Organize by theme, not by expert.
Note which expert holds which position."
```
