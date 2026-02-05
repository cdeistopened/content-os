---
name: opened-daily-newsletter-writer
description: Creates Monday-Thursday OpenEd Daily newsletters using staged sub-agents. Each stage runs independently with only the refined outputs it needs - no context pollution.
---

# OpenEd Daily Newsletter Writer

Creates Monday-Thursday daily newsletters (500-800 words) with Thought-Trend-Tool structure. Uses sub-agents for each stage to keep context clean.

**Not for:** Friday Weekly digests (use `weekly-newsletter-workflow`), social media only, or blog posts.

---

## Architecture Overview

```
ORCHESTRATOR (this conversation)
    │
    ├─► Stage 1: Source Build ──► Source_Material.md
    │                                    │
    │◄──────────── [USER REVIEW] ◄───────┘
    │
    ├─► Stage 2: Substance ─────► Checkpoint_1.md
    │                                    │
    │◄──────────── [USER CHECKPOINT] ◄───┘
    │
    ├─► Stage 3: Draft ─────────► Newsletter_DRAFT.md + questions
    │                                    │
    │◄──────────── [USER ANSWERS] ◄──────┘
    │
    ├─► Stage 4: Subject Lines ─► 10 options
    │                                    │
    │◄──────────── [USER PICKS] ◄────────┘
    │
    └─► Stage 5: Final + Social ► Newsletter_FINAL.md
```

Each sub-agent receives only:
- Refined outputs from previous stages
- Specific reference files it needs
- No MCP history, no iteration debris

---

## Stage 1: Source Build

**Purpose:** Pull staging content from Notion, compile into Source_Material.md

**Sub-agent prompt:**
```
Task:
  subagent_type: general-purpose
  prompt: |
    Pull staged newsletter content from Notion and compile source material.

    1. Search Notion for staging items:
       notion-search:
         query: "staging Thought Tool Trend"
         query_type: "internal"
         data_source_url: "collection://5d0c1ad8-e111-4162-91da-2cac9bd1269b"
         filters:
           created_date_range:
             start_date: "2025-10-01"

    2. For promising items, fetch full content with notion-fetch

    3. Create Source_Material.md with:
       - Each item's title, URL, type (Thought/Tool/Trend)
       - Key quotes and data points
       - Brief notes on potential angles

    Write to: [working-folder]/Source_Material.md
    Return: Summary of what's available (3-5 sentences)
```

**Output:** `Source_Material.md`

**Orchestrator action:** Present summary to user, confirm which items to pursue.

---

## Stage 2: Substance & Angles

**Purpose:** Identify unifying themes, develop angles, create Checkpoint 1

**Inputs:**
- `Source_Material.md`
- OpenEd Identity Framework (for beliefs alignment)

**Sub-agent prompt:**
```
Task:
  subagent_type: general-purpose
  prompt: |
    Read the source material and identity framework. Develop newsletter angles.

    Files to read:
    - [working-folder]/Source_Material.md
    - .claude/skills/opened-identity/SKILL.md

    Create Checkpoint_1.md with:

    ## SELECTED SEGMENTS
    - THOUGHT: [item] - [recommended angle]
    - TREND: [item] - [recommended angle]
    - TOOL: [item] - [recommended angle]

    ## UNIFYING THEME
    [1-2 sentences on what connects these]

    ## ORTHOGONALITY CHECK
    - Thought and Trend are distinct: [yes/no + why]
    - Aligns with OpenEd beliefs: [which ones]

    ## QUESTIONS FOR USER
    [Any clarifications needed before drafting]

    Write to: [working-folder]/Checkpoint_1.md
    Return: The checkpoint content for user review
```

**Output:** `Checkpoint_1.md`

**Orchestrator action:** Present checkpoint to user. Get approval or adjustments before Stage 3.

---

## Stage 3: Draft

**Purpose:** Write the newsletter body with proper voice and headlines

**Inputs:**
- `Source_Material.md`
- `Checkpoint_1.md`
- Voice guide (embedded below)
- Hook & headline patterns

