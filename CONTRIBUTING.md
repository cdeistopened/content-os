# Contributing to Content OS

Thank you for your interest in contributing to Content OS. This guide covers everything you need to know to add a new skill or improve an existing one.

## Adding a New Skill

### 1. Create the Directory Structure

Every skill lives in its own directory under `skills/`. The directory name must match the skill name in the frontmatter.

```
skills/
  your-skill-name/
    SKILL.md          # Required - the skill definition
    references/       # Optional - supporting documents, examples, templates
    scripts/          # Optional - automation scripts (Python, Bash, etc.)
```

### 2. Naming Rules

- **Lowercase kebab-case only:** `my-great-skill`, not `MyGreatSkill` or `my_great_skill`
- **Directory name = skill name:** The directory name must exactly match the `name` field in the SKILL.md frontmatter
- **Be descriptive:** Prefer `youtube-title-creator` over `yt-titles`
- **No brand names:** Skills should be generic. Use `voice-contrarian` instead of `voice-specific-publication`

### 3. SKILL.md Format

Every SKILL.md must follow this structure:

```markdown
---
name: your-skill-name
version: 1.0.0
description: When the user wants to [do something specific], this skill provides [what it provides]. Use when [trigger conditions].
---

# Skill Title

Brief overview of what this skill does and why it exists.

## When to Use This Skill

- Trigger condition 1
- Trigger condition 2
- Trigger condition 3

---

## [Workflow / Framework / Instructions]

The body of your skill. Include:
- Step-by-step workflows
- Templates and frameworks
- Examples and anti-patterns
- Quality checklists
```

### Frontmatter Requirements

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase kebab-case, matches directory name |
| `version` | Yes | Semantic version (e.g., `1.0.0`) |
| `description` | Yes | Must start with "When the user wants to..." |

### Content Guidelines

- **Under 500 lines.** If your skill exceeds this, split it into a core SKILL.md and supporting files in `references/`.
- **Description starts with a trigger phrase.** The description tells Claude when to activate the skill: "When the user wants to..."
- **No hardcoded paths or credentials.** Skills must be portable across machines and users.
- **No brand-specific content.** Remove references to specific companies, products, or people unless the skill is explicitly about a public figure or concept.
- **References go in `references/`.** Supporting documents, style guides, example outputs.
- **Scripts go in `scripts/`.** Python, Bash, or other automation scripts the skill depends on.

---

## Pull Request Process

### Before Submitting

Run through this quality checklist:

- [ ] Directory name matches the `name` field in SKILL.md frontmatter
- [ ] SKILL.md has valid YAML frontmatter with `name`, `version`, and `description`
- [ ] Description starts with "When the user wants to..."
- [ ] SKILL.md is under 500 lines
- [ ] No hardcoded file paths, API keys, or credentials
- [ ] No brand-specific or private content
- [ ] Skill has been tested in Claude Code (loaded and used end-to-end)
- [ ] References are in `references/` subdirectory (if applicable)
- [ ] Scripts are in `scripts/` subdirectory (if applicable)

### PR Template

When opening a pull request, use this format in the PR description:

```markdown
## New Skill: [skill-name]

**Category:** [writing | voice | video-podcast | content-creation | research | automation | design | meta | document-generation | productivity]

**Description:** [One sentence explaining what this skill does]

### Checklist

- [ ] SKILL.md has valid frontmatter (name, version, description)
- [ ] Description starts with "When the user wants to..."
- [ ] Under 500 lines
- [ ] No hardcoded paths or credentials
- [ ] No brand-specific content
- [ ] Tested in Claude Code

### What does this skill do?

[2-3 sentences explaining the use case and what makes this skill valuable]

### How was it tested?

[Describe how you loaded the skill in Claude Code and what tasks you ran]
```

---

## Requesting a New Skill

If you have an idea for a skill but do not want to build it yourself, open a GitHub issue using this format:

```markdown
**Title:** Skill Request: [descriptive-name]

## What should this skill do?

[Describe the task or workflow this skill would handle]

## When would someone use it?

[Describe the trigger conditions - what situation makes this skill useful]

## Example input/output

[If possible, provide an example of what you would give Claude and what you would expect back]

## Category

[writing | voice | video-podcast | content-creation | research | automation | design | meta | document-generation | productivity]
```

---

## Improving Existing Skills

Improvements to existing skills are welcome. Common improvements include:

- Adding missing examples or templates
- Fixing broken workflows
- Improving clarity of instructions
- Adding references or scripts that enhance the skill
- Reducing line count while preserving functionality

When submitting improvements, describe what changed and why in your PR description.

---

## Code of Conduct

Be constructive. Skills are meant to help people create better content. Keep contributions focused, tested, and portable.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
