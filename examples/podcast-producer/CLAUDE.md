# Podcast Producer Workspace

> A workspace for podcast production, from raw recording to published episode with supporting content.

## Where Things Live

| What | Location |
|------|----------|
| **Raw recordings** | `recordings/` |
| **Transcripts** | `transcripts/` |
| **Show notes** | `episodes/` |
| **Blog posts** | `blog/` |
| **Clips** | `clips/` |
| **Skills** | `.claude/skills/` |

## Quick Reference

| Key | Value |
|-----|-------|
| **Podcast Name** | [Your Podcast] |
| **Host** | [Your Name] |
| **Format** | [Interview/Solo/Panel] |
| **Length** | [30min/60min/etc] |

## Production Workflow

Use the `podcast-production` skill for the full workflow:

```
/podcast-production
```

This guides you through 4 checkpoints:
1. **Pre-production** - Guest research, question prep
2. **Post-recording** - Transcript review, highlight marking
3. **Content creation** - Show notes, clips, blog post
4. **Publishing** - Descriptions, social posts

## Skills Quick Reference

| Task | Skill |
|------|-------|
| Full production | `podcast-production` |
| Clean transcript | `transcript-polisher` |
| Episode blog post | `podcast-blog-post-creator` |
| Cold open | `cold-open-creator` |
| YouTube title | `youtube-title-creator` |
| Social clips | `youtube-clip-extractor` |
| Headlines | `hook-and-headline-writing` |

## Episode Template

```markdown
# Episode [NUMBER]: [TITLE]

**Guest:** [Name, Title]
**Recorded:** [Date]
**Published:** [Date]

## Summary
[2-3 sentences]

## Key Topics
- Topic 1 (timestamp)
- Topic 2 (timestamp)

## Notable Quotes
> "Quote here" - Guest

## Resources Mentioned
- [Resource 1](link)

## Clips Created
- [ ] Clip 1: [topic]
- [ ] Clip 2: [topic]
```

## Content Multiplication

From each episode, create:
- [ ] Polished transcript
- [ ] Blog post (use `podcast-blog-post-creator`)
- [ ] 3-5 short clips (use `youtube-clip-extractor`)
- [ ] Newsletter section
- [ ] Social posts (use `social-content-creation`)

---

*Customize this workspace for your specific podcast.*
