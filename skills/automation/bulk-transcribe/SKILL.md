---
name: bulk-transcribe
description: Agentic bulk podcast transcription using Gemini. This skill should be used when transcribing podcast episodes at scale - from a few episodes to entire catalogs of hundreds. It evaluates available sources (RSS audio preferred, then YouTube audio, then YouTube captions), transcribes samples for quality verification, generates cost quotes, and executes full transcription with checkpointing. Handles speaker identification, topic segmentation, and sponsor removal.
---

# Bulk Podcast Transcription

Agentic workflow for transcribing podcast episodes at scale using Gemini 3 Flash Preview. Codifies the full process from source evaluation through final output, with quality gates and cost transparency.

## Purpose

Transform podcast audio into clean, searchable markdown transcripts with:
- Accurate speaker identification from audio cues
- Topic segmentation with timestamped section headers
- Sponsor/ad removal
- Frontmatter metadata for indexing

## When to Use This Skill

- "Transcribe this podcast" or "I need transcripts for [podcast name]"
- Bulk transcription requests (10+ episodes)
- Building podcast wikis or searchable archives
- Any request involving podcast audio → text conversion

**Not for:** Single short audio clips, non-podcast audio, real-time transcription, or translation tasks.

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 0: Source Evaluation                                 │
│  Find optimal audio source (RSS > YouTube > VTT)            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: Sample & Quote                                    │
│  Transcribe 2 samples, gather context, generate cost quote  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    [USER APPROVAL]
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: Execute                                           │
│  Full transcription with checkpointing and progress updates │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 0: Source Evaluation

**Goal:** Identify the highest-quality audio source available.

### Step 1: Gather Podcast Information

Collect from user:
- Podcast name
- RSS feed URL (if known)
- YouTube channel URL (if known)

### Step 2: Evaluate Sources

Check sources in priority order (see `references/source-hierarchy.md`):

1. **RSS Feed with Audio**
   - Parse feed, check for `<enclosure>` tags with audio MIME type
   - If found: This is the gold standard. Use it.

2. **YouTube Channel**
   - Search for official podcast channel
   - Check video availability and match to episode titles
   - If RSS unavailable but YouTube exists: Extract audio

3. **YouTube Captions**
   - Last resort: Use auto-generated VTT files
   - Requires additional polish step for speaker diarization

### Step 3: Report Source Assessment

Present findings to user:
```
Source Assessment for [Podcast Name]

✓ RSS Feed: Found with audio enclosures (819 episodes)
  URL: https://feeds.example.com/podcast.xml
  Quality: Gold standard (direct audio)

○ YouTube: Channel found (partial coverage)
  ~600 videos matched to episodes

Recommended: Use RSS audio for all episodes

Proceed to Phase 1? [Y/n]
```

---

## Phase 1: Sample & Quote

**Goal:** Transcribe samples, gather context, generate accurate cost estimate.

### Step 1: Select Sample Episodes

Choose 2 representative episodes:
- One recent episode (current format/hosts)
- One older episode (if format may have changed)

### Step 2: Transcribe Samples

Use `scripts/transcriber.py` with the transcription prompt from `prompts/transcribe.txt`.

Key parameters:
- Model: `gemini-3-flash-preview`
- Thinking budget: 8192 (for speaker identification)
- Max output tokens: 65536
- Temperature: 0.1

### Step 3: Analyze Samples

From sample transcripts, identify:
- **Speakers**: Names, voice characteristics, roles
- **Format**: Interview, conversation, solo, mixed
- **Segments**: Recurring segments, intro/outro patterns
- **Quality**: Speaker ID accuracy, any issues

Use `prompts/analyze.txt` to structure this analysis.

### Step 4: Generate Context Config

Create podcast configuration:
```yaml
podcast_name: "My First Million"
hosts:
  - name: Sam Parr
    role: co-host
    voice_hints: "Louder, energetic, sales-focused, does sponsor reads"
  - name: Shaan Puri
    role: co-host
    voice_hints: "Calmer, analytical, usually opens episodes"
format: conversation
options:
  remove_sponsors: true
  section_headers: true
  thinking_budget: 8192
```

### Step 5: Calculate Cost Quote

Use pricing from `references/pricing.md`:

```python
# From sample transcription results
avg_input_tokens = (sample1_input + sample2_input) / 2
avg_output_tokens = (sample1_output + sample2_output) / 2

cost_per_episode = (avg_input_tokens / 1_000_000) * 1.00 + (avg_output_tokens / 1_000_000) * 3.00
total_estimate = cost_per_episode * episode_count
```

### Step 6: Present Quote for Approval

```
╭─────────────────────── Quote ───────────────────────╮
│                                                     │
│ Podcast: My First Million                           │
│ Episodes: 819                                       │
│ Avg duration: 59 min                                │
│                                                     │
│ Sample Results:                                     │
│   Speaker ID: Accurate (Sam, Shaan identified)      │
│   Section headers: 12 per episode avg               │
│   Sponsors: Removed successfully                    │
│                                                     │
│ Cost Estimate:                                      │
│   Per episode: $0.094                               │
│   Total: $77.00                                     │
│   (With batch API: $38.50)                          │
│                                                     │
│ Sample transcripts saved to: ./samples/             │
│                                                     │
│ Review samples, then approve to proceed.            │
╰─────────────────────────────────────────────────────╯

Proceed with full transcription? [Y/n]
```

