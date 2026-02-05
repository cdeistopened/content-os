---
name: x-article-converter
version: 1.0.0
description: "When the user wants to convert blog posts or newsletters into X/Twitter articles with handles and a posting strategy. Also use when creating tweetstorms or promoting content on X with expert tagging. For broader social content, see social-content-creation."
---

# X Article Converter

Transform blog posts and newsletters into X/Twitter-ready content with handles and a posting strategy.

## Workflow

### Step 1: Identify People and Companies

Read the source article and extract all:
- Named individuals (authors, experts quoted, founders)
- Companies/organizations mentioned
- Platforms/products referenced

### Step 2: Find Twitter Handles

Use WebSearch to find Twitter/X handles for each person and company:

```
Search: "[Name] twitter" or "@[Name] site:twitter.com"
```

Create a handle reference table:

| Name | Handle | Role |
|------|--------|------|
| Justin Skycak | @justinskycak | Math Academy, quoted |

If no handle found, note "No handle found" and skip tagging.

### Step 3: Create the X Article Version

Duplicate the original article and insert handles at **first mention only**:

- Before: "Justin Skycak, Director of Analytics at Math Academy..."
- After: "@justinskycak (Justin Skycak), Director of Analytics at @_MathAcademy_..."

Keep handles natural - don't force them where they break flow.

### Step 4: Create Launch Tweet Options

Write 3 ranked tweet options for the main article launch. Each should:
- Hook with the strongest insight or stat
- Tag 1-2 key people who might RT
- Include article link
- Stay under 280 chars (or use thread format)

Rank by: likelihood of engagement from tagged people.

### Step 5: Create Weekly Posting Schedule

For each major expert/company in the article, write a standalone post:

| Day | Expert | Angle |
|-----|--------|-------|
| Mon | [Name] | [Specific insight from their quote] |
| Tue | [Name] | [Different angle] |

Each standalone post should:
- Feature one person's insight
- Tag them directly
- Stand alone without requiring the full article
- Link back to article

### Step 6: Output Files

Save to the same folder as the source article:

1. `[Article-Name]-X-Article.md` - Full article with handles
2. `[Article-Name]-Social-Assets.md` - Contains:
   - Handle reference table
   - 3 ranked launch tweets
   - Weekly posting schedule with standalone posts
   - Posting notes for handoff

## Output Format

### Social Assets File Structure

```markdown
# [Article Name] - Social Media Assets

**Article:** [link]
**Date:** [date]

**Handoff Notes:**
- [Key instruction for assistant]
- [Who agreed to RT, if any]

---

## Twitter/X Handles

| Person | Handle | Role |
|--------|--------|------|

---

## MAIN LAUNCH TWEETS (Pick One)

### #1 PICK: [Label]
> [Tweet text]

**Why this one:** [Reasoning]

---

## WEEKLY SCHEDULE

### MONDAY: [Name]
**Angle:** [What makes this post unique]

> [Tweet text]

---
```

## Keep It Simple

- One file for the X article version
- One file for posting strategy
- Handle reference table at top of both
- Clear handoff notes so assistant knows what to do

## Related Skills

- **Upstream**: **human-writing**
- **Enhanced by**: **article-titles**, **hook-and-headline-writing**
- **Feeds into**: **social-content-creation**
