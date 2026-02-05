# Audio Source Hierarchy

When transcribing a podcast, evaluate available sources in this order. Use the highest-quality source available.

## Source Ranking

### 1. RSS Feed with Audio Enclosures (Gold Standard)

**Quality:** Highest
**Why:** Direct audio from publisher, full quality, no intermediary processing

**Detection:**
```python
# Check for audio enclosure in RSS
enclosure = item.find('enclosure')
if enclosure and 'audio' in enclosure.get('type', ''):
    return enclosure.get('url')
```

**Advantages:**
- Original audio quality
- No rate limits or scraping issues
- Direct from source
- Gemini transcription with speaker diarization

**Typical sources:**
- Podcast RSS feeds (Apple Podcasts, Spotify, etc.)
- Megaphone, Transistor, Anchor hosted feeds

---

### 2. YouTube Audio Extraction (Second Best)

**Quality:** High
**Why:** Audio track from video, good quality but requires extraction step

**Detection:**
- Check if podcast has YouTube channel
- Match episode titles to YouTube videos
- Use Apify YouTube scraper or yt-dlp

**Extraction methods:**
1. **Apify YouTube Scraper** - Automated, handles rate limits
2. **yt-dlp** - Local extraction: `yt-dlp -x --audio-format mp3 <url>`

**Advantages:**
- Often available when RSS lacks audio
- Video podcasts captured fully
- Can match to RSS metadata

**Disadvantages:**
- Requires extraction step
- May have different editing than audio-only release
- Rate limit concerns at scale

---

### 3. YouTube Auto-Captions/VTT (Third Best)

**Quality:** Medium
**Why:** Pre-transcribed but lower quality than Gemini-from-audio

**Detection:**
```python
# yt-dlp can extract subtitles
yt-dlp --write-auto-sub --sub-lang en --skip-download <url>
```

**When to use:**
- No audio source available
- Very large catalogs where cost is prohibitive
- Quick/rough transcripts acceptable

**Post-processing required:**
- Speaker diarization (not included in auto-captions)
- Timestamp alignment
- Error correction via Gemini polish step

**Advantages:**
- Fastest (no transcription needed)
- Cheapest (text polish only)
- Good for initial pass

**Disadvantages:**
- No speaker identification
- More errors than audio transcription
- Missing content if no captions available

---

## Source Evaluation Workflow

```
1. Check RSS feed for audio enclosures
   ├── Found → Use RSS audio (Gold Standard)
   └── Not found → Continue

2. Search for YouTube channel/videos
   ├── Found → Check video availability
   │   ├── Videos available → Extract audio (Second Best)
   │   └── Only some videos → Mix sources
   └── Not found → Continue

3. Check for existing transcripts
   ├── YouTube auto-captions available → Use VTT + polish (Third Best)
   └── No captions → Manual transcription required
```

## Quality vs. Cost Tradeoffs

| Source | Quality | Cost/Episode | Best For |
|--------|---------|--------------|----------|
| RSS Audio | Excellent | ~$0.10 | Production quality, speaker ID critical |
| YouTube Audio | Very Good | ~$0.12 | When RSS unavailable |
| YouTube VTT | Good | ~$0.02 | Large catalogs, rough drafts |

## Mixing Sources

For incomplete catalogs, mix sources intelligently:
1. Use RSS audio for episodes that have it
2. Fall back to YouTube for missing episodes
3. Use VTT for very old episodes if cost is a concern

Track source in frontmatter:
```yaml
---
source: rss-audio | youtube-audio | youtube-vtt-polished
---
```
