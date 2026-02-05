# Content OS

> 93 skills for AI-assisted content creation. Transform, don't generate.

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
├── skills/           # Skills across 13+ categories
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

## Related Projects

- **Skill Stack** (`../skill-stack/`) - Web app for the course
- **Skill Stack Studio** (`../skill-stack-studio/`) - Content planning

## Current Status

- Skills organized and cataloged
- Install script ready
- Consolidated from standalone + skill-stack/content-os copies

See `HANDOFF.md` for full context and next steps.
