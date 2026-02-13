# Content OS

> 36 skills for AI-assisted content creation. Transform, don't generate.

Content OS is a collection of Claude Code skills for writers, podcasters, and content creators. Each skill is a self-contained markdown file that teaches Claude how to perform a specific task.

## Quick Start

```bash
git clone https://github.com/cdeistopened/content-os.git
cd content-os
./scripts/install.sh
```

The installer prompts you to choose which skill categories to install.

## Skill Categories

### Writing (15 skills)
Core skills for human-sounding prose.

| Skill | Description |
|-------|-------------|
| `anti-ai-writing` | Eliminate AI tells and write authentically |
| `ai-tells` | Detect and fix AI writing patterns |
| `ghostwriter` | Transform source material into polished prose |
| `human-writing` | Comprehensive human writing system |
| `writing-style` | Core anti-AI patterns for all writing |
| `hook-and-headline-writing` | Create compelling hooks and headlines |
| `cold-open-creator` | Write attention-grabbing cold opens |
| `transcript-polisher` | Clean transcripts while preserving voice |
| `email-writing` | Professional email composition |
| `memo` | Write effective memos |
| `dude-with-sign-writer` | Punchy sign-style statements |
| `voice-pirate-wires` | Pirate Wires editorial voice |
| `invisible-threads` | Narrative threading technique |
| `verified-review` | Write authentic reviews |
| `how-newsletters` | Newsletter strategy and tactics |

### Video & Podcast (9 skills)
Production workflows for audio/video content.

| Skill | Description |
|-------|-------------|
| `podcast-production` | Full production workflow with checkpoints |
| `podcast-blog-post-creator` | Turn episodes into blog posts |
| `youtube-scriptwriting` | Write YouTube scripts |
| `youtube-clip-extractor` | Extract and repurpose clips |
| `youtube-downloader` | Download videos and transcripts |
| `youtube-title-creator` | Click-worthy titles |
| `video-caption-creation` | Captions and subtitles |
| `short-form-video` | Short-form video content |
| `day-in-the-life` | Day-in-the-life video format |

### Social (5 skills)
Social media content and advertising.

| Skill | Description |
|-------|-------------|
| `social-content-creation` | Multi-platform social content |
| `x-article-converter` | Convert articles to X threads |
| `x-posting` | X/Twitter posting and scheduling |
| `text-content` | General text content |
| `meta-ads-creative` | Meta/Facebook ad creative |

### Research (4 skills)
SEO and knowledge management.

| Skill | Description |
|-------|-------------|
| `seo-research` | Keyword research workflows |
| `seo-content-writer` | SEO-optimized content |
| `notebooklm` | Google NotebookLM integration |
| `open-education-hub-deep-dives` | Deep dive research |

### Content (1 skill)
Content generation and image creation.

| Skill | Description |
|-------|-------------|
| `nano-banana-image-generator` | AI image generation with Gemini |

### Productivity (2 skills)
Personal productivity and strategic tools.

| Skill | Description |
|-------|-------------|
| `find-your-margin` | Find where your attention earns the fattest margin with AI |
| `vellum-prep` | Vellum book preparation |

## Using Skills

Once installed, invoke skills in Claude Code:

```
/skill-name
```

Or reference them in your CLAUDE.md:

```markdown
## Writing Guidelines
Always load `skills/anti-ai-writing/SKILL.md` for any writing task.
```

## Customizing

1. Fork this repo
2. Copy example skills as templates
3. Replace brand-specific content with your own
4. Create a CLAUDE.md for your workspace using `CLAUDE.md.template`

## Philosophy

**Transform, Don't Generate.** AI refines human ideas, not replaces them.

The 4S Framework:
- **Source** - Your raw material (transcripts, notes, research)
- **Substance** - The core insight you're expressing
- **Structure** - The format that best delivers your message
- **Style** - Your distinctive voice

## License

MIT

---

*Built by [Charlie Deist](https://skillstack.ai) for the Skill Stack community.*
