#!/bin/bash
# DSS Output Validator
# Validates .md file has proper footnote citations

set -e

FILE="$1"

if [[ -z "$FILE" ]]; then
    echo "Usage: validate-output.sh <file.md>"
    exit 1
fi

if [[ ! -f "$FILE" ]]; then
    echo "❌ File not found: $FILE"
    exit 1
fi

echo "🔍 Validating DSS output: $FILE"
echo "---"

# Check YAML frontmatter
if grep -q "^---" "$FILE" && grep -q "protocol:" "$FILE"; then
    PROTOCOL=$(grep "protocol:" "$FILE" | head -1 | cut -d'"' -f2)
    echo "✅ Protocol: $PROTOCOL"
else
    echo "⚠️ Missing YAML frontmatter or protocol"
fi

# Count in-text citations [^N]
IN_TEXT=$(grep -oE '\[\^[0-9]+\]' "$FILE" | wc -l)
echo "📝 In-text citations: $IN_TEXT"

# Count footnote definitions
DEFINITIONS=$(grep -cE '^\[\^[0-9]+\]:' "$FILE" || echo "0")
echo "📎 Footnote definitions: $DEFINITIONS"

# Check for orphan citations
echo "---"
echo "🔎 Checking for orphans..."

# Get unique in-text citation numbers
IN_TEXT_NUMS=$(grep -oE '\[\^[0-9]+\]' "$FILE" | sort -u | grep -oE '[0-9]+')

# Get defined footnote numbers
DEFINED_NUMS=$(grep -oE '^\[\^[0-9]+\]:' "$FILE" | grep -oE '[0-9]+')

# Check each in-text citation has definition
ORPHANS=0
for NUM in $IN_TEXT_NUMS; do
    if ! echo "$DEFINED_NUMS" | grep -q "^${NUM}$"; then
        echo "❌ Citation [^$NUM] has no definition!"
        ((ORPHANS++))
    fi
done

if [[ $ORPHANS -eq 0 ]]; then
    echo "✅ All citations have definitions"
fi

# Check sources_used matches actual
if grep -q "sources_used:" "$FILE"; then
    DECLARED=$(grep "sources_used:" "$FILE" | grep -oE '[0-9]+')
    UNIQUE_SOURCES=$(grep -oE '^\[\^[0-9]+\]:' "$FILE" | wc -l)

    if [[ "$DECLARED" -eq "$UNIQUE_SOURCES" ]]; then
        echo "✅ sources_used ($DECLARED) matches actual ($UNIQUE_SOURCES)"
    else
        echo "⚠️ sources_used ($DECLARED) != actual footnotes ($UNIQUE_SOURCES)"
    fi
fi

# Summary
echo "---"
echo "📊 Summary:"
echo "   In-text: $IN_TEXT | Definitions: $DEFINITIONS | Orphans: $ORPHANS"

if [[ $ORPHANS -gt 0 ]]; then
    echo "❌ VALIDATION FAILED"
    exit 1
else
    echo "✅ VALIDATION PASSED"
    exit 0
fi
