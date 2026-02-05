# AGENTS.md - Agent Instructions for Content OS

This file is for AI agents (Claude, etc.) that consume skills from this repository. It defines how to discover, load, route, and chain skills.

---

## Discovering Skills

Skills are stored in `skills/` as individual directories. Each directory contains a `SKILL.md` file and optional supporting resources.

**To list all available skills:**

```
ls skills/
```

**To load a skill:**

```
Read skills/{skill-name}/SKILL.md
```

**To browse programmatically:**

- `manifest.json` at the repo root contains a machine-readable index of all skills with metadata.
- Each entry includes `name`, `category`, `tier`, and `description`.

---

## Frontmatter Spec

Every SKILL.md begins with YAML frontmatter:

```yaml
---
name: skill-name          # Required. Lowercase kebab-case. Matches directory name.
version: 1.0.0            # Required. Semantic versioning.
description: When the user wants to... # Required. Trigger-based description.
---
```

### Field Details

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | Yes | Must match the directory name exactly |
| `version` | string | Yes | Follows semver (MAJOR.MINOR.PATCH) |
| `description` | string | Yes | Starts with "When the user wants to..." |

---

## Description Format

The `description` field serves two purposes:

1. **Trigger phrase:** Tells the agent when to activate this skill. Always begins with "When the user wants to..."
2. **Boundary definition:** Clarifies what the skill handles and what falls outside its scope.

### Examples

Good:
```
When the user wants to transform AI-generated text into authentic human prose, this skill provides the SUCKS framework, forbidden pattern lists, and quality checklists.
```

Bad:
```
A writing skill for making text better.
```

The description should be specific enough that an agent can decide whether to load the skill based on the user's request.

---

## Cross-Skill Routing

Some skills are related and can be chained or routed between. Follow these conventions:

### Routing Rules

1. **Check the description first.** If the user's request matches a skill's trigger phrase, load that skill.
2. **One skill at a time.** Load the most specific skill for the task. Do not load multiple skills unless explicitly chaining.
3. **Skill references.** If a SKILL.md mentions another skill by name (e.g., "For voice work, see `voice-analyzer`"), that is a routing hint. Follow it when appropriate.
4. **Fallback order.** If no single skill matches, prefer skills in this order: specific workflow > general framework > meta skill.

### Common Routing Patterns

| User Intent | Primary Skill | May Chain With |
|-------------|---------------|----------------|
| Write a blog post from a podcast | `podcast-blog-post-creator` | `human-writing`, `transcript-polisher` |
| Create YouTube content | `youtube-scriptwriting` | `youtube-title-creator`, `cold-open-creator` |
| Humanize AI text | `anti-ai-writing` | `human-writing`, `voice-matching-wizard` |
| Build a new skill | `skill-creator` | - |
| Capture a voice style | `voice-analyzer` | `voice-matching-wizard`, `voice-wizard` |
| Generate social content | `social-content-creation` | `dude-with-sign-writer`, `hook-and-headline-writing` |

---

## Chaining Skills

When a task requires multiple skills in sequence:

1. Load the first skill and complete its workflow.
2. Use the output as input for the next skill.
3. Do not load the next skill until the previous one's output is ready.
4. Respect each skill's defined scope. Do not blend instructions from multiple skills simultaneously.

### Example Chain: Podcast to Social

```
1. Load transcript-polisher     -> Clean raw transcript
2. Load podcast-blog-post-creator -> Generate blog post
3. Load social-content-creation  -> Create social posts from blog
4. Load hook-and-headline-writing -> Polish headlines
```

---

## File Structure Convention

```
skills/
  skill-name/
    SKILL.md              # Required. The skill definition and instructions.
    references/           # Optional. Supporting documents, templates, examples.
      style-guide.md
      example-output.md
    scripts/              # Optional. Automation scripts.
      process.py
      build.sh
```

### Loading Order

1. Always read `SKILL.md` first.
2. Only read files from `references/` or `scripts/` when the SKILL.md instructions direct you to.
3. Do not preload all files in a skill directory. Load on demand.

---

## Style Guide for Skill Content

When writing or editing skills, follow these conventions:

### Structure

- Begin with a brief overview (1-2 sentences) after the frontmatter.
- Include a "When to Use This Skill" section with bullet points.
- Use `---` horizontal rules to separate major sections.
- Use headers (##, ###) to organize workflows and frameworks.
- End with quality checklists or output format specifications when applicable.

### Tone

- Write as direct instructions to the agent: "Do X", "Never Y", "Always Z".
- Be specific. Vague instructions produce vague outputs.
- Include anti-patterns (what NOT to do) alongside positive instructions.

### Constraints

- Maximum 500 lines per SKILL.md.
- No hardcoded file paths, API keys, or user-specific data.
- No references to specific brands or private organizations unless the skill is explicitly about a public concept.

---

## Categories

Skills are organized into these categories:

| Category | Covers |
|----------|--------|
| `writing` | Prose, editing, humanization, style |
| `voice` | Voice analysis, matching, creation |
| `video-podcast` | YouTube, podcast production, clips |
| `content-creation` | Social media, newsletters, hooks |
| `research` | SEO, Amazon, multi-source research |
| `automation` | Workflows, pipelines, integrations |
| `design` | Visual design, branding, images |
| `meta` | Skill creation, management |
| `document-generation` | PDF, DOCX, PPTX, XLSX |
| `productivity` | Notes, search, knowledge capture |
