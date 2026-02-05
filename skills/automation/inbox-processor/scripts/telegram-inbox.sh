#!/bin/bash
# Poll Telegram bot for new messages and save to inbox
# Usage: ./telegram-inbox.sh [--daemon]
#   --daemon: Run continuously, polling every 30 seconds

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$HOME/Desktop/New Root Docs"
INBOX_DIR="$ROOT_DIR/Life OS/inbox"
VOICE_DIR="$ROOT_DIR/Life OS/inbox/audio"
STATE_FILE="$SCRIPT_DIR/.telegram-offset"
LOG_FILE="$SCRIPT_DIR/.telegram-inbox.log"
OPENED_IDEAS_DIR="$ROOT_DIR/OpenEd Vault/Studio/OpenEd Daily/ideas"

# Logging function with timestamps
log() {
    local level="$1"
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" | tee -a "$LOG_FILE"
}

log_error() { log "ERROR" "$@"; }
log_info() { log "INFO" "$@"; }
log_debug() { log "DEBUG" "$@"; }

# Keep log file from growing too large (last 1000 lines)
if [[ -f "$LOG_FILE" ]] && [[ $(wc -l < "$LOG_FILE") -gt 2000 ]]; then
    tail -1000 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
fi

source "$ROOT_DIR/.env"

if [[ -z "$TELEGRAM_BOT_TOKEN" ]]; then
    echo "Error: TELEGRAM_BOT_TOKEN not set in .env"
    exit 1
fi

if [[ -z "$GEMINI_API_KEY" ]]; then
    echo "Error: GEMINI_API_KEY not set in .env"
    exit 1
fi

TELEGRAM_API="https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN"

# Get last processed offset
get_offset() {
    if [[ -f "$STATE_FILE" ]]; then
        cat "$STATE_FILE"
    else
        echo "0"
    fi
}

# Save offset for next run
save_offset() {
    echo "$1" > "$STATE_FILE"
}

# Download file from Telegram
download_telegram_file() {
    local file_id="$1"
    local output_path="$2"

    # Get file path from Telegram
    local file_info=$(curl -s "$TELEGRAM_API/getFile?file_id=$file_id")
    local file_path=$(echo "$file_info" | jq -r '.result.file_path // empty')

    if [[ -z "$file_path" ]]; then
        echo "Error: Could not get file path for $file_id"
        return 1
    fi

    # Download the file
    curl -s "https://api.telegram.org/file/bot$TELEGRAM_BOT_TOKEN/$file_path" -o "$output_path"
    echo "Downloaded: $output_path"
}

# Transcribe audio using Gemini
transcribe_audio() {
    local audio_file="$1"

    local audio_base64=$(base64 -i "$audio_file")

    local response=$(curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=$GEMINI_API_KEY" \
        -H 'Content-Type: application/json' \
        -d @- << EOF
{
  "contents": [{
    "parts": [
      {
        "inline_data": {
          "mime_type": "audio/ogg",
          "data": "$audio_base64"
        }
      },
      {
        "text": "Transcribe this voice message. Return ONLY the transcription, no commentary. If unclear, note [inaudible]."
      }
    ]
  }],
  "generationConfig": {
    "temperature": 0.1
  }
}
EOF
    )

    echo "$response" | jq -r '.candidates[0].content.parts[0].text // "[transcription failed]"'
}

# Fetch URL content and metadata
fetch_url_content() {
    local url="$1"

    # Use Gemini to fetch and summarize the URL
    local response=$(curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=$GEMINI_API_KEY" \
        -H 'Content-Type: application/json' \
        -d @- << EOF
{
  "contents": [{
    "parts": [{
      "text": "Fetch and analyze this URL: $url\n\nReturn JSON only:\n{\n  \"title\": \"article title\",\n  \"outlet\": \"publication name\",\n  \"author\": \"author name or null\",\n  \"date_published\": \"YYYY-MM-DD or null\",\n  \"summary\": \"2-3 sentence summary\",\n  \"content_type\": \"thought|tool|trend|deep-dive|article-source\",\n  \"project\": \"project-slug from registry below\",\n  \"key_points\": [\"point 1\", \"point 2\", \"point 3\"]\n}\n\nPROJECT REGISTRY (match content to best fit):\n- opened: Education, homeschooling, alternative education, schools, learning, parenting\n- skill-stack: AI, Claude, LLMs, prompts, skills, Claude Code, agents, automation\n- benedict: Fasting, Liturgy of Hours, Catholic spirituality, prayer\n- jfk50: 50 mile march, walking, endurance, fitness challenges\n- naval: Naval Ravikant, podcasts, wisdom, philosophy\n- pause: Meditation, mindfulness\n- ray-peat: Ray Peat, metabolism, nutrition, health research, bioenergetics\n- california-clm: Catholic Land Movement, distributism, agrarianism\n- california-revival: California politics, culture\n- life-os: Personal/general (default if unclear)\n\nContent types:\n- thought: brief insight, opinion piece, hot take\n- tool: tool, resource, app, curriculum\n- trend: news, policy, statistics\n- deep-dive: long-form research, guide\n- article-source: general article for repurposing"
    }]
  }],
  "generationConfig": {
    "temperature": 0.2,
    "response_mime_type": "application/json"
  }
}
EOF
    )

    echo "$response" | jq -r '.candidates[0].content.parts[0].text // "{}"'
}