**STOP HERE AND AWAIT USER APPROVAL**

---

## Phase 2: Execute

**Goal:** Transcribe all episodes with checkpointing for resume capability.

### Step 1: Initialize Job

Create manifest file for checkpointing:
```json
{
  "config": { ... },
  "episodes": [
    {"id": "ep001", "status": "pending"},
    {"id": "ep002", "status": "pending"},
    ...
  ],
  "started_at": "2026-01-21T08:00:00",
  "total_cost": 0.0
}
```

### Step 2: Process Episodes

For each pending episode:

1. **Download audio** from source URL
2. **Build prompt** with podcast context and host hints
3. **Transcribe** via Gemini with thinking mode
4. **Save transcript** as markdown with frontmatter
5. **Update manifest** with status and token counts
6. **Rate limit** wait 3-5 seconds between episodes

### Step 3: Handle Errors

On failure:
- Mark episode as "failed" in manifest
- Log error message
- Continue to next episode
- Report failed episodes at end

### Step 4: Progress Reporting

Every 10 episodes or 5 minutes:
```
Progress: 147/819 (18%)
├── Completed: 145
├── Failed: 2
├── Remaining: 672
├── Cost so far: $13.63
└── Est. remaining: $63.37

Current: "How Alex Hormozi Gets Other People to Sell"
```

### Step 5: Completion Report

```
╭───────────────── Complete ─────────────────╮
│                                            │
│ Transcribed: 817/819 episodes              │
│ Failed: 2 (see errors.log)                 │
│                                            │
│ Total cost: $76.80                         │
│ Total time: 41 hours                       │
│                                            │
│ Output: ./transcripts/                     │
│ Manifest: ./manifest.json                  │
│ Cost breakdown: ./costs.csv                │
│                                            │
╰────────────────────────────────────────────╯
```

---

## Output Format

Each transcript is a markdown file with YAML frontmatter:

```markdown
---
title: "Episode Title"
episode_id: episode_slug
source: rss-audio
speakers:
  - Sam Parr
  - Shaan Puri
  - Guest Name
topics:
  - Business
  - Startups
  - Marketing
---

[One paragraph summary]

**Topics:** Business, Startups, Marketing
**Speakers:** Sam Parr, Shaan Puri, Guest Name

---

## Section Title [00:00]

**Sam:** Opening remarks...

**Shaan:** Response...

## Next Section [05:32]

...
```

---

## Bundled Resources

### Scripts (`scripts/`)

- `transcribe_parallel.py` - Parallel Gemini audio transcription (4 workers, 3x speedup)
- `transcriber.py` - Single-threaded Gemini audio transcription
- `youtube_captions.py` - YouTube caption scraper via yt-dlp
- `polish_captions.py` - Polish YouTube captions with Gemini (add speaker ID, remove stutters)
- `rss_parser.py` - RSS feed parsing and episode extraction
- `manifest.py` - Job checkpointing and progress tracking

### Prompts (`prompts/`)

- `transcribe.txt` - Main transcription prompt with speaker ID and segmentation instructions
- `analyze.txt` - Sample analysis prompt for detecting hosts and format

### References (`references/`)

- `pricing.md` - Current Gemini pricing and cost calculation formulas
- `source-hierarchy.md` - When to use RSS vs YouTube vs VTT sources

---

## Quality Checklist

Before delivering transcripts, verify:

- [ ] Speaker names are consistent throughout
- [ ] Section headers appear every 5-10 minutes
- [ ] No sponsor reads remain in transcript
- [ ] Frontmatter metadata is complete
- [ ] No obvious transcription errors in spot-check

---

## Resuming Interrupted Jobs

If a job is interrupted:

1. Check for existing `manifest.json` in output directory
2. Load manifest to see completed/pending episodes
3. Resume from first pending episode
4. Maintain cumulative cost tracking

---

## Hybrid Strategy: Gemini + YouTube Captions

For large catalogs (500+ episodes), use a hybrid approach:

### Priority 1: Gemini Audio Transcription
- Most recent 100-200 episodes via RSS audio + Gemini
- Highest quality: accurate speaker ID, timestamps, formatting
- Cost: ~$0.07-0.10 per episode

### Priority 2: YouTube Captions + Polish
- Scrape captions via `scripts/youtube_captions.py` (free, fast)
- Polish with `scripts/polish_captions.py` (~$0.01/episode)
- Polish adds: speaker ID, section headers, stutter removal, sponsor removal
- Uses Gemini 3 Flash Preview with thinking (4096 budget)
- Output: 70-90% of input length (cleanup, not summarization)

### Upgrade Path
As budget allows, replace placeholders with Gemini transcripts:
1. Run `--skip-existing` to only transcribe non-Gemini episodes
2. System automatically skips episodes with existing high-quality transcripts
3. Placeholders are replaced in-place

### When to Use Hybrid
- Large back catalogs (500+ episodes)
- Limited budget (want searchable content now, quality later)
- Time-sensitive projects (get wiki up quickly)

---

## Environment Requirements

- `GEMINI_API_KEY` - Google Gemini API key
- Python 3.9+ with: `google-genai`, `python-dotenv`

---

*This skill codifies the full bulk transcription workflow. Execute phases in order, always await user approval before Phase 2.*
