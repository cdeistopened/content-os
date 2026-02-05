# Google Gemini Integration

Large language model with 1M+ token context and image generation capabilities.

## Setup

1. Get an API key at [makersuite.google.com](https://makersuite.google.com)
2. Set environment variable:
   ```bash
   export GEMINI_API_KEY=your-key-here
   ```

## Used By

- **nano-banana-image-generator** — AI image generation via Gemini's image capabilities
- **pdf-ocr** — OCR and text extraction from PDFs using Gemini's vision
- **image-prompt-generator** — Generate editorial images

## Models

| Model | Best For | Context |
|-------|----------|---------|
| gemini-2.0-flash | Fast tasks, image gen | 1M tokens |
| gemini-2.5-pro | Complex reasoning, analysis | 1M tokens |

## Rate Limits

Free tier: 15 RPM, 1M tokens/min, 1500 requests/day.
Paid tier: Higher limits via Google Cloud.
