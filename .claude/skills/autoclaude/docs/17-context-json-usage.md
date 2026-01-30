---
title: "Context.json Usage"
updated: "2025-12-20"
---

# Context.json

## Purpose
- Track autoclaude progress
- Inject context from outside
- Store thinking frameworks

## Rules
| Rule | Description |
|------|-------------|
| Relative Path | Always `.claude/context.json` |
| Never Absolute | No `/home/...` paths |
| Per Project | Each project has own file |

## BEFORE-DURING-AFTER

**Before**: Read context, create from skeleton if missing
**During**: Update status, current_task, 5w1h, six_hats
**After**: Mark completed, save findings, lessons learned

## Setup
```bash
mkdir -p .claude
cp .fong/claude-code-automation/docs/skeleton-context.json .claude/context.json
```

## Schema
```json
{
  "updated": "ISO8601",
  "project": "name",
  "status": "in_progress|completed",
  "last_completed": "task-name",
  "next": "next-task",
  "findings": {}
}
```