# Generate schematic from photo using Gemini image API
generate_schematic() {
    local input_image="$1"
    local prompt="$2"
    local output_dir="$3"
    local timestamp="$4"

    local output_file="$output_dir/schematic_${timestamp}.png"

    # Encode image to base64
    local image_base64=$(base64 -i "$input_image")
    local mime_type="image/jpeg"

    # Determine mime type from extension
    if [[ "$input_image" == *.png ]]; then
        mime_type="image/png"
    elif [[ "$input_image" == *.webp ]]; then
        mime_type="image/webp"
    fi

    # Call Gemini with image + prompt for schematic generation
    local response=$(curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$GEMINI_API_KEY" \
        -H 'Content-Type: application/json' \
        -d @- << EOF
{
  "contents": [{
    "parts": [
      {
        "inline_data": {
          "mime_type": "$mime_type",
          "data": "$image_base64"
        }
      },
      {
        "text": "$prompt"
      }
    ]
  }],
  "generationConfig": {
    "temperature": 0.7,
    "response_modalities": ["TEXT", "IMAGE"]
  }
}
EOF
    )

    # Extract image from response if present
    local image_data=$(echo "$response" | jq -r '.candidates[0].content.parts[] | select(.inline_data != null) | .inline_data.data // empty' | head -1)

    if [[ -n "$image_data" ]]; then
        # Decode and save the image
        echo "$image_data" | base64 -d > "$output_file"
        echo "$output_file"
    else
        # Log error
        local error_msg=$(echo "$response" | jq -r '.error.message // .candidates[0].content.parts[0].text // "Unknown error"')
        log_error "Schematic generation failed: $error_msg"
        echo ""
    fi
}

# Route content with Claude (via Gemini for now - can swap later)
suggest_routing() {
    local content="$1"

    local response=$(curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=$GEMINI_API_KEY" \
        -H 'Content-Type: application/json' \
        -d @- << EOF
{
  "contents": [{
    "parts": [{
      "text": "Analyze this note and suggest routing to the appropriate project. Return JSON only:\n{\n  \"project\": \"project-slug\",\n  \"action\": \"task|idea|reference|archive\",\n  \"tags\": [\"tag1\", \"tag2\"],\n  \"title\": \"short title\",\n  \"is_todo\": true/false\n}\n\nPROJECT REGISTRY (match content to the best fit):\n- opened: Education, homeschooling, alternative education, schools, learning, parenting\n- skill-stack: AI, Claude, LLMs, prompts, skills, Claude Code, agents, automation\n- benedict: Fasting, Liturgy of Hours, Vigil app, Catholic spirituality, prayer\n- jfk50: 50 mile march, walking, endurance, fitness challenges, RFK\n- naval: Naval Ravikant, podcasts, wisdom, philosophy\n- pause: Meditation, mindfulness, contemplation\n- ray-peat: Ray Peat, metabolism, nutrition, health research, bioenergetics\n- california-clm: Catholic Land Movement, distributism, agrarianism, rural life\n- california-revival: California politics, culture, state policy\n- clm-publishing: Cross & Plough magazine, Rural Prayer Life\n- doodle-reader: PDF tools, transcription, RSS feeds\n- spiral: AI writing tools, wizard patterns\n- gemini-writer: Long-form autonomous writing\n- life-os: Personal goals, priorities, general notes (default if unclear)\n\nIf it mentions a feature request, bug, or to-do item, set is_todo=true.\nIf genuinely unclear which project, use life-os.\n\nContent:\n$content"
    }]
  }],
  "generationConfig": {
    "temperature": 0.2,
    "response_mime_type": "application/json"
  }
}
EOF
    )

    echo "$response" | jq -r '.candidates[0].content.parts[0].text // "{}"'
}

