# Content OS - Session Handoff

**Date:** 2026-01-31
**Previous session:** `efc2eade-7757-4a82-a10e-2ac12841fb77` (ran from `/`)

---

## What This Is

Content OS is a publishable GitHub repo that bundles 93 skills from across your workspaces into a single, organized library. Others can clone it and use your skills as templates.

**Philosophy:** Transform, Don't Generate. AI refines human material via the 4S Framework (Source → Substance → Structure → Style).

---

## What Was Accomplished

- [x] Created `/content-os/` repo structure with 93 skills across 13 categories
- [x] Organized skills: writing, video, newsletter, social, brand-voice, research, automation, design, notion, canvas, cursor, productivity, meta
- [x] Created `manifest.json` cataloging all skills
- [x] Created `install.sh` for symlinking skills to workspaces
- [x] Created `CLAUDE.md.template` for users
- [x] Created interactive playground (`content-os-architecture.html`)
- [x] QMD installed at `~/.bun/bin/qmd`
- [x] Moved repo to proper location: `CIA/content-os/`

---

## What's Left To Do

### High Priority
- [ ] Design Content OS teaching architecture (how to teach the 4S framework + skills)
- [ ] Design vault structure (finalize folders vs frontmatter hybrid)

### Medium Priority
- [ ] Rework root CLAUDE.md as personal assistant context
- [ ] Create intentional capture system (batch processing at desk, no heartbeat)

### Lower Priority
- [ ] Set up QMD for local RAG indexing
- [ ] Create url-to-markdown skill
- [ ] Commit and push to GitHub

---

## Key Decisions Made

| Decision | Choice |
|----------|--------|
| **Structure** | 3 areas (OpenEd / CIA / Personal), NOT strict PARA |
| **File organization** | Hybrid: shallow folders for assets, frontmatter tags for notes, wikilinks |
| **Capture mode** | Intentional batch at desk, NOT always-on heartbeat |
| **Local RAG** | QMD for token conservation |
| **Teaching tool** | Zed or Cursor (skills work in any agentic coding tool) |
| **Symlink direction** | Workspaces symlink INTO content-os (single source of truth) |

---

## Architecture Overview

```
content-os/
├── skills/
│   ├── writing/      (14 skills)
│   ├── video/        (9 skills)
│   ├── newsletter/   (5 skills)
│   ├── social/       (6 skills)
│   ├── brand-voice/  (5 skills)
│   ├── research/     (4 skills)
│   ├── automation/   (6 skills)
│   ├── design/       (8 skills)
│   ├── notion/       (4 skills)
│   ├── canvas/       (4 skills)
│   ├── cursor/       (5 skills)
│   ├── productivity/ (6 skills)
│   └── meta/         (4 skills)
├── examples/
├── scripts/
│   └── install.sh
├── manifest.json
├── README.md
├── CLAUDE.md.template
└── content-os-architecture.html  # Interactive playground
```

---

## The Bigger Picture

Content OS feeds into **Skill Stack** - a course teaching agentic content creation. The course itself should be produced USING the system (meta is the message).

**Order of operations for students:**
1. Source - What raw material do you have?
2. Intent - What output do you need?
3. Skill Selection - Which transformation applies?
4. Execution - Run the skill
5. Human Judgment - Review, refine, publish

---

## To Resume

```bash
cd "/Users/charliedeist/Desktop/New Root Docs/Creative Intelligence Agency/content-os"
claude
```

Then paste:
```
Read HANDOFF.md and continue where we left off. Priority: finalize the teaching architecture for Content OS.
```

---

## Files to Review

- `README.md` - Current user-facing documentation
- `manifest.json` - Full skill catalog
- `content-os-architecture.html` - Interactive architecture playground (open in browser)
- `scripts/install.sh` - Symlink installer

---

## Context from Lost Session

Your original prompt:
> "I want to create a Content OS repo on GitHub that collects all of my skills from across workspaces... If we could accomplish it with symlinks rather than actually duplicating all of the skills"

Key insight you had:
> "I don't want to be a total slave adherent to the PARA method... OpenEd is my salaried job, Creative Intelligence Agency is my other projects, Personal is true personal"

On capture:
> "maybe we don't go too crazy. let's rework capture system and vault structure assuming we don't want to totally reinvent the wheel"
