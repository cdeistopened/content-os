#!/bin/bash
# Voice Memos Extraction Script
# Extracts recent voice memos, converts .qta to .m4a, organizes by date

set -e

# Configuration
SOURCE_DIR="$HOME/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings"
DB_PATH="$SOURCE_DIR/CloudRecordings.db"
DEST_DIR="$HOME/Desktop/New Root Docs/Life OS/Voice Memos/inbox"
LIMIT=${1:-50}  # Default to 50 most recent

# Ensure destination exists
mkdir -p "$DEST_DIR"

echo "Extracting $LIMIT most recent voice memos..."
echo "Source: $SOURCE_DIR"
echo "Destination: $DEST_DIR"
echo ""

# Query database for recent recordings
# ZDATE is Core Data timestamp (seconds since 2001-01-01)
# Add 978307200 to convert to Unix timestamp
sqlite3 "$DB_PATH" "
SELECT 
    ZPATH,
    ZCUSTOMLABEL,
    ZDATE,
    ZDURATION
FROM ZCLOUDRECORDING 
ORDER BY ZDATE DESC 
LIMIT $LIMIT;
" | while IFS='|' read -r filename label coredata_ts duration; do
    
    # Skip if file doesn't exist
    if [[ ! -f "$SOURCE_DIR/$filename" ]]; then
        echo "SKIP (not found): $filename"
        continue
    fi
    
    # Convert Core Data timestamp to Unix timestamp
    unix_ts=$(echo "$coredata_ts + 978307200" | bc)
    unix_ts_int=${unix_ts%.*}
    
    # Format date for filename: YYYY-MM-DD_HH-MM
    formatted_date=$(date -r "$unix_ts_int" +"%Y-%m-%d_%H-%M")
    
    # Clean up label for filename (remove special chars, truncate)
    if [[ -n "$label" && "$label" != "null" ]]; then
        # Extract title if it's an ISO timestamp format, otherwise use the label
        if [[ "$label" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T ]]; then
            clean_label=""
        else
            clean_label=$(echo "$label" | tr -cd '[:alnum:] _-' | head -c 50 | xargs)
        fi
    else
        clean_label=""
    fi
    
    # Build output filename
    if [[ -n "$clean_label" ]]; then
        out_name="${formatted_date}_${clean_label}.m4a"
    else
        out_name="${formatted_date}.m4a"
    fi
    
    # Replace spaces with underscores
    out_name=$(echo "$out_name" | tr ' ' '_')
    
    out_path="$DEST_DIR/$out_name"
    
    # Skip if already processed
    if [[ -f "$out_path" ]]; then
        echo "EXISTS: $out_name"
        continue
    fi
    
    # Convert .qta files using afconvert, copy .m4a files directly
    ext="${filename##*.}"
    if [[ "$ext" == "qta" ]]; then
        echo "CONVERT: $filename → $out_name"
        afconvert -f m4af -d aac "$SOURCE_DIR/$filename" "$out_path" 2>/dev/null
    else
        echo "COPY: $filename → $out_name"
        cp "$SOURCE_DIR/$filename" "$out_path"
    fi
    
    # Set file timestamps to original recording time
    touch -t $(date -r "$unix_ts_int" +"%Y%m%d%H%M.%S") "$out_path"
    
done

echo ""
echo "Done! Files in: $DEST_DIR"
ls -la "$DEST_DIR" | head -20
