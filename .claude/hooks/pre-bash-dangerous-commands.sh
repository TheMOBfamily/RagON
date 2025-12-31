#!/bin/bash
# PreToolUse Hook: Block dangerous commands
# Matcher: Bash
# Version: 1.0.0
# Managed commands: rm, git add

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

# === BLOCKED COMMANDS ===

# 1. BLOCK: rm (any form) - NEVER delete, always archive
if echo "$COMMAND" | grep -qE '(^|\s|;|&&|\|)rm\s+'; then
    cat << 'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🚫 BLOCKED: 'rm' is FORBIDDEN. Use: mv file \"file.$(date +%Y%m%d_%H%M%S).b\" OR mv folder \"folder.$(date +%Y%m%d_%H%M%S).b\". If you MUST delete, ask USER to do it manually."
  }
}
EOF
    exit 0
fi

# 2. BLOCK: git add -f / --force
if echo "$COMMAND" | grep -qE 'git\s+add\s+.*(-f|--force)'; then
    cat << 'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🚫 BLOCKED: 'git add -f/--force' is FORBIDDEN. This bypasses .gitignore safety. Use 'git add .' instead."
  }
}
EOF
    exit 0
fi

exit 0
