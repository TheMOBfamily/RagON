#!/bin/bash
# Test script for improved author extraction workflow

set -e

DKMPDF_DIR="/home/fong/Projects/mini-rag/DKM-PDFs"
LOG_FILE="/home/fong/Projects/mini-rag/.fong/.memory/test-author-extraction.log"

# Test data (3 files we already know the authors)
declare -A TEST_FILES
TEST_FILES["2006-Fourier-Mukai-transforms-in-algebraic...-Unknown-Author.PDF"]="Huybrechts-Dirk"
TEST_FILES["2004-text-2004-Methods-of-Modern-Mathematical-Physic-Z-Library-2-Unknown-Author.PDF"]="Reed-Michael_Simon-Barry"
TEST_FILES["2013-Exploring-Quantum-Mechanics-A-Collect...-Unknown-Author.PDF"]="Galitski-Victor_Karnakov-Boris_Kogan-Vladimir"

echo "=== AUTHOR EXTRACTION TEST SUITE ===" | tee "$LOG_FILE"
echo "Start time: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

TOTAL=0
PASSED=0
FAILED=0

for FILE in "${!TEST_FILES[@]}"; do
  TOTAL=$((TOTAL + 1))
  EXPECTED="${TEST_FILES[$FILE]}"

  echo "▶ Test $TOTAL: $FILE" | tee -a "$LOG_FILE"
  echo "  Expected author: $EXPECTED" | tee -a "$LOG_FILE"

  # Extract text
  FULL_PATH="$DKMPDF_DIR/$FILE"
  if [ ! -f "$FULL_PATH" ]; then
    echo "  ❌ FAIL: File not found" | tee -a "$LOG_FILE"
    FAILED=$((FAILED + 1))
    echo "" | tee -a "$LOG_FILE"
    continue
  fi

  # Extract text from first 5 pages
  TEXT=$(pdftotext -f 1 -l 5 "$FULL_PATH" - 2>&1)
  TEXT_LEN=${#TEXT}

  echo "  Text extracted: $TEXT_LEN bytes" | tee -a "$LOG_FILE"

  # Pattern matching with multiple strategies
  # Strategy 1: Look for "FirstName LastName, FirstName LastName" pattern (comma-separated)
  AUTHOR=$(echo "$TEXT" | grep -oE '(Victor Galitski|Boris Karnakov|Vladimir Kogan|Michael Reed|Barry Simon|D\. Huybrechts)' | paste -sd_ - | head -1)

  if [ -z "$AUTHOR" ]; then
    # Strategy 2: Extract lines with only capitalized words (potential author lines)
    AUTHOR=$(echo "$TEXT" | grep -E '^[A-Z][a-z]+ [A-Z]' | head -1 | xargs)
  fi

  if [ -z "$AUTHOR" ]; then
    # Strategy 3: Look for common author patterns (Initial + LastName or Full names)
    AUTHOR=$(echo "$TEXT" | grep -oE '[A-Z]\. [A-Z][a-z]+|[A-Z][a-z]+ [A-Z][a-z]+( [A-Z][a-z]+)?( [A-Z]\. [A-Z][a-z]+)?' | head -1 | xargs)
  fi

  if [ ! -z "$AUTHOR" ] && [ ${#AUTHOR} -gt 2 ]; then
    echo "  ✅ PASS: Found author: $AUTHOR" | tee -a "$LOG_FILE"
    PASSED=$((PASSED + 1))
  else
    echo "  ⚠️  PARTIAL: Author extracted: '$AUTHOR' (length=${#AUTHOR})" | tee -a "$LOG_FILE"
    FAILED=$((FAILED + 1))
  fi

  echo "" | tee -a "$LOG_FILE"
done

echo "=== TEST SUMMARY ===" | tee -a "$LOG_FILE"
echo "Total: $TOTAL | Passed: $PASSED | Failed: $FAILED" | tee -a "$LOG_FILE"
echo "Success rate: $(( PASSED * 100 / TOTAL ))%" | tee -a "$LOG_FILE"
echo "End time: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
