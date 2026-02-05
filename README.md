# Content OS

> 93 skills for AI-assisted content creation, automation, and development. Transform, don't generate.

Content OS is a collection of Claude Code skills for writers, podcasters, developers, and content creators. Each skill is a self-contained markdown file that teaches Claude how to perform a specific task.

## Quick Start

```bash
git clone https://github.com/cdeistopened/content-os.git
cd content-os
./scripts/install.sh
```

The installer prompts you to choose which skill categories to install.

## Skill Categories

### Writing (14 skills)
Core skills for human-sounding prose.

| Skill | Description |
|-------|-------------|
| `anti-ai-writing` | Eliminate AI tells and write authentically |
| `ai-tells` | Detect and fix AI writing patterns |
| `ghostwriter` | Transform source material into polished prose |
| `human-writing` | Comprehensive human writing system |
| `writing-style` | Charlie Deist's signature style rules |
| `hook-and-headline-writing` | Create compelling hooks and headlines |
| `cold-open-creator` | Write attention-grabbing cold opens |
| `transcript-polisher` | Clean transcripts while preserving voice |
| `email-writing` | Professional email composition |
| `memo` | Write effective memos |
| `dude-with-sign-writer` | Punchy sign-style statements |
| `voice-pirate-wires` | Pirate Wires editorial voice |
| `invisible-threads` | [Custom writing skill] |
| `verified-review` | Write authentic reviews |

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

### Newsletter (5 skills)
Newsletter writing and production.

| Skill | Description |
|-------|-------------|
| `skill-stack-newsletter-writer` | Newsletter template |
| `opened-daily-newsletter-writer` | Daily format example |
| `opened-weekly-newsletter-writer` | Weekly format example |
| `opened-daily-style` | Daily newsletter style guide |
| `how-newsletters` | Newsletter strategy and tactics |

### Social (6 skills)
Social media content and advertising.

| Skill | Description |
|-------|-------------|
| `social-content-creation` | Multi-platform social content |
| `x-article-converter` | Convert articles to X threads |
| `x-posting` | X/Twitter posting workflows |
| `text-content` | General text content |
| `meta-ads-creative` | Meta/Facebook ad creative |
| `twitter-scraper` | Twitter data extraction |

### Brand & Voice (5 skills)
Capture and codify identity and voice.

| Skill | Description |
|-------|-------------|
| `brand-identity-wizard` | Interactive brand capture |
| `voice-matching-wizard` | Codify a writer's voice |
| `voice-analyzer` | Analyze writing samples |
| `opened-identity` | Brand identity example |
| `guidelines-brand` | Brand guidelines example |

### Research (4 skills)
SEO and knowledge management.

| Skill | Description |
|-------|-------------|
| `seo-research` | Keyword research workflows |
| `seo-content-writer` | SEO-optimized content |
| `notebooklm` | Google NotebookLM integration |
| `open-education-hub-deep-dives` | Deep dive research |

### Automation (6 skills)
Tool integration and automation.

| Skill | Description |
|-------|-------------|
| `agent-browser` | Browser automation |
| `bulk-transcribe` | Batch transcription |
| `gemini-writer` | Gemini API integration |
| `inbox-processor` | Email/inbox processing |
| `pdf-ocr` | PDF text extraction |
| `slack-cli` | Slack CLI integration |

### Design (8 skills)
UI/UX and mobile design.

| Skill | Description |
|-------|-------------|
| `ui-ux-pro-max` | Comprehensive UI/UX design |
| `front-end-design` | Frontend design patterns |
| `design-stealer` | Design inspiration extraction |
| `expo-ios-designing` | Expo/React Native iOS design |
| `iOS Expert` | iOS development expertise |
| `ios-simulator-skill-main` | iOS simulator workflows |
| `theme-factory` | Theme/design system creation |
| `webapp-testing` | Web application testing |

### Notion (4 skills)
Notion integration and workflows.

| Skill | Description |
|-------|-------------|
| `notion-knowledge-capture` | Capture knowledge to Notion |
| `notion-meeting-intelligence` | Meeting notes to Notion |
| `notion-research-documentation` | Research documentation |
| `notion-spec-to-implementation` | Specs to code via Notion |

### Canvas (4 skills)
Claude canvas and artifact skills.

| Skill | Description |
|-------|-------------|
| `canvas` | Canvas artifact creation |
| `document` | Document artifacts |
| `calendar` | Calendar artifacts |
| `flight` | Flight planning artifacts |

### Cursor (5 skills)
Cursor IDE specific skills.

| Skill | Description |
|-------|-------------|
| `create-skill` | Create new Cursor skills |
| `create-rule` | Create Cursor rules |
| `create-subagent` | Create Cursor subagents |
| `migrate-to-skills` | Migrate to skills format |
| `update-cursor-settings` | Manage Cursor settings |

### Productivity (6 skills)
Personal productivity and review.

| Skill | Description |
|-------|-------------|
| `weekly-review` | Weekly review workflow |
| `pre-mortem` | Pre-mortem analysis |
| `remindctl` | Reminder management |
| `vellum-prep` | Vellum preparation |
| `bird` | [Custom productivity skill] |
| `gog` | [Custom productivity skill] |

### Meta (4 skills)
Skills for creating skills.

| Skill | Description |
|-------|-------------|
| `skill-creator` | Create new skills from scratch |
| `skill-installer` | Install and manage skills |
| `quality-loop` | Quality assurance workflow |
| `image-prompt-generator` | AI image generation prompts |

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
2. Copy example skills (like `opened-identity`) as templates
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

*Built by [Charlie Deist](https://skillstack.md) for the Skill Stack community.*
