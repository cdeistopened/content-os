---
name: opened-daily-newsletter-writer
description: Creates Monday-Thursday OpenEd Daily newsletters (500-800 words) with Thought-Trend-Tool structure. Use when the user asks to create a daily newsletter, write daily content, or transform source material into newsletter segments. Not for Friday Weekly digests.
---

# OpenEd Daily Newsletter Writer

Creates Monday-Thursday daily newsletters (500-800 words) that challenge standardized education with contrarian angles and authentic voice. Structured workflow with approval checkpoints.

**Not for:** Friday Weekly digests (use `weekly-newsletter-workflow`), social media only, or blog posts.

## Session Startup

### Pull Staging Content from Notion

Use one `notion-search` call to find all staged Thought/Tool/Trend items:

```
notion-search:
  query: "staging Thought Tool Trend"
  query_type: "internal"
  data_source_url: "collection://5d0c1ad8-e111-4162-91da-2cac9bd1269b"
  filters:
    created_date_range:
      start_date: "2025-10-01"
```

This returns items in staging with `Content Formats` containing Thought, Tool, or Trend. Parse the results to build your curation options.

**To drill into a specific item:** Use `notion-fetch` with the page ID from search results.

### Sync Published Content (Optional)

For internal linking to published content:

```bash
cd "Studio/Misc. Utilities/seomachine" && python3 -c "
from dotenv import load_dotenv
load_dotenv('data_sources/config/.env')
from data_sources.modules.webflow import sync_content_database
sync_content_database()
"
```

---

## Workflow

### Phase 1: Content Curation

Select 3 segments (Thought/Tool/Trend) ensuring orthogonality and thematic coherence.

**Segment types:**
- **THOUGHT:** Contrarian takes, educational philosophy
- **TREND:** Current developments, research, student stories
- **TOOL:** Practical resources readers can use immediately

**Segment order:** THOUGHT → TREND → TOOL (standard flow)

**Critical:** Thought and Trend must be related but NOT repetitive.

### Content Sourcing Rules

**TOOLs:**
- Primary source: [Tool Database](../../../Studio/Lead Magnet Project/OpenEd_Tool_Database.md) (200+ tools with quotes/stats)
- Also valid: Tools mentioned in source articles during research
- Must have concrete detail (stats, quotes, specific features)

**THOUGHTs:**
- Named individuals + direct quotes work best
- "Happy, not Fortune 500" > generic philosophy
- Tag articles with THOUGHT potential during initial analysis

**TRENDs:**
- Vary topics — avoid repeating "enrollment surge" pattern every issue
- Look for: learning science, tech/AI, parent behavior, international comparisons
- Specific numbers + authoritative sources

**Avoid:**
- Heavy ESA/school choice policy content
- Federal tax programs
- State-specific policy details (unless the story transcends the state)

**Unused content:** Save to [Content Queue](../../../Studio/OpenEd Daily/CONTENT_QUEUE.md) organized by segment type

Create working folder:
```bash
mkdir "Studio/OpenEd Daily/[YYYY-MM-DD] - [Brief Theme]/"
```

Create `Source_Material.md` with URLs, key quotes, and angle notes.

---

### Phase 2: Angle Development (Checkpoint 1)

Create `Checkpoint_1_Angles.md` - **DO NOT proceed to Phase 3 without approval.**

For each segment, generate 3-4 angles using:
- What's the contrarian but obviously true take?
- How does this challenge standardized education?
- Would Sarah (our One True Fan) forward this?

See [OpenEd Identity Framework](../../Frameworks/Basic Context/OpenEd Identity Framework.md) for core beliefs.

**Segment structure:**
- **THOUGHT:** Story first, insight second (~100-120 words)
- **TREND:** Data and concrete examples (~100-120 words)
- **TOOL:** Lead with benefit, not description (~100-120 words)

**Section titles:** ALL CAPS H2, 1-5 words. Short is better. Format: `THOUGHT: Two Outcomes` or just `THE HAPPY QUESTION`. Use sticky techniques (alliteration, contrast, curiosity).

**Subject lines:** Generate 10 options (8-10 words max):
- 3-4 Curiosity-Based
- 3-4 Specificity-Based
- 2-3 Hybrid

See [Subject Line Guide](../../Frameworks/Newsletter/Subject Line Guide.md) for formulas.

**Preview text:** Should give enough context that someone knows what they're getting, while still creating curiosity.

Formula: `[Specific claim]. [Context]. [Gap/tension]. PLUS: [bonus]`

