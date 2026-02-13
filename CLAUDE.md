# Content OS

> 36 skills for AI-assisted content creation. Transform, don't generate.

## What This Is

A publishable GitHub repo bundling skills from across Charlie's workspaces into a single, organized library. Users clone it and use skills as templates for their own content systems.

## Philosophy

**Transform, Don't Generate.** AI refines human material, not replaces it.

**4S Framework:**
- **Source** - Raw material (transcripts, voice memos, notes)
- **Substance** - Core insight being expressed
- **Structure** - Format that delivers the message
- **Style** - Distinctive voice

## Structure

```
content-os/
├── skills/           # Skills across 6 categories
├── examples/         # Example workspace configurations
├── scripts/
│   └── install.sh    # Symlinks skills to user's workspace
├── manifest.json     # Skill catalog
├── README.md         # User documentation
└── CLAUDE.md.template
```

## Key Commands

```bash
# Install skills to a workspace
./scripts/install.sh ~/.claude/skills

# Open architecture playground
open content-os-architecture.html

# Index with QMD for local RAG
qmd collection add . --name content-os --mask "**/*.md"
```

## Origin

This is the open-source skill library from the [Skill Stack](https://skillstack.ai) blog, packaged for standalone use.

## Current Status

- 36 skills organized across 6 categories (writing, video, social, research, content, productivity)
- Install script ready
- Manifest cataloging all skills
- Stripped to Charlie's original skills only (v2.0)
