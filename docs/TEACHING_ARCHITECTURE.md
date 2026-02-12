# Content OS - Teaching Architecture

> A 5-module video course that teaches non-technical creators how to build their own Claude Code content machine.

---

## Core Thesis

**Transform, Don't Generate.** Every module starts with the student's own raw material and shows them how a specific skill transforms it into something publishable. The course itself is produced using the system (meta is the message).

**4S Framework** threads through every module:
- **Source** - Your raw material (what you already have)
- **Substance** - The core insight being expressed
- **Structure** - The format that delivers it
- **Style** - Your distinctive voice

---

## Audience

**Non-technical creators** - newsletter writers, podcasters, content marketers. They use Notion, Google Docs, and social platforms daily but have never opened a terminal. They're drowning in content demands and intrigued by AI but disappointed by generic ChatGPT output.

**The transformation:** From "AI writes for me (badly)" to "AI transforms my raw material into finished content (in my voice)."

---

## Module Sequence

### Module 0: Setup (Prerequisite / Bonus)
**"Get Your Rig Running"**

Not a proper module - a setup guide they complete before Module 1. Could be a short video or just the README from the `anyone-can-claude-code` repo.

- Install Cursor
- Install Claude Code extension
- Clone the Content OS repo
- Run `./scripts/install.sh`
- Open Claude Code and say hello

**Deliverable:** Working environment with skills installed.

**Corresponding repo:** `anyone-can-claude-code/`

---

### Module 1: Source
**"Curate and Import Your Source Material"**

This is where every content system lives or dies. Before any AI touches anything, the student learns to identify and organize what they already have.

