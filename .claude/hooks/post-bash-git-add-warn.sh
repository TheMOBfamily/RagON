#!/bin/bash
# PostToolUse Hook: Warn about git add <files>
# Matcher: Bash
# Version: 2.0.0 - Follow post-grep.sh pattern

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

# Skip if not git add command
echo "$COMMAND" | grep -qE 'git\s+add\s+' || exit 0

# Skip if git add . (correct usage)
echo "$COMMAND" | grep -qE 'git\s+add\s+\.\s*($|&&|\|)' && exit 0

# Skip if force add (already blocked by PreToolUse)
echo "$COMMAND" | grep -qE 'git\s+add\s+.*(-f|--force)' && exit 0

# WARN: git add <files>
cat << 'EOF'
{
  "decision": "block",
  "reason": "⚠️ WARNING: Detected 'git add <files>'. Rule: ALWAYS use 'git add .' (never individual files). Next time, run 'git add .' to stage all changes."
}
EOF

exit 0
