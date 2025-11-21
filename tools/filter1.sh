#!/bin/bash
# filter1.sh - Convert non-PDF ebooks, archive originals, dedupe, and drop files already in DKM-PDFs.
# Usage: ./filter1.sh <folder> [dkm_folder]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load environment from .env (portable)
source "$SCRIPT_DIR/../load-env.sh"

usage() {
  echo "Usage: $0 <folder> [dkm_folder]"
  echo "  <folder>: Source folder containing PDFs/ebooks"
  echo "  [dkm_folder]: Defaults to \$DKM_PDF_PATH ($DKM_PDF_PATH)"
}

die() {
  echo "❌ $1" >&2
  exit 1
}

[ $# -ge 1 ] || { usage; exit 1; }

TARGET_DIR="${1%/}"
DKM_DIR="${2:-$DKM_PDF_PATH}"

SKIP_ALREADY_EXISTS=0
[ -d "$TARGET_DIR" ] || die "Target folder not found: $TARGET_DIR"
[ -d "$DKM_DIR" ] || die "DKM folder not found: $DKM_DIR"

if ! command -v ebook-convert >/dev/null 2>&1; then
  die "ebook-convert (Calibre CLI) is required. Install Calibre before running filter1."
fi

LOG_DIR="${LOG_DIR:-$RAGON_ROOT/logs}"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/filter1-$(date +%Y%m%d-%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1
echo "# filter1.sh run: $(date --iso-8601=seconds)"
echo "# Logging to: $LOG_FILE"

# Ensure Calibre can run headless
export QT_QPA_PLATFORM=offscreen
export QTWEBENGINE_DISABLE_SANDBOX=1
export QT_OPENGL=software

for required in sha256sum find sort pandoc wkhtmltopdf; do
  command -v "$required" >/dev/null 2>&1 || die "$required is required but not found"
done

OLD_DIR="$TARGET_DIR/_old"
ORIG_DIR="$OLD_DIR/originals"
DUP_DIR="$OLD_DIR/duplicates"
DKM_DUP_DIR="$OLD_DIR/dkm_matches"
mkdir -p "$ORIG_DIR" "$DUP_DIR" "$DKM_DUP_DIR"

safe_move() {
  local src="$1" dest_dir="$2" base dest counter extension stem
  base="$(basename "$src")"
  if [[ "$base" == *.* ]]; then
    extension=".${base##*.}"
    stem="${base%.*}"
  else
    extension=""
    stem="$base"
  fi
  dest="$dest_dir/$base"
  counter=1
  while [ -e "$dest" ]; do
    dest="$dest_dir/${stem}_$counter$extension"
    counter=$((counter + 1))
  done
  mv "$src" "$dest"
}

convert_supported() {
  local file="$1" filename output_base output_pdf
  filename="$(basename "$file")"
  output_base="${filename%.*}"
  output_pdf="$TARGET_DIR/${output_base}.PDF"

  SKIP_ALREADY_EXISTS=0

  if [ -e "$output_pdf" ]; then
    echo "⚠️  Skipping conversion, PDF already exists: $filename"
    SKIP_ALREADY_EXISTS=1
    return 0
  fi

  echo "🔄 Converting: $filename → $(basename "$output_pdf")"
  if ebook-convert "$file" "$output_pdf" --paper-size a4 --pdf-default-font-size 12 --chapter-mark pagebreak >/dev/null; then
    SKIP_ALREADY_EXISTS=0
    return 0
  fi

  echo "❌ Conversion via ebook-convert failed: $filename"
  echo "↪️  Fallback: pandoc + wkhtmltopdf"
  if pandoc_wkhtml_convert "$file" "$output_pdf"; then
    SKIP_ALREADY_EXISTS=0
    return 0
  fi

  return 1
}

pandoc_wkhtml_convert() {
  local file="$1" output_pdf="$2" tmpdir html_out
  tmpdir=$(mktemp -d)
  html_out="$tmpdir/book.html"

  if ! pandoc "$file" --standalone --extract-media="$tmpdir/media" -o "$html_out" >/dev/null 2>&1; then
    echo "❌ Pandoc failed to convert: $(basename "$file")"
    rm -rf "$tmpdir"
    return 1
  fi

  if wkhtmltopdf --quiet --enable-local-file-access "$html_out" "$output_pdf" >/dev/null 2>&1; then
    rm -rf "$tmpdir"
    return 0
  fi

  echo "❌ wkhtmltopdf failed to render HTML for: $(basename "$file")"
  rm -rf "$tmpdir"
  return 1
}

converted=0
conversion_failures=0
unsupported=0
moved_originals=0
skipped_existing=0

while IFS= read -r -d '' file; do
  filename="$(basename "$file")"
  ext="${filename##*.}"
  lower_ext="$(echo "$ext" | tr '[:upper:]' '[:lower:]')"
  case "$lower_ext" in
    pdf)
      continue
      ;;
    epub|mobi|azw3|fb2)
      if convert_supported "$file"; then
        if [ "$SKIP_ALREADY_EXISTS" -eq 1 ]; then
          ((skipped_existing += 1))
        else
          ((converted += 1))
        fi
        safe_move "$file" "$ORIG_DIR"
        ((moved_originals += 1))
      else
        ((conversion_failures += 1))
        continue
      fi
      ;;
    *)
      echo "⚠️  Unsupported non-PDF (moving to _old): $filename"
      safe_move "$file" "$ORIG_DIR"
      ((unsupported += 1))
      ((moved_originals += 1))
      ;;
  esac
