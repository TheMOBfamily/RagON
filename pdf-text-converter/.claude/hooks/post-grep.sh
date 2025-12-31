#!/bin/bash
# PostToolUse Hook: Smart Search Reminder
# Matcher: Grep, Glob
# Version: 1.6.0 - CLI-first, MCP secondary

cat << 'EOF'
{
  "decision": "block",
  "reason": "Use smart-search CLI:\n\n/home/fong/Projects/smart-search-fz-rg-bm25/smart-search.sh \"keyword\" /path\n\n📁 Find files: smart-search \"name\" /path -e .sh\n📄 Search content: smart-search \"text\" /path --show-content\n⚡ Fast exact: rg --files --glob \"*.sh\" /path\n\n(MCP: mcp__smart-search__smart-search)"
}
EOF

exit 0
