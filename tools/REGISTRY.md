# Tools Registry

External tools and services referenced by Content OS skills. Install what you need for the skills you use.

---

## CLI Tools

| Tool | Used By | Install | Purpose |
|------|---------|---------|---------|
| **yt-dlp** | youtube-downloader, youtube-clip-extractor, twitter-scraper | `brew install yt-dlp` | Download video/audio from YouTube and other platforms |
| **ffmpeg** | youtube-clip-extractor, video-caption-creation, short-form-video | `brew install ffmpeg` | Video/audio processing, clipping, format conversion |
| **whisper** | transcript-polisher, twitter-scraper | `pip install openai-whisper` | Speech-to-text transcription |
| **pandoc** | vellum-prep, docx | `brew install pandoc` | Document format conversion |
| **python3** | nano-banana-image-generator, semantic-chunking-rules, podcast-wiki-pipeline | Pre-installed on macOS | Script execution |

## APIs & Services

| Service | Used By | Auth | Purpose |
|---------|---------|------|---------|
| **Google Gemini** | nano-banana-image-generator, pdf-ocr, image-prompt-generator | `GEMINI_API_KEY` | Image generation, OCR, large document processing |
| **Google Veo** | video-generator | `GOOGLE_API_KEY` | AI video generation |
| **DataForSEO** | seo-research (if added) | `DATAFORSEO_LOGIN` + `DATAFORSEO_PASSWORD` | Keyword research, SERP analysis |
| **Notion API** | notion-* skills | `NOTION_TOKEN` | Knowledge capture, meeting prep, research docs |
| **X/Twitter API** | x-article-converter | Account credentials | Post conversion |

## Desktop Apps

| App | Used By | Purpose |
|-----|---------|---------|
| **Vellum** | vellum-prep | Book formatting (macOS) |
| **Remotion** | remotion-video (if added) | Programmatic video in React |

## MCP Servers

| Server | Used By | Purpose |
|--------|---------|---------|
| **Slack MCP** | slack-gif-creator | Slack integration |
| **Notion MCP** | notion-* skills | Notion workspace access |

---

## Setup by Tier

### Tier 1 (No Setup)
Most Tier 1 skills work with zero external dependencies. They're pure instruction sets.

### Tier 2 (Light Setup)
Some Tier 2 skills need a CLI tool:
- `brew install yt-dlp` for YouTube skills
- `brew install ffmpeg` for video editing skills

### Tier 3 (API Keys)
Power User skills often need API access:
- Gemini API key for image/OCR skills
- Notion token for productivity skills
- DataForSEO credentials for SEO skills

---

See `integrations/` for per-tool setup guides.
