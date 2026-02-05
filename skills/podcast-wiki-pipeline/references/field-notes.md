# Field Notes (Pipeline Learnings)

## What works
- Manifest-driven runs with per-item status allow resumes after failure.
- Small batches (2-5) avoid timeouts and rate limits.
- Overlap-aware caption merge is essential for YouTube auto-captions.
- Timestamp markers every ~60 seconds balance citation and readability.
- Keep raw VTT and cues.json to rebuild markdown without re-fetching.

## What breaks
- Long-lived loops without checkpoints time out.
- Naive VTT -> text creates duplicate lines.

## Operational defaults
- Batch size: 5
- Marker cadence: 60 seconds
- Chunk size: 500-1500 words
- Status flow: pending -> done | skipped | needs_stt