**Sub-agent prompt:**
```
Task:
  subagent_type: general-purpose
  prompt: |
    Write the newsletter draft based on approved angles.

    Files to read:
    - [working-folder]/Source_Material.md
    - [working-folder]/Checkpoint_1.md
    - .claude/skills/ghostwriter/references/pirate-wires-style.md (for vibe, not rules)

    VOICE GUIDANCE:

    The vibe: A smart person talking to another smart person. No performance.
    No manipulation. Just: here's what happened, here's why it matters.

    Trust the reader. Don't tell them how to feel. Show them the thing.

    Say less. If you wrote it twice, delete one.

    No fake questions. "The top concerns?" is a crutch. Just tell them.

    Short sentences are fine. Fragments too. "Stomach aches gone." works.

    Avoid AI tells:
    - Correlative constructions ("She wasn't X. She was Y.")
    - Rhetorical questions that set up your own point
    - "Meanwhile:" overuse
    - Trying to sound punchy instead of being clear

    The test: Read it aloud. Does it sound like a person talking?

    HEADLINE GUIDANCE:

    Section titles (H2s) should create an information gap.

    Patterns that work:
    - The Label: "THE GETTING BY TRAP" - names a phenomenon
    - The Stat: "83% OF PARENTS AGREE" - specific number
    - The Object: "TOOL: CHOMPSAW" - clear and direct

    Avoid: generic labels, questions as headlines, clickbait, puns

    FORMAT:
    - 3 segments, ~100-120 words each
    - ALL CAPS H2 titles
    - NO EMOJIS
    - Links throughout (not just at ends)
    - --- between sections
    - End with: "That's all for today!\n\n– Charlie (the OpenEd newsletter guy)"

    OPENING LETTER: Optional. If included, keep it short (2-3 sentences max).
    Tease, don't summarize. End with "Let's dive in."

    Write to: [working-folder]/Newsletter_DRAFT.md

    Return:
    1. The draft
    2. Any questions or uncertainties for user
```

**Output:** `Newsletter_DRAFT.md` + questions

**Orchestrator action:** Present draft and questions. Get user feedback.

---

## Stage 4: Subject Lines

**Purpose:** Generate 10 subject line options using the Subject Line Guide

**Inputs:**
- `Newsletter_DRAFT.md` (just needs to know what the content is about)
- Subject Line Guide

**Sub-agent prompt:**
```
Task:
  subagent_type: general-purpose
  prompt: |
    Generate subject line options for this newsletter.

    Files to read:
    - [working-folder]/Newsletter_DRAFT.md
    - .claude/skills/opened-daily-newsletter-writer/references/Subject_Line_Guide.md

    Generate 10 subject lines (8-10 words max each):

    ## CURIOSITY-BASED (3-4)
    [Lines that create information gaps]

    ## SPECIFICITY-BASED (3-4)
    [Lines with specific numbers, names, or details]

    ## HYBRID (2-3)
    [Combine curiosity + specificity]

    Principles:
    - Create curiosity, be specific, don't oversell
    - Reader should think "I need to know more"
    - Avoid correlative constructions

    Return: The 10 options, formatted and categorized
```

**Output:** 10 subject line options

**Orchestrator action:** Present options. User picks one.

---

## Stage 5: Final Assembly

**Purpose:** Finalize newsletter with chosen subject line, write preview text, optionally generate social

**Inputs:**
- `Newsletter_DRAFT.md`
- Chosen subject line
- User feedback from Stage 3

**Sub-agent prompt:**
```
Task:
  subagent_type: general-purpose
  prompt: |
    Finalize the newsletter.

    Subject line: [chosen subject line]
    User feedback: [any revisions requested]

    1. Apply any requested revisions to the draft
    2. Add the subject line
    3. Write preview text (40-100 characters)
       - Should complement, not repeat, the subject line
       - Create additional curiosity

    Format:
    **SUBJECT:** [subject line]
    **PREVIEW:** [preview text]

    ---

    [newsletter body]

    Write to: [working-folder]/Newsletter_FINAL.md
    Return: The final newsletter
```

**Output:** `Newsletter_FINAL.md`

**Optional - Social Media:**
```
Task:
  subagent_type: general-purpose
  prompt: |
    Create social posts from this newsletter.

    Read: [working-folder]/Newsletter_FINAL.md
    Read: .claude/skills/social-content-creation/SKILL.md

    Generate:
    - 1 Twitter/X post (280 chars)
    - 1 LinkedIn post (longer form)

    Return: Both posts formatted and ready to copy
```

---

## File Structure

Working folder: `Studio/OpenEd Daily/[YYYY-MM-DD] - [Theme]/`

Files created:
- `Source_Material.md` (Stage 1)
- `Checkpoint_1.md` (Stage 2)
- `Newsletter_DRAFT.md` (Stage 3)
- `Newsletter_FINAL.md` (Stage 5)

---

## Quick Reference

**Segment types:**
- THOUGHT: Contrarian takes, educational philosophy
- TREND: Current developments, research, data
- TOOL: Practical resources readers can use

**Format requirements:**
- 500-800 words total
- ALL CAPS H2 titles
- NO EMOJIS in body
- Links throughout
- `---` between sections

**Critical checks:**
- Thought and Trend are orthogonal (related but not repetitive)
- Voice sounds human, not performative
- Headlines create information gaps
- Subject line creates curiosity without overselling

---

## Reference Files

- `opened-identity` - Brand beliefs and audience
- `ghostwriter/references/pirate-wires-style.md` - Voice (read for vibe)
- `references/Subject_Line_Guide.md` - Subject line formulas
- `social-content-creation` - Social repurposing
