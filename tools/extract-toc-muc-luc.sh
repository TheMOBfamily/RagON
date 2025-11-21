#!/usr/bin/env bash
# Extract Table of Contents from PDFs with heuristics and caching.
# Usage: extract-toc-muc-luc.sh [pdf_directory] (defaults to /home/fong/Projects/mini-rag/DKM-PDFs)
# Env:
#   MAX_FILES=N        limit processed files (testing)
#   RUN_TS=YYYYmmdd-HHMMSS  override run timestamp for log name
#   FORCE=1            re-generate even if cache exists
set -euo pipefail

ROOT="/home/fong/Projects/mini-rag"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"
RUN_TS="${RUN_TS:-$(date -u +%Y%m%d-%H%M%S)}"
LOG_FILE="$LOG_DIR/extract-toc-$RUN_TS.log"
log() { printf '%s %s\n' "$(date -u +%FT%TZ)" "$*" | tee -a "$LOG_FILE" >&2; }

DEFAULT_DIR="/home/fong/Projects/mini-rag/DKM-PDFs"
# If arg provided use it; otherwise default to DKM-PDFs
if [ $# -ge 1 ]; then
  PDF_DIR="$1"
else
  PDF_DIR="$DEFAULT_DIR"
fi
[ -d "$PDF_DIR" ] || { echo "Directory not found: $PDF_DIR" >&2; exit 1; }

need_tools=(pdfinfo pdftotext)
for t in "${need_tools[@]}"; do
  if ! command -v "$t" >/dev/null 2>&1; then
    log "[FATAL] missing tool: $t (install poppler-utils)"
    exit 2
  fi
done
HAS_PDFTK=0
if command -v pdftk >/dev/null 2>&1; then HAS_PDFTK=1; fi

ANCHOR_REGEX='Table of Contents|Contents|Mục lục|Muc luc|TOC|Indice|Index|Contenido|Sommaire|Sumário'
TMP_DIR="$(mktemp -d)"; trap 'rm -rf "$TMP_DIR"' EXIT

process_pdf() {
  local pdf="$1"; local idx="$2"; local total="$3"
  local base md5 out_dir out_file pages_total limit
  base="$(basename "$pdf")"
  md5="$(md5sum "$pdf" | awk '{print $1}')"
  out_dir="$PDF_DIR/$md5"
  out_file="$out_dir/index.md"
  mkdir -p "$out_dir"
  if [ -f "$out_file" ] && [ "${FORCE:-0}" = "0" ]; then
    log "[$idx/$total][SKIP] exists: $out_file"
    return 0
  fi
  pages_total="$(pdfinfo "$pdf" 2>/dev/null | awk '/^Pages:/ {print $2}')" || pages_total=""
  if ! [[ "$pages_total" =~ ^[0-9]+$ ]]; then pages_total=30; fi
  limit=$(( pages_total / 10 ))
  [ $limit -lt 30 ] && limit=30
  [ $limit -gt 60 ] && limit=60
  [ $pages_total -lt $limit ] && limit=$pages_total

  # 1) Try outlines via pdftk if available
  if [ $HAS_PDFTK -eq 1 ]; then
    local outline_tmp="$TMP_DIR/outline.txt"; : > "$outline_tmp"
    if pdftk "$pdf" dump_data 2>/dev/null | awk '/^BookmarkTitle: /{title=substr($0,16)} /^BookmarkPageNumber: /{page=$2; if(title!="" && page!=""){printf("- %s .... %s\n", title, page); title=""}}' > "$outline_tmp"; then
      if [ -s "$outline_tmp" ]; then
        log "[$idx/$total][OK] outlines detected via pdftk: $base"
        {
          printf '# TOC for %s\n\n' "$base"
          printf 'Source file hash: %s\nDetected via: pdftk outlines\n\n' "$md5"
          echo '## Extracted Entries'
          cat "$outline_tmp"
        } > "$out_file"
        log "[$idx/$total][OK] TOC written: $out_file (outlines)"
        return 0
      fi
    fi
  fi

  # 2) Heuristic scan of front matter
  declare -a page_scores; declare -a page_anchors
  local p text anchor score
  for ((p=1; p<=limit; p++)); do
    text="$(pdftotext -layout -f $p -l $p "$pdf" - 2>/dev/null || true)"
    anchor=0; score=0
    while IFS= read -r line; do
      [ -z "$line" ] && continue
      if echo "$line" | grep -Eiq "$ANCHOR_REGEX"; then anchor=1; fi
      if echo "$line" | grep -Eq '.{8,}\.{2,}[[:space:]]*[0-9]{1,4}[[:space:]]*$'; then score=$((score+1)); continue; fi
      if echo "$line" | grep -Eq '^(Chapter[[:space:]][0-9]+|[IVXLCM]{1,4}\.|[0-9]+(\.[0-9]+){0,3})[[:space:]]+.{3,}[[:space:]][0-9]{1,4}[[:space:]]*$'; then score=$((score+1)); continue; fi
    done <<<"$text"
    page_scores[$p]=$score
    page_anchors[$p]=$anchor
  done

  local start=0 end zeros=0
  for ((p=1; p<=limit; p++)); do
    if [ ${page_anchors[$p]:-0} -eq 1 ] || [ ${page_scores[$p]:-0} -ge 5 ]; then start=$p; break; fi
  done
  if [ $start -eq 0 ]; then
    local best_sum=0 best_idx=1 w
    for ((p=1; p<=limit-2; p++)); do
      w=$(( ${page_scores[$p]:-0} + ${page_scores[$((p+1))]:-0} + ${page_scores[$((p+2))]:-0} ))
      if [ $w -gt $best_sum ]; then best_sum=$w; best_idx=$p; fi
    done
    if [ $best_sum -ge 6 ]; then start=$best_idx; fi
  fi

  local toc_lines_file="$TMP_DIR/toc_lines.txt"; : > "$toc_lines_file"
  if [ $start -gt 0 ]; then
    end=$start; zeros=0
    for ((p=start; p<=limit; p++)); do
      if [ ${page_scores[$p]:-0} -gt 0 ]; then end=$p; zeros=0; else zeros=$((zeros+1)); fi
      [ $zeros -ge 2 ] && break
    done
    for ((p=start; p<=end; p++)); do
      text="$(pdftotext -layout -f $p -l $p "$pdf" - 2>/dev/null || true)"
      while IFS= read -r line; do
        [ -z "$line" ] && continue
        if echo "$line" | grep -Eiq "$ANCHOR_REGEX" \
           || echo "$line" | grep -Eq '.{8,}\.{2,}[[:space:]]*[0-9]{1,4}[[:space:]]*$' \
           || echo "$line" | grep -Eq '^(Chapter[[:space:]][0-9]+|[IVXLCM]{1,4}\.|[0-9]+(\.[0-9]+){0,3})[[:space:]]+.{3,}[[:space:]][0-9]{1,4}[[:space:]]*$'; then
          echo "$line" >> "$toc_lines_file"
        fi
      done <<<"$text"
    done
  fi

  # 3) Manual-like fallback from raw text if no lines detected
  if [ ! -s "$toc_lines_file" ]; then
    log "[$idx/$total][WARN] No explicit TOC; applying text fallback: $base"
    local raw_tmp="$TMP_DIR/raw.txt"; : > "$raw_tmp"
    # scan first up to 20 pages for candidate headings
    local scan_pages=$(( pages_total < 20 ? pages_total : 20 ))
    pdftotext -layout -f 1 -l "$scan_pages" "$pdf" "$raw_tmp" 2>/dev/null || true
    if [ -s "$raw_tmp" ]; then
      # Heuristic: uppercase titles, numbered headings without trailing page
      awk '
        function trim(s){gsub(/^\s+|\s+$/,"",s); return s}
        {
          line=trim($0); if(length(line)<4) next;
          if (line ~ /^[[:upper:][:digit:][:space:][:punct:]]+$/ && length(line)<=80) print line; 
          else if (line ~ /^[0-9]+(\.[0-9]+){0,3}[[:space:]]+[A-Za-z].{3,}$/) print line;
          else if (line ~ /^Chapter[[:space:]][0-9]+[[:space:]]+/) print line;
        }' "$raw_tmp" | awk 'NR<=120' | sed '/^[[:space:]]*$/d' | uniq > "$toc_lines_file"
    fi
  fi

  # Prepare output
  local start_text half
  if [ ${start:-0} -gt 0 ]; then
    start_text="$(pdftotext -layout -f $start -l $start "$pdf" - 2>/dev/null || true)"
  else
    start_text="$(pdftotext -layout -f 1 -l 1 "$pdf" - 2>/dev/null || true)"
  fi
  mapfile -t start_lines <<<"$start_text" || true
  half=$(( ${#start_lines[@]} / 2 ))

  {
    printf '# TOC for %s\n\n' "$base"
    if [ $start -gt 0 ]; then
      printf 'Source file hash: %s\nDetected TOC pages: %d-%d (scanned first %d pages)\n\n' "$md5" "$start" "${end:-start}" "$limit"
    else
      printf 'Source file hash: %s\nDetected via: text fallback (no TOC pages)\n\n' "$md5"
    fi
    if [ -s "$toc_lines_file" ]; then
      echo '## Extracted Entries'
      sort -u "$toc_lines_file"
    else
      echo 'No structured TOC lines detected.'
    fi
    echo ''
    echo '---'
    echo '## Extra Context (first half of start page)'
    for ((i=0; i<half; i++)); do
      line="${start_lines[$i]:-}"
      [ -n "$line" ] && echo "$line"
    done
  } > "$out_file"
  log "[$idx/$total][OK] TOC written: $out_file (pages ${start:-0}-${end:-0})"
}

# Iterate PDFs
mapfile -d '' pdfs < <(find "$PDF_DIR" -maxdepth 1 -type f -iname '*.pdf' -print0 | sort -z)
TOTAL=${#pdfs[@]}
log "Starting TOC extraction for $TOTAL PDFs in $PDF_DIR; log: $LOG_FILE"
count=0
for pdf in "${pdfs[@]}"; do
  count=$((count+1))
  if [ -n "${MAX_FILES:-}" ] && [ "$count" -gt "${MAX_FILES}" ]; then break; fi
  process_pdf "$pdf" "$count" "$TOTAL" || log "[$count/$TOTAL][ERR] failed: $(basename "$pdf")"
done
log "Finished."
