#!/bin/bash
# Extract Authors từ Unknown-Author PDFs - Production Batch Script
# Usage: ./extract-authors-batch.sh [max_files]
# Default: 15 files, Set to process larger batch

set -euo pipefail

# Configuration
DKM_PATH="/home/fong/Projects/mini-rag/DKM-PDFs"
LOG_FILE="/home/fong/Projects/mini-rag/.fong/.memory/author-extraction-batch.log"
TEMP_DIR="/tmp/author_extraction_$$"
MAX_FILES="${1:-15}"
PROCESSED=0
SUCCESS=0
SKIPPED=0
FAILED=0

# Ensure directories exist
mkdir -p "$TEMP_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🚀 Starting batch extraction (max $MAX_FILES files)"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] DKM Path: $DKM_PATH" >> "$LOG_FILE"

# Function: Extract author from text
extract_author() {
    local text="$1"
    local author=""

    # Pattern 1: All-caps author names (Priority 1 - NEW)
    # Matches: "A. G. SVESHNOKOV. A. N. TIKHONOV"
    author=$(echo "$text" | grep -E '^[A-Z]\. [A-Z]\. [A-Z][A-Z]+' | head -1 | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')

    if [ -n "$author" ] && [ ${#author} -gt 2 ]; then
        echo "$author"
        return 0
    fi

    # Pattern 2: Copyright line (Priority 2)
    # Matches: "© 2013 V. Galitski, B. Karnakov, V. Kogan, V. Galitski Jr."
    author=$(echo "$text" | grep -iE '©|copyright' | head -1 | sed -E 's/.*©[^0-9]*[0-9]{4}[^A-Z]*//; s/^[[:space:]]*//; s/[[:space:]]*$//' | head -c 80)

    if [ -n "$author" ] && [ ${#author} -gt 2 ]; then
        echo "$author"
        return 0
    fi

    # Pattern 3: Author keyword (Priority 3)
    # Matches: "by D. Huybrechts", "Author: Michael Reed"
    author=$(echo "$text" | grep -iE '^[[:space:]]*(by|author:)[[:space:]]+' | head -1 | sed -E 's/^[[:space:]]*(by|author:)[[:space:]]*//i; s/^[[:space:]]*//; s/[[:space:]]*$//' | head -c 80)

    if [ -n "$author" ] && [ ${#author} -gt 2 ]; then
        echo "$author"
        return 0
    fi

    # Pattern 4: Title page author - with dots (Priority 4)
    # Matches: "A. G. Sveshnokov", "Michael Reed Barry Simon"
    author=$(echo "$text" | grep -E '^[A-Z]\. [A-Z]\. [A-Za-z]+|^[A-Z][a-zA-Z]+ ([A-Z][a-zA-Z]+ )*[A-Z][a-zA-Z]+$' | head -1 | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')

    if [ -n "$author" ] && [ ${#author} -gt 2 ]; then
        echo "$author"
        return 0
    fi

    # Pattern 5: Department/Institution (Priority 5)
    # Matches: "Michael Reed\nDepartment of Mathematics"
    author=$(echo "$text" | grep -B1 -iE 'department|faculty|institute' | head -1 | sed 's/^[[:space:]]*//; s/[[:space:]]*$//' | grep -E '^[A-Z][a-zA-Z]+')

    if [ -n "$author" ] && [ ${#author} -gt 2 ]; then
        echo "$author"
        return 0
    fi

    echo ""
}

# Function: Format author name (Last-First)
format_author() {
    local author="$1"

    # Remove titles and suffixes
    author=$(echo "$author" | sed -E 's/\b(Dr\.|Prof\.|Mr\.|Ms\.|Mrs\.|Sir|Lady)\b//g')
    author=$(echo "$author" | sed -E 's/\b(Jr\.|Sr\.|II|III|IV|V)\b//g')
    author=$(echo "$author" | xargs)  # Trim whitespace

    # Handle "A. G. SVESHNOKOV. A. N. TIKHONOV" format (dots as separators)
    # Convert dots followed by space to commas for splitting
    if [[ $author =~ ^[A-Z]\.[[:space:]][A-Z]\. ]]; then
        # Extract all last names from "A. G. LASTNAME. B. H. LASTNAME" pattern
        local lastname_parts=()
        while [[ $author =~ ([A-Z]+)\.?[[:space:]]*$ ]]; do
            author="${author%${BASH_REMATCH[0]}}"
        done

        # Better approach: extract capitals after dots
        local names=$(echo "$author" | grep -oE '[A-Z][A-Z]+' | head -4)

        local formatted=""
        local count=0
        while IFS= read -r name; do
            if [ $count -ge 3 ]; then break; fi
            if [ -n "$name" ] && [ ${#name} -gt 2 ]; then
                if [ -z "$formatted" ]; then
                    formatted="$name"
                else
                    formatted="${formatted}_${name}"
                fi
                count=$((count + 1))
            fi
        done <<< "$names"

        if [ -n "$formatted" ]; then
            echo "$formatted"
            return 0
        fi
    fi

    # Split by comma or "and"
    IFS=',' read -ra NAMES <<< "$author"

    local formatted=""
    local count=0

    for name in "${NAMES[@]}"; do
        # Skip if count > 3 (max 3 authors)
        if [ $count -ge 3 ]; then
            break
        fi

        name=$(echo "$name" | sed 's/ and /,/g' | xargs)

        # Try to extract Last-First pattern
        if [[ $name =~ ^([A-Za-z\-]+),?[[:space:]]*(.*)$ ]]; then
            local last="${BASH_REMATCH[1]}"
            local first="${BASH_REMATCH[2]}"

            first=$(echo "$first" | xargs)

            # If has first name, use Last-First format
            if [ -n "$first" ]; then
                if [ -z "$formatted" ]; then
                    formatted="${last}-${first}"
                else
                    formatted="${formatted}_${last}-${first}"
                fi
            else
                # Single name, just use it
                if [ -z "$formatted" ]; then
                    formatted="$last"
                else
                    formatted="${formatted}_${last}"
                fi
            fi
            count=$((count + 1))
        fi
    done

    # If no pattern matched, use original with underscore
    if [ -z "$formatted" ]; then
        formatted=$(echo "$author" | head -c 60 | sed 's/ /_/g')
    fi

    echo "$formatted"
}

# Function: Process single file
process_file() {
    local file="$1"
    local filepath="$DKM_PATH/$file"

    # Extract text from first 5 pages
    local text_file="$TEMP_DIR/text_$((PROCESSED+1)).txt"

    if ! pdftotext -f 1 -l 5 "$filepath" "$text_file" 2>/dev/null; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ FAILED: $file (corrupted PDF)"
        echo "$(date '+%Y%m%d-%H%M%S') FAILED $file (corrupted)" >> "$LOG_FILE"
        FAILED=$((FAILED + 1))
        return 1
    fi

    local text_len=$(wc -c < "$text_file")

    # Check if text is too short (< 50 chars)
    if [ "$text_len" -lt 50 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  SKIP: $file (text too short: $text_len bytes)"
        echo "$(date '+%Y%m%d-%H%M%S') SKIP $file (text < 50 chars)" >> "$LOG_FILE"
        SKIPPED=$((SKIPPED + 1))
        return 1
    fi

    # Extract author
    local author=$(extract_author "$(cat "$text_file")")

    if [ -z "$author" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  SKIP: $file (no author found)"
        echo "$(date '+%Y%m%d-%H%M%S') SKIP $file (no author detected)" >> "$LOG_FILE"
        SKIPPED=$((SKIPPED + 1))
        return 1
    fi

    # Format author
    local formatted_author=$(format_author "$author")

    # Extract year from filename or text
    local year=$(echo "$file" | grep -oE '^[0-9]{4}' || echo "UNKNOWN")

    # Extract title (remove year and Unknown-Author suffix)
    local title=$(basename "$file" .PDF | sed 's/^[0-9]*-//' | sed 's/-Unknown-Author.*//' | sed 's/-anonymous.*//')

    # Validate
    if [ ${#formatted_author} -gt 60 ]; then
        formatted_author=$(echo "$formatted_author" | cut -c1-60)
    fi

    # Build new filename
    local new_name="${year}-${title}-${formatted_author}.PDF"

    # Check if filename is too long (> 255 chars)
    if [ ${#new_name} -gt 255 ]; then
        formatted_author=$(echo "$formatted_author" | cut -c1-40)
        new_name="${year}-${title}-${formatted_author}.PDF"
    fi

    # Rename file
    if [ "$new_name" != "$file" ]; then
        if mv "$filepath" "$DKM_PATH/$new_name" 2>/dev/null; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ SUCCESS: $file → $new_name"
            echo "$(date '+%Y%m%d-%H%M%S') SUCCESS $file → $new_name" >> "$LOG_FILE"
            SUCCESS=$((SUCCESS + 1))
            return 0
        else
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ FAILED: $file (rename error)"
            echo "$(date '+%Y%m%d-%H%M%S') FAILED $file (rename error)" >> "$LOG_FILE"
            FAILED=$((FAILED + 1))
            return 1
        fi
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  SKIP: $file (already named correctly)"
        SKIPPED=$((SKIPPED + 1))
        return 1
    fi
}

# Main loop
cd "$DKM_PATH"
for file in *.PDF; do
    # Check if max files reached
    if [ $PROCESSED -ge $MAX_FILES ]; then
        break
    fi

    # Skip if not Unknown-Author
    if ! echo "$file" | grep -qiE '(Unknown-Author|anonymous)'; then
        continue
    fi

    PROCESSED=$((PROCESSED + 1))
    process_file "$file" || true  # Continue even if file is skipped or fails
done

# Summary
echo ""
echo "=== BATCH EXTRACTION SUMMARY ==="
echo "Total Processed: $PROCESSED files"
echo "Success: $SUCCESS"
echo "Skipped: $SKIPPED"
echo "Failed: $FAILED"
echo "Success Rate: $(( SUCCESS * 100 / (PROCESSED > 0 ? PROCESSED : 1) ))%"
echo ""
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Batch complete. Results: $SUCCESS/$PROCESSED success"

# Cleanup
rm -rf "$TEMP_DIR"

exit 0
