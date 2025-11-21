#!/bin/bash
# Find duplicate PDF files by MD5 hash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load environment from .env (portable)
source "$SCRIPT_DIR/../load-env.sh"

cd "$DKM_PDF_PATH" || exit

echo "Finding duplicate files..."
echo

for hash in 5094890468b549c81712a3baa33b464d 520f39d25fcbe853a8d288c7da394cfd 5d2b78154c98496c9f5defd7a0d64d2f bcece50c97b83329954a863ca01ac13d c36ae55cd111e8bec0ba3f6b56a46e60; do
  echo "=== Hash: $hash ==="
  find . -maxdepth 1 -type f \( -name "*.PDF" -o -name "*.pdf" \) -exec md5sum {} \; | grep "^$hash" | awk '{$1=""; print $0}' | sed 's/^  //' | xargs -I {} basename "{}"
  echo
done