done < <(find "$TARGET_DIR" -maxdepth 1 -type f -print0)

printf '\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
printf 'Conversion summary\n'
printf '  Converted successfully : %d\n' "$converted"
printf '  Conversion failures   : %d\n' "$conversion_failures"
printf '  Already had PDF       : %d\n' "$skipped_existing"
printf '  Unsupported moved     : %d\n' "$unsupported"
printf '  Non-PDF moved total   : %d\n' "$moved_originals"
printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'

SOURCE_HASHES=$(mktemp)
DKM_HASHES=$(mktemp)
trap 'rm -f "$SOURCE_HASHES" "$DKM_HASHES"' EXIT

declare -A HASH_TO_FILE=()
declare -a HASH_ORDER=()
duplicates_removed=0

while IFS= read -r -d '' pdf_file; do
  hash=$(sha256sum "$pdf_file" | awk '{print $1}')
  if [[ -n "${HASH_TO_FILE[$hash]:-}" ]]; then
    echo "⚠️  Duplicate detected (same hash). Moving: $(basename "$pdf_file")"
    safe_move "$pdf_file" "$DUP_DIR"
    ((duplicates_removed += 1))
    continue
  fi
  HASH_TO_FILE[$hash]="$pdf_file"
  HASH_ORDER+=("$hash")
done < <(find "$TARGET_DIR" -maxdepth 1 -type f -iname '*.pdf' -print0 | sort -z)

> "$SOURCE_HASHES"
for hash in "${HASH_ORDER[@]}"; do
  printf '%s\t%s\n' "$hash" "${HASH_TO_FILE[$hash]}" >> "$SOURCE_HASHES"
done

printf 'Duplicate summary\n'
printf '  Removed duplicates    : %d\n' "$duplicates_removed"
printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'

find "$DKM_DIR" -maxdepth 1 -type f -iname '*.pdf' -print0 | \
  xargs -0 -r -I{} sha256sum '{}' | awk '{print $1}' | sort -u > "$DKM_HASHES"

if [ ! -s "$DKM_HASHES" ]; then
  echo "⚠️  Warning: No reference PDFs detected in $DKM_DIR"
fi

dkm_removed=0
kept_after_dkm=0

while IFS=$'\t' read -r hash pdf_file; do
  if grep -qx "$hash" "$DKM_HASHES"; then
    echo "🗑️  Matches DKM hash, moving out: $(basename "$pdf_file")"
    safe_move "$pdf_file" "$DKM_DUP_DIR"
    ((dkm_removed += 1))
  else
    ((kept_after_dkm += 1))
  fi
  HASH_TO_FILE[$hash]="$pdf_file"
done < "$SOURCE_HASHES"

printf '\nDKM comparison summary\n'
printf '  Matches removed       : %d\n' "$dkm_removed"
printf '  Remaining PDFs        : %d\n' "$kept_after_dkm"
printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'

final_count=$(find "$TARGET_DIR" -maxdepth 1 -type f -iname '*.pdf' | wc -l | tr -d ' ')
printf '\n📌 Final tally: %s PDFs stay in %s\n' "$final_count" "$TARGET_DIR"
printf 'Archives saved under: %s\n' "$OLD_DIR"
