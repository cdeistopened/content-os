#!/bin/bash
# Transcribe a single voice memo using Gemini API
# Usage: ./transcribe-voice-memo.sh <audio_file.m4a>
# Output: Creates <audio_file>.md alongside the audio

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
    echo "Usage: $0 <audio_file.m4a>"
    exit 1
fi

BASENAME=$(basename "$AUDIO_FILE" .m4a)
OUTPUT_DIR=$(dirname "$AUDIO_FILE")
OUTPUT_FILE="$OUTPUT_DIR/$BASENAME.md"

if [[ -f "$OUTPUT_FILE" ]]; then
    echo "Already transcribed: $OUTPUT_FILE"
    exit 0
fi

FILESIZE=$(stat -f%z "$AUDIO_FILE")
if [[ "$FILESIZE" -lt 1000 ]]; then
    echo "Skip (too small, likely empty): $AUDIO_FILE"
    echo "---" > "$OUTPUT_FILE"
    echo "status: skipped" >> "$OUTPUT_FILE"
    echo "reason: file too small (${FILESIZE} bytes)" >> "$OUTPUT_FILE"
    echo "---" >> "$OUTPUT_FILE"
    exit 0
fi

echo "Transcribing: $BASENAME"

AUDIO_BASE64=$(base64 -i "$AUDIO_FILE")

RESPONSE=$(curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=$GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -d @- << EOF
{
  "contents": [{
    "parts": [
      {
        "inline_data": {
          "mime_type": "audio/mp4",
          "data": "$AUDIO_BASE64"
        }
      },
      {
        "text": "Transcribe this audio recording verbatim. Return ONLY the transcription, no commentary or labels. If there are multiple speakers, indicate speaker changes with [Speaker 1], [Speaker 2], etc. If the audio is unclear or empty, just say '[inaudible]' or '[no speech detected]'."
      }
    ]
  }],
  "generationConfig": {
    "temperature": 0.1
  }
}
EOF
)

TRANSCRIPT=$(echo "$RESPONSE" | jq -r '.candidates[0].content.parts[0].text // empty')

if [[ -z "$TRANSCRIPT" ]]; then
    ERROR=$(echo "$RESPONSE" | jq -r '.error.message // "Unknown error"')
    echo "Error transcribing $BASENAME: $ERROR"
    echo "---" > "$OUTPUT_FILE"
    echo "status: error" >> "$OUTPUT_FILE"
    echo "error: $ERROR" >> "$OUTPUT_FILE"
    echo "---" >> "$OUTPUT_FILE"
    exit 1
fi

cat > "$OUTPUT_FILE" << MDEOF
---
source: voice-memo
date: $BASENAME
status: raw
---

## Transcript

$TRANSCRIPT
MDEOF

echo "Done: $OUTPUT_FILE"
