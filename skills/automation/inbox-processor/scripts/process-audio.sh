#!/bin/bash
# Process audio file: transcribe, summarize, suggest routing
# Usage: ./process-audio.sh <audio_file>
# Output: Creates <audio_file>.md with full analysis

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$HOME/Desktop/New Root Docs"

source "$ROOT_DIR/.env"

if [[ -z "$GEMINI_API_KEY" ]]; then
    echo "Error: GEMINI_API_KEY not set in .env"
    exit 1
fi

AUDIO_FILE="$1"

if [[ -z "$AUDIO_FILE" || ! -f "$AUDIO_FILE" ]]; then
    echo "Usage: $0 <audio_file>"
    exit 1
fi

BASENAME=$(basename "$AUDIO_FILE" | sed 's/\.[^.]*$//')
OUTPUT_DIR=$(dirname "$AUDIO_FILE")
OUTPUT_FILE="$OUTPUT_DIR/$BASENAME.md"

if [[ -f "$OUTPUT_FILE" ]]; then
    echo "Already processed: $OUTPUT_FILE"
    exit 0
fi

FILESIZE=$(stat -f%z "$AUDIO_FILE" 2>/dev/null || stat --format=%s "$AUDIO_FILE")
if [[ "$FILESIZE" -lt 1000 ]]; then
    echo "Skip (too small): $AUDIO_FILE"
    exit 0
fi

echo "Processing: $BASENAME"

# Base64 encode audio
AUDIO_BASE64=$(base64 -i "$AUDIO_FILE")

# Determine mime type
EXT="${AUDIO_FILE##*.}"
case "$EXT" in
    m4a) MIME="audio/mp4" ;;
    ogg) MIME="audio/ogg" ;;
    mp3) MIME="audio/mpeg" ;;
    wav) MIME="audio/wav" ;;
    *) MIME="audio/mp4" ;;
esac

# Single API call that does transcription + analysis
RESPONSE=$(curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -d @- << EOF
{
  "contents": [{
    "parts": [
      {
        "inline_data": {
          "mime_type": "$MIME",
          "data": "$AUDIO_BASE64"
        }
      },
      {
        "text": "Process this voice memo in the following format. Be thorough and precise.

## Summary
[2-3 sentence summary of the main points]

## Suggested Routing
Based on content, suggest the most likely project:
- opened (OpenEd, newsletter, homeschool, education content)
- skill-stack (AI skills, Claude Code, writing tools, Skill Stack)
- naval (Naval podcast, production)
- pause (meditation, MBHP, Dr. Miller)
- ray-peat (Ray Peat, metabolism, bioenergetic)
- benedict (Benedict Challenge, fasting, Vigil app, liturgy)
- jfk50 (JFK50, 50 mile march, fitness training)
- california-clm (Catholic Land Movement, CLM chapters)
- california-revival (California politics, CalTrad)
- doodle-reader (Doodle Reader, PDF, RSS)
- movement-app (Movement Meetup App)
- wiki-projects (wiki building, authorise.io)
- life-os (personal, general, unclear)

Format as:
- **Project:** [slug]
- **Action:** task | idea | reference
- **Confidence:** high | medium | low

## Action Items
Extract any explicit or implied action items as a checkbox list. If none, write 'None identified.'

## Topics Mentioned
If the note says 'new note' or clearly switches topics, list each distinct topic. Otherwise write 'Single topic.'

---

## Full Transcript (Polished)
[Clean up filler words, false starts, and interruptions while preserving 100% of the meaning and speaker's voice. Keep all substantive content.]

---

## Raw Transcript
[Verbatim transcription exactly as spoken, including ums, false starts, background voices marked as [background]. This is the source of truth.]"
      }
    ]
  }],
  "generationConfig": {
    "temperature": 0.1
  }
}
EOF
)

# Extract the response text
CONTENT=$(echo "$RESPONSE" | jq -r '.candidates[0].content.parts[0].text // empty')

if [[ -z "$CONTENT" ]]; then
    ERROR=$(echo "$RESPONSE" | jq -r '.error.message // "Unknown error"')
    echo "Error: $ERROR"
    exit 1
fi

# Get date from filename or current date
if [[ "$BASENAME" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
    FILE_DATE="${BASH_REMATCH[1]}"
else
    FILE_DATE=$(date +%Y-%m-%d)
fi

# Write output with frontmatter
cat > "$OUTPUT_FILE" << MDEOF
---
source: voice-memo
date: $FILE_DATE
status: unprocessed
original_file: $AUDIO_FILE
---

$CONTENT
MDEOF

echo "Done: $OUTPUT_FILE"