# Process a single message
process_message() {
    local message="$1"
    local timestamp=$(date +%Y-%m-%d_%H-%M-%S)
    local date_only=$(date +%Y-%m-%d)

    # Extract message details
    local text=$(echo "$message" | jq -r '.text // empty')
    local voice=$(echo "$message" | jq -r '.voice // empty')
    local audio=$(echo "$message" | jq -r '.audio // empty')
    local photo=$(echo "$message" | jq -r '.photo // empty')
    local caption=$(echo "$message" | jq -r '.caption // empty')
    local from_user=$(echo "$message" | jq -r '.from.first_name // "Unknown"')

    # Handle voice messages
    if [[ -n "$voice" && "$voice" != "null" ]]; then
        echo "Processing voice message..."
        local file_id=$(echo "$message" | jq -r '.voice.file_id')
        local duration=$(echo "$message" | jq -r '.voice.duration')
        local audio_file="$VOICE_DIR/telegram_${timestamp}.ogg"

        mkdir -p "$VOICE_DIR"
        download_telegram_file "$file_id" "$audio_file"

        echo "Transcribing with Gemini..."
        local transcript=$(transcribe_audio "$audio_file")

        echo "Suggesting routing..."
        local routing=$(suggest_routing "$transcript")
        local title=$(echo "$routing" | jq -r '.title // "Voice Note"')
        local project=$(echo "$routing" | jq -r '.project // "null"')
        local action=$(echo "$routing" | jq -r '.action // "idea"')
        local tags=$(echo "$routing" | jq -r '.tags // []')

        # Create markdown file
        local safe_title=$(echo "$title" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g' | cut -c1-50)
        local output_file="$INBOX_DIR/${date_only}-telegram-${safe_title}.md"

        cat > "$output_file" << MDEOF
---
source: telegram-voice
date: $date_only
title: $title
project: $project
action: $action
tags: $(echo "$tags" | jq -c '.')
duration: ${duration}s
status: unprocessed
---

## Transcript

$transcript

---
*Voice note received via Telegram at $timestamp*
MDEOF

        echo "Saved: $output_file"
        return 0
    fi

    # Handle photo messages (convert to schematic)
    if [[ -n "$photo" && "$photo" != "null" && "$photo" != "[]" ]]; then
        echo "Processing photo message..."

        # Get the largest photo (last in array)
        local file_id=$(echo "$message" | jq -r '.photo[-1].file_id')
        local photo_file="$VOICE_DIR/telegram_photo_${timestamp}.jpg"
        local schematic_output="$INBOX_DIR/schematics"

        mkdir -p "$VOICE_DIR"
        mkdir -p "$schematic_output"

        download_telegram_file "$file_id" "$photo_file"

        if [[ -f "$photo_file" ]]; then
            echo "Generating schematic with Gemini..."

            # Check if caption requests schematic (or default to schematic)
            local schematic_prompt="Convert this image into a clean technical schematic illustration. GOAL: Recreate the essential forms and structure as a simplified black and white diagram. STYLE: Technical schematic. Pure black lines on white background. No gradients, no shading except minimal hatching for depth. Uniform line weight. Patent illustration quality. COMPOSITION: 8.5x11 portrait orientation. Center the subject with generous white margins. SIMPLIFICATION: Distill to essential geometric forms. Remove photorealistic detail, texture, and color. Keep only what's necessary to identify the subject. OUTPUT: Clean black and white schematic suitable for technical documentation. AVOID: Gradients, gray tones, artistic flourishes, decorative elements, photorealism."

            # If caption has custom instructions, use those instead
            if [[ -n "$caption" && "$caption" != "null" ]]; then
                schematic_prompt="$caption. Convert to clean technical schematic: pure black lines on white, simplified geometric forms, 8.5x11 format."
            fi

            # Generate schematic using Gemini image API
            local schematic_file=$(generate_schematic "$photo_file" "$schematic_prompt" "$schematic_output" "$timestamp")

            if [[ -n "$schematic_file" && -f "$schematic_file" ]]; then
                echo "Schematic saved: $schematic_file"

                # Create markdown reference
                local output_file="$INBOX_DIR/${date_only}-telegram-schematic.md"
                cat > "$output_file" << MDEOF
---
source: telegram-photo
date: $date_only
title: Schematic from photo
type: schematic
original: $photo_file
schematic: $schematic_file
status: generated
---

## Schematic Generated

Original photo converted to technical schematic.

- **Original:** $photo_file
- **Schematic:** $schematic_file
- **Caption:** ${caption:-"(none)"}

---
*Photo received via Telegram at $timestamp*
MDEOF
                echo "Saved: $output_file"
            else
                echo "Schematic generation failed"
            fi
        fi
        return 0
    fi

    # Handle text messages
    if [[ -n "$text" && "$text" != "/start" ]]; then
        echo "Processing text message..."

        # Check if it's a URL
        local url=$(echo "$text" | grep -oE 'https?://[^ ]+' | head -1)

        if [[ -n "$url" ]]; then
            echo "Detected URL: $url"
            echo "Fetching URL content..."
            local url_data=$(fetch_url_content "$url")

            local article_title=$(echo "$url_data" | jq -r '.title // "Untitled"')
            local outlet=$(echo "$url_data" | jq -r '.outlet // "Unknown"')
            local author=$(echo "$url_data" | jq -r '.author // null')
            local date_published=$(echo "$url_data" | jq -r '.date_published // null')
            local summary=$(echo "$url_data" | jq -r '.summary // ""')
            local content_type=$(echo "$url_data" | jq -r '.content_type // "article-source"')
            local project=$(echo "$url_data" | jq -r '.project // "life-os"')
            local key_points=$(echo "$url_data" | jq -r '.key_points // []')

            local safe_title=$(echo "$article_title" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g' | cut -c1-50)

            # Route everything to inbox (project suggestion saved in frontmatter)
            echo "Detected project: $project (routing to inbox for manual review)"
            local output_file="$INBOX_DIR/${date_only}-telegram-${safe_title}.md"

            cat > "$output_file" << MDEOF
---
source: telegram-link
date: $date_only
title: $article_title
url: $url
outlet: $outlet
author: $author
date_published: $date_published
content_type: $content_type
project: $project
status: unprocessed
---

## Summary

$summary

## Key Points

$(echo "$key_points" | jq -r '.[] | "- " + .')

## Context

$text

---
*Link shared via Telegram at $timestamp*
MDEOF

            echo "Saved: $output_file"
            return 0
        else
            # Regular text - check for todos
            local routing=$(suggest_routing "$text")
            local title=$(echo "$routing" | jq -r '.title // "Note"')
            local project=$(echo "$routing" | jq -r '.project // "null"')
            local action=$(echo "$routing" | jq -r '.action // "idea"')
            local tags=$(echo "$routing" | jq -r '.tags // []')
            local is_todo=$(echo "$routing" | jq -r '.is_todo // false')

            local safe_title=$(echo "$title" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g' | cut -c1-50)
            local output_file="$INBOX_DIR/${date_only}-telegram-${safe_title}.md"

            if [[ "$is_todo" == "true" ]]; then
                action="task"
            fi

            cat > "$output_file" << MDEOF
---
source: telegram-text
date: $date_only
title: $title
project: $project
action: $action
tags: $(echo "$tags" | jq -c '.')
status: unprocessed
---

$text

---
*Received via Telegram at $timestamp*
MDEOF

            echo "Saved: $output_file"
            return 0
        fi
    fi

    echo "Skipped message (no processable content)"
}

# Main polling function
poll_telegram() {
    local offset=$(get_offset)

    log_info "Polling Telegram (offset: $offset)..."

    local response=$(curl -s --max-time 30 "$TELEGRAM_API/getUpdates?offset=$offset&timeout=5")

    if [[ -z "$response" ]]; then
        log_error "Empty response from Telegram API (network issue?)"
        return 1
    fi

    local ok=$(echo "$response" | jq -r '.ok')

    if [[ "$ok" != "true" ]]; then
        log_error "Telegram API error: $(echo "$response" | jq -r '.description // "Unknown error"')"
        return 1
    fi

    local count=$(echo "$response" | jq '.result | length')

    if [[ "$count" -eq 0 ]]; then
        log_info "No new messages"
        return 0
    fi

    log_info "Found $count new update(s)"

    # Process each update
    echo "$response" | jq -c '.result[]' | while read -r update; do
        local update_id=$(echo "$update" | jq -r '.update_id')
        local message=$(echo "$update" | jq -r '.message // empty')

        if [[ -n "$message" && "$message" != "null" ]]; then
            log_debug "Processing update $update_id"
            if ! process_message "$message"; then
                log_error "Failed to process update $update_id"
            fi
        fi

        # Save offset (next update_id)
        save_offset $((update_id + 1))
        log_debug "Saved offset: $((update_id + 1))"
    done

    log_info "Done processing"
}

# Daemon mode
run_daemon() {
    log_info "Starting Telegram inbox daemon (Ctrl+C to stop)..."
    while true; do
        poll_telegram || log_error "Poll failed, will retry..."
        sleep 30
    done
}

# Main
mkdir -p "$INBOX_DIR"

if [[ "$1" == "--daemon" ]]; then
    run_daemon
else
    poll_telegram
fi
