---
name: inbox-processor
description: Unified inbox processing for Telegram and Voice Memos. Transcribes audio, analyzes content, and routes to projects. Handles multi-topic items by splitting into separate notes. Run with /inbox or invoke directly.
---

# Inbox Processor

Unified system for capturing and routing inputs from Telegram bot and Apple Voice Memos.

## Quick Start

```
/inbox              # Process all pending items
/inbox telegram     # Just Telegram
/inbox voice        # Just Voice Memos
/inbox status       # Show what's pending
```

## What It Does

1. **Collects** from:
   - Telegram bot (@claudiusXIIbot) - voice, text, links, photos
   - Apple Voice Memos (via extract script)

2. **Transcribes** audio via Gemini 3 Flash

3. **Converts photos** to black & white schematics via Gemini Pro Image

4. **Analyzes** content for:
   - Project references (can be multiple per item)
   - Action type (task, idea, reference, archive)
   - Priority signals

5. **Routes** to appropriate project folders:
   - Single-topic items → direct to project
   - Multi-topic items → split into separate notes
   - Photos → schematics folder

## Project Context (For Routing)

| Trigger Keywords | Project | Destination |
|------------------|---------|-------------|
| OpenEd, newsletter, homeschool, education | opened | `OpenEd Vault/Studio/` |
| Skill Stack, AI skills, Claude Code, skills | skill-stack | `CIA/skill-stack/` |
| Naval, podcast production | naval | `CIA/clients/Naval/` |
| Pause, meditation, MBHP, Dr. Miller | pause | `CIA/clients/Pause/` |
| Ray Peat, metabolism, bioenergetic | ray-peat | `CIA/wiki-projects/Ray Peat/` |
| Benedict, fasting, Vigil, liturgy | benedict | `Personal/Benedict Challenge/` |
| JFK50, 50 mile, march, fitness | jfk50 | `Personal/JFK50/` |
| California, CLM, Catholic Land | california-clm | `Personal/California CLM/` |
| California Revival, CalTrad, politics | california-revival | `Personal/California Revival/` |
| Doodle, reader, PDF, transcription | doodle-reader | `CIA/doodle-reader/` |
| Movement app, meetup | movement-app | `CIA/Movement Meetup App/` |
| Wiki, authorise.io | wiki-projects | `CIA/wiki-projects/` |
| Personal, family, Emma | personal | `Life OS/` |

## Photo to Schematic

Send a photo to the Telegram bot and it will automatically convert it to a clean black & white technical schematic.

**How it works:**
1. Send any photo to @claudiusXIIbot
2. Gemini Pro Image converts it to a simplified line drawing
3. Output: 8.5x11 format, pure black lines on white, patent illustration style

**Custom prompts:** Add a caption to your photo to customize the conversion:
- "Focus on the mechanical parts"
- "Include labels for each component"
- "Make it more detailed"

**Output location:** `Life OS/inbox/schematics/`

---

## Multi-Topic Handling

**Explicit delimiter:** Say "new note" in your voice recording to indicate a topic break.

When a voice note mentions multiple unrelated projects:

**Example input:**
> "Two things. First, for OpenEd I want to try a new newsletter format. Second, for Skill Stack I should write about the SEO skill suite."

**Output:** Creates two separate notes:
1. `OpenEd Vault/Studio/ideas/2026-01-18-newsletter-format.md`
2. `CIA/skill-stack/ideas/2026-01-18-seo-skill-suite.md`

Each gets frontmatter linking back to source audio.

## Frontmatter Schema

```yaml
---
source: telegram-voice | telegram-text | telegram-link | voice-memo
date: 2026-01-18
title: Auto-generated title
project: detected-project
action: task | idea | reference
status: unprocessed
original_file: path/to/audio.m4a  # if applicable
split_from: path/to/original.md   # if split from multi-topic
---
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/poll-telegram.sh` | Pull messages from Telegram bot |
| `scripts/extract-voice-memos.sh` | Extract from Apple Voice Memos |
| `scripts/transcribe.sh` | Transcribe audio via Gemini |
| `scripts/route-item.sh` | Analyze and route single item |

## Dependencies

- Gemini API key in `Root Docs/.env`
- Telegram bot token in `Root Docs/.env`
- Full Disk Access for Voice Memos extraction (System Preferences)

## Workflow

```
┌──────────────┐     ┌──────────────┐
│   Telegram   │     │ Voice Memos  │
│     Bot      │     │   (Apple)    │
└──────┬───────┘     └──────┬───────┘
       │                    │
       ▼                    ▼
┌─────────────────────────────────────┐
│         Life OS/inbox/              │
│    (staging area for all inputs)    │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│      Gemini Transcription           │
│   + Project Analysis + Splitting    │
└──────────────────┬──────────────────┘
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
   Project A   Project B   Project C
   (routed)    (routed)    (routed)
```

## Manual Override

If auto-routing is wrong, just move the file manually. The system trusts your judgment over its heuristics.