Example: "Students who test themselves retain 80% more. Researchers have known this since the 1900s. Schools still don't do it. PLUS: an app that does."

Not just keywords - actual mini-summary with curiosity.

**Checkpoint 1 template:**
```markdown
# Checkpoint 1: Angles & Structure - [Date]

## SUBJECT LINE OPTIONS (10 total)
[Organize by type: Curiosity, Specificity, Hybrid]

## PREVIEW TEXT
[Draft]

## SEGMENT 1: [TITLE] (Type)
**Source:** [URL]
**Angle Options:** [3-4 options]
**Recommended:** [Which and why]
**Structure:** Hook / Substance / Insight

## SEGMENT 2: [TITLE] (Type)
[Same format]

## SEGMENT 3: [TITLE] (Type)
[Same format]

## ORTHOGONALITY CHECK
- [ ] Thought and Trend are distinct
- [ ] Aligns with OpenEd beliefs
- [ ] Would Sarah forward this?
```

🛑 **PAUSE:** Get user approval before Phase 3.

**User feedback notation:**
- `***` = preferred choice
- `<>` = extrapolate contextually
- `{question}` = answer directly
- `~~text~~` = delete

---

### Phase 3: Newsletter Writing

Create `Newsletter_DRAFT.md` after Checkpoint 1 approval.

### Opening Letter Strategy (~100-150 words)

The opening letter establishes the relationship with the reader. It should be personal, encouraging, and slightly contrarian or curious.

**Key Elements:**
1.  **Greeting:** "Greetings Eddies!", "Welcome Eddies!", or "Greetings!".
2.  **The Hook:** Start with a story, a startling statistic ("20,000 subscribers", "$16,000 per child"), a contrarian question ("Why do students find science boring?"), or a community milestone.
3.  **The Pivot:** Connect the hook to the broader mission of "opening up education" or the specific value in today's issue.
4.  **The Tease:** Mention what's coming (Deep Dive, etc.) without summarizing it.
5.  **The Sign-off:** Almost always ends with "Let's dive in." (or occasionally "Read on...").

**Style Notes:**
-   **Voice:** Encouraging ("you've got this!"), authentic (admits to "silly gimmicks"), and mission-driven.
-   **Format:** Short paragraphs (1-2 sentences).
-   **Signature:** The opening is a prelude; sign off with "Let's dive in." The actual signature ("– Charlie") comes at the end of the newsletter.

**Examples:**
- *Milestone/Community:* "Greetings Eddies! It just came to my attention that the OpenEd Daily hit a new milestone... We take this as a sign of the growing appetite for trustworthy content... Onward & upward,"
- *Contrarian/Data:* "Greetings! An education expert recently published something that's making a lot of parents nervous... The data sounds brutal, but is he interpreting it correctly? Let's dive in."
- *Story-Driven:* "Greetings! Ken Danford had spent six years teaching... In it, he found case studies of teens who left school and turned out... fine! Let's dive in."

**Opening Checklist:**
- [ ] Greetings Eddies! (or variation)
- [ ] Hook (Story/Stat/Question)
- [ ] Pivot to mission/value
- [ ] "Let's dive in." sign-off
- [ ] ❌ No spoiling the segments

**Write 3 segments (each ~100-120 words):**

Apply voice from:
- [Pirate Wires Style Guide](../../Frameworks/Style/Pirate Wires Imitation Style Guide.md)
- [OpenEd Writing Guide](../../Frameworks/Style/OpenEd Newsletter Style Guide The Art of Impactful Writing.md)

**Format requirements:**
- NO EMOJIS (non-negotiable)
- ALL CAPS H2 titles for segments
- **Bold** for key quotes/stats
- Hyperlinks throughout (not just at ends)
- `---` between sections

**Internal Linking:**
When mentioning topics covered in existing OpenEd content, link to them. Search the content index:
```bash
grep -i "keyword" "Studio/Misc. Utilities/seomachine/context/content-index.csv"
```
Priority: Blog Posts > Podcasts > other Daily newsletters. Aim for 2-3 internal links per newsletter where natural.

**Complete structure:**
```markdown
**SUBJECT:** [From Checkpoint 1]
**PREVIEW:** [From Checkpoint 1]
---

[Opening]
---

## [SEGMENT 1 TITLE]
[100-120 words]
---

## [SEGMENT 2 TITLE]
[100-120 words]
---

## [SEGMENT 3 TITLE]
[100-120 words]
---

That's all for today!

– Charlie (the OpenEd newsletter guy)

P.S. [Optional announcement]
```

