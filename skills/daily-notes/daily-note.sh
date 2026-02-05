#!/bin/bash

# Daily Notes CLI
# Manages daily notes in M-D-YYYY format (e.g., 1-1-2026.md)

NOTES_DIR="${NOTES_DIR:-$HOME/.mcpclient/notes}"
mkdir -p "$NOTES_DIR"

format_date() {
    local date_str="$1"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        date -j -f "%Y-%m-%d" "$date_str" "+%-m-%-d-%Y" 2>/dev/null
    else
        date -d "$date_str" "+%-m-%-d-%Y" 2>/dev/null
    fi
}

get_date_n_days_ago() {
    local days_ago="$1"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        date -v-"${days_ago}"d "+%Y-%m-%d"
    else
        date -d "${days_ago} days ago" "+%Y-%m-%d"
    fi
}

get_today() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        date "+%-m-%-d-%Y"
    else
        date "+%-m-%-d-%Y"
    fi
}

display_note() {
    local note_file="$1"
    local note_date="$2"
    local show_header="${3:-true}"

    if [[ -f "$note_file" && -s "$note_file" ]]; then
        if [[ "$show_header" == "true" ]]; then
            echo ""
            echo "=== Notes from $note_date ==="
            echo ""
        fi
        cat "$note_file"
        if [[ "$show_header" == "true" ]]; then
            echo ""
            echo "---"
        fi
        return 0
    else
        return 1
    fi
}

cmd_get_today() {
    local TODAY=$(get_today)
    local NOTE_PATH="$NOTES_DIR/${TODAY}.md"

    if [[ ! -f "$NOTE_PATH" ]]; then
        touch "$NOTE_PATH"
        echo "Created: $NOTE_PATH" >&2
    fi

    if [[ -s "$NOTE_PATH" ]]; then
        cat "$NOTE_PATH"
    fi
}

cmd_get_note() {
    local date_input="$1"
    if [[ -z "$date_input" ]]; then
        echo "Error: Date required" >&2
        exit 1
    fi
    local NOTE_FILE="$NOTES_DIR/${date_input}.md"
    if display_note "$NOTE_FILE" "$date_input" "false"; then
        exit 0
    else
        echo "Error: No note found for date: $date_input" >&2
        exit 1
    fi
}

cmd_get_last_x() {
    local days_input="$1"
    if [[ -z "$days_input" ]]; then
        echo "Error: Duration required (e.g., 7days)" >&2
        exit 1
    fi
    local days="${days_input//[^0-9]/}"
    echo "Fetching daily notes from the last $days days..."
    echo "==========================================="
    local FOUND_NOTES=0
    for ((i=0; i<days; i++)); do
        local DATE_ISO=$(get_date_n_days_ago "$i")
        local DATE_FORMATTED=$(format_date "$DATE_ISO")
        if [[ -n "$DATE_FORMATTED" ]]; then
            local NOTE_FILE="$NOTES_DIR/${DATE_FORMATTED}.md"
            if display_note "$NOTE_FILE" "$DATE_FORMATTED"; then
                FOUND_NOTES=$((FOUND_NOTES + 1))
            fi
        fi
    done
    echo ""
    echo "Found $FOUND_NOTES note(s) from the last $days days."
}

COMMAND="${1:-}"
case "$COMMAND" in
    get-today) cmd_get_today ;;
    get-note) cmd_get_note "$2" ;;
    get-last-x) cmd_get_last_x "$2" ;;
    *)
        echo "Daily Notes CLI"
        echo "Usage: $0 <command> [arguments]"
        echo "Commands: get-today, get-note [M-D-YYYY], get-last-x [Ndays]"
        exit 1
        ;;
esac
