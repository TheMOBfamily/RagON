#!/bin/bash
# PostToolUse Hook: MCP Tools Handler
# Matcher: mcp__.*

# Read stdin (JSON with tool info)
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)

# ==========================================
# PATTERN: Context Collector + Simple Prompt Proxy → Verbose Log + UUID Log
# Fields: tool_response (array of {type,text}), NOT tool_output
# ==========================================
if [[ "$TOOL_NAME" == *"collect_context"* ]] || [[ "$TOOL_NAME" == *"proxy"* ]]; then
  # Absolute path: script lives in context-collector, hook distributed to all projects
  CC_ROOT="/home/fong/Projects/context-collector"
  VERBOSE_SCRIPT="$CC_ROOT/scripts/mcp-verbose-terminal.sh"

  # Parse tool_response[0].text (stringified JSON → parse with fromjson)
  # collect_context: {uuid, summary, output_file, duration_ms}
  # proxy: {uuid, result, duration_ms, engine}
  PARSED=$(echo "$INPUT" | jq -r '.tool_response[0].text | fromjson? // empty' 2>/dev/null)
  UUID=$(echo "$PARSED" | jq -r '.uuid // empty' 2>/dev/null)
  SUMMARY=$(echo "$PARSED" | jq -r '.summary // .result // empty' 2>/dev/null | head -5)
  OUTPUT_FILE=$(echo "$PARSED" | jq -r '.output_file // empty' 2>/dev/null)
  DURATION=$(echo "$PARSED" | jq -r '.duration_ms // empty' 2>/dev/null)

  # Call verbose terminal → get LOG_FILE + ensure xterm open
  if [[ -x "$VERBOSE_SCRIPT" ]]; then
    LOG_FILE=$("$VERBOSE_SCRIPT" "$TOOL_NAME" "${UUID:-no-uuid}")

    # Append output summary to verbose log
    {
      echo "[$(date '+%H:%M:%S')] [DONE] $TOOL_NAME (${DURATION:-?}ms)"
      [[ -n "$OUTPUT_FILE" ]] && echo "Output: $OUTPUT_FILE"
      [[ -n "$SUMMARY" ]] && echo "$SUMMARY"
      echo "---"
    } >> "$LOG_FILE"

    # Append to UUID log if directory exists
    if [[ -n "$UUID" ]]; then
      UUID_LOG_DIR="$CC_ROOT/logs/$UUID"
      if [[ -d "$UUID_LOG_DIR" ]]; then
        {
          echo ""
          echo "=== PostToolUse Hook $(date '+%H:%M:%S') ==="
          echo "Tool: $TOOL_NAME"
          echo "Duration: ${DURATION:-?}ms"
          echo "Verbose log: $LOG_FILE"
          [[ -n "$SUMMARY" ]] && echo "Summary: $SUMMARY"
        } >> "$UUID_LOG_DIR/hook-output.log"
      fi
    fi
  fi

  exit 0
fi

# ==========================================
# PATTERN 0: Knowledge Query Tools → Citation Workflow
# Applies to: queryNewRAG, queryPerplexity, queryCopilot, chinese-zai
# ==========================================
if [[ "$TOOL_NAME" == *"queryNewRAG"* ]] || [[ "$TOOL_NAME" == *"queryPerplexity"* ]] || [[ "$TOOL_NAME" == *"queryCopilot"* ]] || [[ "$TOOL_NAME" == *"chinese-zai"* ]]; then
  cat << 'EOF'
{"decision":"block","reason":"📚 CITATION WORKFLOW (queryNewRAG):\\n\\n**Nếu kết quả QUAN TRỌNG + LIÊN QUAN HỌC THUẬT:**\\n\\n1. GHI CHÉP vào `.fong/docs/citations/{topic}.md`\\n   - Format: APA7 citation + source chunk + page\\n   - Dùng `apa7_recommended` field từ RAG output\\n\\n2. VERIFY citation theo hướng dẫn:\\n   - `.claude/skills/write-paper/instructions-red-team-check-reference-citation.json`\\n   - `.fong/instructions/academic/instructions-apa7-citation-verify.json`\\n\\n3. CHECKLIST (anti-hallucination):\\n   - [ ] DOI exists và resolves?\\n   - [ ] Author name chính xác?\\n   - [ ] Year matches publication?\\n   - [ ] ≥2 sources xác nhận?\\n\\n**Philosophy:** H₀ = Citation is WRONG. Prove otherwise.\\n**Tool:** CrossRef API, Autochrome screenshot, Perplexity cross-check."}
EOF
  exit 0
fi

# ==========================================
# PATTERN 1: TS Reader Tools → Graph Debug
# ==========================================
if [[ "$TOOL_NAME" =~ ts.*reader ]] || [[ "$TOOL_NAME" =~ ts-php-reader ]] || [[ "$TOOL_NAME" =~ ts-ts-js-reader ]] || [[ "$TOOL_NAME" =~ ts-py-reader ]]; then
  cat << 'EOF'
{"decision":"block","reason":"GRAPH DEBUG: MCP reader depth=5. Cần sâu hơn? Gọi standalone .sh với depth=10.\\nPath: /home/fong/Projects/graph-file-tree/graph-*.sh\\nSyntax: graph-*.sh <file.*> --scope <project_root> --depth 10\\nVariants: graph-php.sh | graph-py.sh | graph-ts.sh | graph-js.sh\\nDocs: .fong/instructions/instructions-debug-file-tree-graph.json"}
EOF
  exit 0
fi

# ==========================================
# PATTERN 2: RAG Query Reminder (20% chance)
# ONLY for RAG-related MCPs (queryRAG, queryPerplexity, queryArXiv, queryCopilot)
# NOTE: queryNewRAG already handled in PATTERN 0 with citation workflow
# ==========================================

# Filter: Only apply to RAG-related tools (exclude safe-calculation, context7, fnote, etc.)
RAG_TOOLS_PATTERN="queryRAG|queryPerplexity|queryArXiv|queryCopilot"
if [[ ! "$TOOL_NAME" =~ $RAG_TOOLS_PATTERN ]]; then
  exit 0
fi

# Deduplication
LOCK_FILE="/tmp/post-tool-mcp-lock"
exec 200>"${LOCK_FILE}"
flock -n 200 || exit 0
LAST_RUN=$(cat "${LOCK_FILE}.ts" 2>/dev/null || echo 0)
NOW=$(date +%s)
[[ $((NOW - LAST_RUN)) -lt 2 ]] && exit 0

# Trigger probability (20%)
TRIGGER_PERCENT=20
[[ $((RANDOM % 100)) -ge $TRIGGER_PERCENT ]] && exit 0

echo "${NOW}" > "${LOCK_FILE}.ts"

cat << 'EOF'
{"decision":"block","reason":"RAG PATTERN: Query → <thinking> → Work → Query (if needed). NEVER batch queries. Interleave: 1 query → analyze → do work → query again only if gaps found."}
EOF

exit 0