**Target:** 500-800 words total.

Submit as `Newsletter_DRAFT.md`. Iterate based on user feedback using notation from Phase 2.

---

### Phase 4: Social Media (Optional)

For social repurposing, use the `social-content-creation` skill or create `Social_Media_Plan.md`.

See [Social Media frameworks](../../Frameworks/Social Media/) for templates.

---

### Phase 5: QA & Archive

**Final checklist:**
- [ ] Segments are orthogonal
- [ ] NO EMOJIS in body
- [ ] ALL CAPS H2 titles
- [ ] 500-800 words total
- [ ] All links work
- [ ] Aligns with OpenEd beliefs

**Archive:**
```bash
cp [working-folder]/Newsletter_FINAL.md daily-newsletter-workflow/examples/[YYYY-MM-DD]-newsletter.md
```

## Voice: What Actually Works

Don't follow style guides mechanically. Channel this instead:

**The Core Principle: Context + Substance**

Every segment must deliver both:
1. **Context** - Who is this person? What did they do? Why should I care?
2. **Substance** - What's the actual insight, data, or takeaway?

Don't just introduce someone and then tell us they're interesting. Show us what they discovered. Don't just describe a trend - give us the number, the study, the specific detail that makes it real.

**Bad:** "Justin Skycak runs Math Academy and has interesting ideas about education."
**Good:** "Justin Skycak runs Math Academy. His argument: schools use teaching methods that research abandoned decades ago - spaced repetition, retrieval practice, deliberate practice. Researchers have studied this since the 1900s. Schools just don't do it."

The second version delivers substance. The first is a placeholder.

### Context + Substance Examples (from Pirate Wires)

**Example 1 - Debunking a study:**
> "A new MIT study claims LLM users 'consistently underperform' on neural and linguistic tests — and AI doomers are obsessed. A professor on Bluesky declares the 'death knell' of AI, and normies are 'terrified' ChatGPT will rot our brains. Of course, none of them read the 206-page report, which reveals 18 college students had 20min to write essays based on (boring) SAT prompts using only ChatGPT. They could barely recall what they 'wrote,' meaning they just copy/pasted, lol..."

**Why it works:** Context (the study, the reaction) + Substance (18 students, 20 minutes, SAT prompts, copy/paste behavior). The substance undermines the context - that's the insight.

**Example 2 - Funding news:**
> "Last week, former OpenAI CTO Mira Murati raised $2 billion in seed funding (!) for her stealth AI startup, Thinking Machines Lab, valuing the six-month-old company at around $10 billion with, from best I can tell, no product or business. This on the heels of Mark Zuckerberg offering $100 million signing bonuses for Sam Altman's engineers..."

**Why it works:** Specific numbers ($2B, $10B, $100M) make abstract "AI funding is crazy" concrete. The parenthetical "(from best I can tell, no product or business)" is the insight delivered conversationally.

**Example 3 - Local dysfunction:**
> "Bay Area electrical engineer Patrick McCabe has created an app called Solve SF that allows city residents to file 311 reports about issues like poop on the sidewalk in as little as 10 seconds, far faster than the city's official 311 app. Unfortunately, because nice things are illegal in San Francisco, the city is about to effectively shut down Solve SF when they discontinue use of the API it runs on, citing maintenance costs..."

**Why it works:** Person + specific thing they built + specific problem = context. The contrast (10 seconds vs. city app, maintenance costs vs. other budget priorities) = substance that reveals dysfunction without lecturing.

**The vibe:** A smart person talking to another smart person. No performance. No manipulation. Just: here's what happened, here's why it matters.

**Trust the reader.** Don't tell them how to feel ("this should make you uncomfortable"). Show them the thing. They'll feel something.

**Say less.** If you wrote it twice, delete one. "She pulled her 14-year-old out" + "So she pulled her out" = redundant. Cut it.

**No fake questions.** "The top concerns?" is a crutch. Nobody's actually asking. Just tell them.

**Short sentences are fine.** Fragments too. "Stomach aches gone." works. Don't dress it up.

**Avoid AI tells:**
- Correlative constructions ("She wasn't X. She was Y.")
- Rhetorical questions that set up your own point
- "Meanwhile:" at the start of paragraphs (use sparingly)
- Trying to sound punchy instead of actually being clear
- "X:" pattern before explanations ("The classic study:" / "The clever part:") - just write naturally
- Triple Threat Syndrome (grouping everything in threes)
- Empty enthusiasm ("Absolutely!", "Great question!")
- Thesaurus abuse ("utilize" instead of "use")

