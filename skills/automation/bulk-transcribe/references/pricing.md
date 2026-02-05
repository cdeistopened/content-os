# Gemini Transcription Pricing

*Last updated: January 2026*

## Gemini 3 Flash Preview

| Token Type | Price per 1M Tokens |
|------------|---------------------|
| Audio Input | $1.00 |
| Text Input | $0.50 |
| Text Output | $3.00 |

### Cost Calculation Formula

```
episode_cost = (audio_tokens / 1,000,000) * $1.00 + (output_tokens / 1,000,000) * $3.00
```

### Typical Episode Costs

Based on empirical testing:

| Episode Length | Audio Tokens | Output Tokens | Estimated Cost |
|----------------|--------------|---------------|----------------|
| 30 min | ~45,000 | ~8,000 | ~$0.07 |
| 60 min | ~90,000 | ~18,000 | ~$0.14 |
| 90 min | ~135,000 | ~25,000 | ~$0.21 |

**Rule of thumb:** ~$0.10 per hour of audio

### Batch API Discount

Using Gemini's batch API provides a **50% discount** on all token costs.

| Pricing Mode | 60-min Episode Cost |
|--------------|---------------------|
| Standard | ~$0.14 |
| Batch API | ~$0.07 |

### Cost Estimation for Full Catalogs

```python
def estimate_catalog_cost(episode_count: int, avg_duration_minutes: int = 60) -> float:
    """Estimate cost for transcribing a full podcast catalog."""
    cost_per_hour = 0.10  # Standard pricing
    hours_per_episode = avg_duration_minutes / 60
    return episode_count * hours_per_episode * cost_per_hour
```

**Examples:**
- 100 episodes × 60 min avg = ~$10
- 500 episodes × 45 min avg = ~$37.50
- 819 episodes × 59 min avg = ~$77

### Token Counting

Audio tokenization rate: ~25 tokens per second of audio
- 1 minute = ~1,500 tokens
- 1 hour = ~90,000 tokens

Output tokens vary by content density but typically:
- ~200-300 output tokens per minute of audio
- ~15,000-20,000 output tokens per hour

### Source

- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- Empirical testing on My First Million podcast (January 2026)