**What they learn:**
- The difference between generating and transforming (the whole philosophy)
- What counts as "source material" (transcripts, voice memos, notes, bookmarks, existing posts)
- How to get source material INTO the system (drag files, paste text, voice memo pipeline)
- How CLAUDE.md works (your AI's memory)

**Skills unpacked:**
- `transcript-polisher` - show how a raw transcript becomes clean source material
- `inbox-processor` - how to route captured ideas to the right place
- `bulk-transcribe` - batch processing for people with lots of audio

**Hands-on project:** Student imports 3 pieces of their own source material (a voice memo, some notes, a transcript or article they've saved) and organizes them in their workspace.

**Key insight for student:** "You already have more raw material than you think. The bottleneck isn't ideas - it's processing."

---

### Module 2: Style
**"Teach AI to Write Like You"**

The module that makes everything personal. Before producing any content, the student captures their voice so every output sounds like them, not like a robot.

**What they learn:**
- Why AI writing sounds like AI (the tells)
- How to extract style rules from their own writing samples
- How skills encode knowledge the model can't have without you
- The difference between a prompt and a skill

**Skills unpacked:**
- `anti-ai-writing` / `human-writing` - the core human voice system
- `voice-matching-wizard` - interactive wizard that captures their voice from samples
- `ai-tells` - learn to spot and kill AI patterns

**Hands-on project:** Student provides 3-5 writing samples (emails, posts, anything). Together with Claude, they build a personal `writing-style` skill that captures their voice. Then they test it: give Claude a topic and compare output with and without the skill.

**Key insight for student:** "A skill is just a markdown file. You can read it, edit it, improve it. It's not magic - it's documentation of how you think."

---

### Module 3: Structure
**"Turn One Idea Into Five Formats"**

Now they have source material (Module 1) and a voice skill (Module 2). This module shows how structure transforms the same substance into different outputs.

**What they learn:**
- Hub-and-spoke content model (one source, many outputs)
- How different formats serve different platforms
- Image generation as a content format
- The prompt-as-specification pattern

**Skills unpacked:**
- `image-prompt-generator` - generate visuals from concepts (the "wow" moment for non-technical users)
- `social-content-creation` - turn a single idea into platform-specific posts
- `hook-and-headline-writing` - the attention layer

**Hands-on project:** Take one piece of source material from Module 1 and produce:
1. A social post (using their voice skill from Module 2)
2. An image prompt for that post
3. A newsletter intro
4. A thread/carousel outline

**Key insight for student:** "Structure is the multiplier. Same substance, different containers. This is how one podcast episode becomes 15 pieces of content."

---

### Module 4: Workflows
**"Chain Skills Into Multi-Step Pipelines"**

Single skills are useful. Chained skills are a system. This module shows how to combine skills into repeatable workflows.

**What they learn:**
- How skills can reference and build on each other
- Building a repeatable workflow (not a one-off prompt)
- The CLAUDE.md as a workflow orchestrator
- When to use Claude Code vs. ChatGPT (context window, file access, skill persistence)

**Skills unpacked:**
- `podcast-production` - full production workflow with checkpoints (the exemplar multi-step skill)
- `ghostwriter` - source material in, polished prose out
- `skill-creator` - how to build their own skills (meta-skill)

**Hands-on project:** Student designs and builds a 3-step workflow for their own content type. Examples:
- Podcaster: transcript → blog post → social promotion
- Newsletter writer: research → draft → format for Beehiiv
- Coach: client session notes → follow-up email → social insight post

**Key insight for student:** "You're not learning to use a tool. You're building a system that compounds. Every skill you create makes the next one easier."

---

### Module 5: Publishing
**"Ship It - From Draft to Live"**

The final module connects the content machine to actual publishing. No more drafts sitting in folders.

**What they learn:**
- Connecting Claude Code to external platforms (MCPs)
- The review/approval step (human judgment stays in the loop)
- Batch publishing workflows
- How to maintain and improve skills over time

**Skills unpacked:**
- `newsletter-writer` skills (daily/weekly examples)
- `x-posting` / `social-content-creation` - publishing workflows
- `quality-loop` - the review cycle that improves output over time

**Hands-on project:** Student publishes one real piece of content end-to-end using their system:
1. Source material (already have from Module 1)
2. Transform using voice skill (Module 2)
3. Structure for their platform (Module 3)
4. Run through their workflow (Module 4)
5. Publish

**Key insight for student:** "The system is now yours. You own the skills, you own the workflow, you own the voice. None of this is locked in a SaaS product."

---

## Course Arc

```
Module 0        Module 1        Module 2        Module 3        Module 4        Module 5
SETUP    -->    SOURCE    -->    STYLE    -->    STRUCTURE  -->  WORKFLOW  -->   PUBLISH

"Get running"   "What do I      "How do I       "What formats   "How do I       "How do I
                 have?"          sound?"         work?"          chain it?"      ship it?"

                 4S: Source      4S: Style       4S: Structure   4S: Substance   All 4S
                                                                 (the glue)      together
```

---

## Teaching Principles

1. **Build, don't lecture.** Every module produces a tangible artifact the student keeps.
2. **Their material, not templates.** Generic examples are for the README. The course uses the student's own content.
3. **Show the skill file.** Don't hide the markdown. Let them see it, read it, understand it's just text.
4. **Meta is the message.** Show that this course's content was produced using the system.
5. **Progressive complexity.** Module 1 is drag-and-drop. Module 5 chains multiple skills with MCPs.

---

## Video Format

Each module video follows the same structure:

1. **Cold open** (30 sec) - Show the finished output. "Here's what we're building today."
2. **The problem** (1-2 min) - Why does this matter? What's the pain point?
3. **The skill** (3-5 min) - Open the skill file. Walk through what it does. Demystify it.
4. **Live build** (5-10 min) - Screencast of actually doing it with real material.
5. **Your turn** (1 min) - Assignment: do this with YOUR material.

**Target length:** 10-15 min per module. Tight. No filler.

---

## What Students Walk Away With

By end of course, each student has:

- [ ] A working Claude Code environment with skills installed
- [ ] Their own source material organized and accessible
- [ ] A personal `writing-style` skill encoding their voice
- [ ] At least 5 pieces of transformed content
- [ ] A custom multi-step workflow for their content type
- [ ] One published piece produced entirely through the system
- [ ] Understanding of how to create new skills on their own

---

## Pricing / Packaging (TBD)

| Tier | Includes | Price |
|------|----------|-------|
| **Free** | Content OS repo + README + Module 0 setup | $0 |
| **Course** | All 5 modules + assignments | TBD |
| **Cohort** | Course + live Q&A + skill review | TBD |
| **DFY** | Done-for-you skill library setup | TBD |

---

## Production Notes

- Record in Cursor with Claude Code visible (not a terminal - too intimidating for audience)
- Use split screen: skill file on left, Claude output on right
- Keep the repo public - course value is the teaching, not the skills themselves
- Consider "One Skill" Shorts (15-30 sec) as promotional content for each skill in the library

---

## Related Files

- `README.md` - Current user-facing docs (needs update after architecture is final)
- `manifest.json` - Full 93-skill catalog
- `content-os-architecture.html` - Interactive architecture playground
- `HANDOFF.md` - Previous session context
- `../skill-stack-studio/studio/plans/content-os-offering.md` - Business model notes

---

*Created: 2026-02-03*
*Priority: Design teaching architecture for Content OS (from HANDOFF.md)*