**For complete AI-tell reference:** See `ai-tells` skill

**The test:** Read it out loud. Does it sound like a person talking? Or like someone performing "good writing"?

---

## Tone: Curious > Accusatory

Notice things. Don't blame.

When critiquing institutions (schools, EdTech, etc.), observe the gap rather than attack. Let the reader draw conclusions.

**Bad:** "Schools prioritize fun over learning. Educators are failing our kids."
**Good:** "Skycak's point isn't that educators are villains. It's that maximizing learning isn't the only thing schools are trying to do, and maybe not even the main thing."

The reader will notice. You don't have to tell them how to feel.

---

## Sentence Rhythm

Vary sentence length. Not all staccato.

Short sentences work. Fragments too. But walls of choppy fragments feel robotic. Mix long flowing sentences with short punches.

**Bad (all staccato):**
"The research isn't new. Spaced repetition. Retrieval practice. Not controversial. Just not how schools work."

**Good (varied rhythm):**
"His argument is interesting. The techniques aren't new - spaced repetition, retrieval practice, deliberate practice. Researchers have been studying this stuff since the 1900s and it's not controversial. It's just not how schools are set up."

Long sentence builds context → short sentence lands the point.

---

## Context Setting

Lead with WHO is doing WHAT before diving into the argument.

Readers need an anchor. Don't drop them into jargon or claims without context.

**Bad:** "Spaced repetition. Retrieval practice. Deliberate practice. This stuff has been studied since the 1900s..."

**Good:** "Justin Skycak runs Math Academy, an online learning platform, and he's been writing about why schools don't use methods that actually work."

First sentence: who this person is, what they do. Then: their argument.

---

## Headlines: Curiosity Over Cleverness

Section titles (H2s) should make readers want to know what's underneath.

**Good headlines:**
- Create an information gap (reader needs to read to close it)
- Use specific numbers or details
- Imply a story or tension
- Are short (2-5 words ideal)

**Headline patterns that work:**
- **The Label:** "THE GETTING BY TRAP" - names a phenomenon
- **The Stat:** "83% OF PARENTS AGREE" - specific number creates credibility
- **The Object:** "TOOL: CHOMPSAW" - clear, direct, says what it is

**Avoid:**
- Generic labels ("WHAT WE LEARNED")
- Questions as headlines ("WHAT IF...?")
- Clickbait that doesn't deliver
- Puns that sacrifice clarity

**Subject lines:** Same principles. Create curiosity, be specific, don't oversell. The reader should think "I need to know more" not "I've been promised something."

**Counterintuitive framing works:** "The other kind of testing" challenges assumptions (testing = bad?) without revealing the answer. Reader has to open to find out.

---

## Reference Files

**Core frameworks:**
- [OpenEd Identity Framework](../../Frameworks/Basic Context/OpenEd Identity Framework.md) - Beliefs and audience
- [Subject Line Guide](../../Frameworks/Newsletter/Subject Line Guide.md) - Formulas and strategies
- [Pirate Wires Style](../ghostwriter/references/pirate-wires-style.md) - Voice examples (read for vibe, not rules)
- [OpenEd Writing Guide](../../Frameworks/Style/OpenEd Newsletter Style Guide The Art of Impactful Writing.md) - Sticky sentences
- [Opening Letter Examples](references/Opening_Letter_Examples.md) - Examples of tone and structure

**Content resources:**
- [Tool Database](../../../Studio/Lead Magnet Project/OpenEd_Tool_Database.md) - 200+ tools with quotes and stats
- [Content Queue](../../../Studio/OpenEd Daily/CONTENT_QUEUE.md) - Unused THOUGHT/TREND/TOOL material

**Related skills:**
- `weekly-newsletter-workflow` - Friday digest
- `social-content-creation` - Social repurposing
- `linkedin-content` - LinkedIn-specific posts with framework matching

## File Naming

Working folder: `Studio/OpenEd Daily/[YYYY-MM-DD] - [Theme]/`

Files:
- `Source_Material.md`
- `Checkpoint_1_Angles.md`
- `Newsletter_DRAFT.md`
- `Newsletter_FINAL.md` (only after approval)

## Critical Reminders

❌ NO EMOJIS in body
❌ Don't skip Checkpoint 1
❌ Opening must not spoil segments (tease, don't summarize)
❌ Thought and Trend must be orthogonal
✅ 500-800 words total
✅ ALL CAPS H2 titles
✅ Link early and often
