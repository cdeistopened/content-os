---
name: voice-wizard
version: 1.0.0
description: "When the user wants to create a voice skill from writing samples, emphasizing examples over instructions (70% examples, 30% instructions). Also use when building example-heavy voice profiles. For guided wizard workflow, see voice-matching-wizard. For voice analysis, see voice-analyzer."
---

# Voice Wizard

Create a voice skill from writing samples.

**The Key Insight:** Examples teach voice. Instructions are secondary. The output skill should be 70% examples, 30% instructions.

---

## The Process

### Step 1: Research and Collect Samples

**This is the most important step.**

If analyzing a known writer:
- Use WebSearch and WebFetch to find their published work
- Look for essays, articles, newsletters - extended prose
- Collect 3-5 substantial passages (300+ words each)
- Prioritize passages that show technique, not just topic

If analyzing your own writing:
- Gather 3-5 pieces you're proud of
- Same medium (all newsletters, all blog posts)

**What makes a good sample:**
- Shows the writer's rhythm and sentence variation
- Demonstrates their structural moves
- Reveals their relationship to the reader
- Long enough to see patterns (not tweets)

### Step 2: Extract Key Passages

From your samples, select:
- 2-3 **opening passages** that show how they begin
- 3-5 **body paragraphs** that demonstrate their rhythm
- 2-3 **closing passages** that show how they end
- 5-10 **signature sentences** that capture the voice

These passages ARE the skill. Everything else is commentary.

### Step 3: Identify Patterns (Briefly)

Note:
- Sentence length variation pattern
- How they elaborate on assertions
- What they avoid
- Key anti-AI patterns for this voice

Keep this section SHORT. The examples do the teaching.

### Step 4: Generate the Voice Skill

**Structure the output skill like this:**

```markdown
---
name: voice-[name]
description: Write in [Name]'s voice. [One sentence]. Examples-based - absorb the rhythm from the passages below.
---

# Voice: [Name]

[One paragraph describing the voice]

---

## Examples to Absorb

Read these passages. Absorb the rhythm. Let them train your ear.

### Opening Passages

[Full paragraph from their work]

[Full paragraph from their work]

### Body Passages

[Full paragraph showing their technique]

[Full paragraph showing their technique]

[Full paragraph showing their technique]

### Signature Sentences

1. "[Actual sentence]"
2. "[Actual sentence]"
3. "[Actual sentence]"
4. "[Actual sentence]"
5. "[Actual sentence]"

### Closing Passages

[Full paragraph showing how they end]

---

## Brief Technique Notes

[3-5 bullet points only - the examples teach; this just names what to notice]

- Sentence rhythm: [pattern]
- Elaboration style: [pattern]
- What they avoid: [pattern]

## Anti-AI Patterns

- No correlative constructions
- [Voice-specific patterns to avoid]

## The Test

- [ ] Does this sound like the examples above?
- [ ] Would the writer recognize this as their voice?
```

---

## Critical Principles

### Examples > Instructions

A voice skill with 10 good passages and 5 bullet points will outperform one with 50 bullet points and 2 passages.

Claude learns voice from examples, not descriptions. The descriptions just name what's already visible in the examples.

### Research is Required

Don't generate a voice skill from memory. Actually go find the writer's work:

```
Use WebSearch: "[Author name] essay full text"
Use WebFetch: [URL of their published work]
```

Collect real passages. Include them in full.

### Conceal the Channeling

The goal is to channel HOW they write, not WHAT they write about. The examples teach rhythm and sensibility. When applying the voice to new content, the Berry-ness (or whoever-ness) should be felt, not obvious.

### Length of Examples

Each passage should be substantial enough to demonstrate rhythm:
- Minimum: 3-4 sentences
- Ideal: Full paragraph (5-10 sentences)
- Multiple passages show range

---

## Example: What a Good Voice Skill Looks Like

The bulk should be actual passages from the writer's work, with minimal framing. Like this:

> "Most urban shoppers would tell you that food is produced on farms. But most of them do not know what farms, or what kinds of farms, or where the farms are, or what knowledge or skills are involved in farming. They apparently have little doubt that farms will continue to produce, but they do not know how or over what obstacles."

Then a brief note: *Notice: simple declaration → elaboration → accumulated uncertainty. Three sentences, increasing length.*

That's it. The passage teaches. The note names what to see.

---

## Output Location

Save to: `.claude/skills/voice-[name]/SKILL.md`

---

*The best voice skill is a curated anthology of the writer's best passages, with minimal commentary.*

## Related Skills

- **Upstream**: **voice-analyzer**
- **Enhanced by**: **writing-style**
- **Feeds into**: **voice-matching-wizard**, **ghostwriter**
