---
title: "Claude Code Automation"
version: "11.0.0"
updated: "2025-12-30"
aliases: ["{autoclaude}", "{microtask}", "{stateless task}", "{wbs task}"]
ssot_reference: "ftask/00-ftask.md"
---

# Claude Code Automation

> **autoclaude = ftask + Automation Tools**

## Terminology
**microtask = stateless task = wbs task** (3 terms, 1 concept)
- Self-contained. Cold start OK.
- 1 task = 1 prompt = 1 loop.

## Task Quantity (Fibonacci Rule)
| Min | Sequence | Example |
|-----|----------|---------|
| 8 | 8, 13, 21, 34, 55... | 8 tasks minimum |

## Task Ratio (80:20)
| Type | % | Purpose |
|------|---|---------|
| Output | 80% | Produce deliverables |
| Review/Red-team/Fix | 20% | Quality assurance |

Example: 10 tasks = 8 output + 2 review

## Loop Count Formula
```
loops = microtasks × 1.2
```
Example: 10 tasks → 12 loops (buffer for fixes)

## OKR Buffer Rule
Plan OKR with 20% buffer. Red-team finds bugs → time to fix.
```
KR target = actual_need × 1.2
```

## Quick Rules

### Task Creation
```bash
cp .fong/instructions/ftask/TEMPLATE-SKELETON.md XX-task-name.md
# Fill sections. NEVER write from scratch.
```

### Task Completion (5 Steps)
1. Fill Execution Log (timestamps, actions, outputs)
2. Update YAML: `status: "completed"`
3. Rename: `XX-task.md` → `done-XX-task.md`
4. Git: `git add . && git commit -m "feat(task-XX): ..."`
5. Update init-autoclaude.json: `completed` array

### Entry Point
AI enters folder → Find `init-autoclaude.json` → Read `files_order` → Execute

## SSoT Map

| Need | ftask/ (SSoT) | autoclaude/ |
|------|---------------|-------------|
| Template | `TEMPLATE-SKELETON.md` | - |
| Lifecycle | `13-task-lifecycle-mark-done.md` | config.json |
| Diary | `02-diary-schema.md` | `docs/13-diary-template.json` |

**Principle**: ftask = Framework SSoT. autoclaude = Automation Layer.

## Structure
```
claude-code-automation/
├── config.json       ← Prompt prefix/suffix, telegram
├── scripts/          ← autoclaude-*.sh
├── docs/             ← Patterns, schemas
└── logs/             ← Debug logs
```

## Scripts
```bash
# Non-block (gnome-terminal) - Long tasks - PREFERRED
./scripts/autoclaude-nonblock.sh "/path/to/init.json" <loops> [--cheap] [--max-time 600]

# Block (inline) - Short tasks
./scripts/autoclaude-block.sh "/path/to/init.json" <loops> [--cheap] [--max-time 600]

# List active sessions
./scripts/list-sessions.sh

# Kill by SESSION_ID or all
./scripts/kill-stop-autoclaude.sh [SESSION_ID]

# Loop calculation: loops = microtasks × 1.2
```

## Feature: Session ID (v11.0)
Mỗi instance có unique SESSION_ID để tracking.

| Component | Format |
|-----------|--------|
| ID | `YYYYMMDD-HHMMSS-uuid4` |
| File | `sessions/<SESSION_ID>.session` |
| Display | Terminal title, console, telegram, debug.log |

```bash
# List all active sessions
./scripts/list-sessions.sh

# Kill specific session
./scripts/kill-stop-autoclaude.sh 20251230-234853-372f

# Kill all sessions
./scripts/kill-stop-autoclaude.sh
```

## Feature: Exponential Backoff Retry (v11.0)
Auto-retry khi Claude CLI trả empty response.

| Retry | Delay | Use Case |
|-------|-------|----------|
| 1 | 30s | Transient error |
| 2 | 2 min | Network glitch |
| 3 | 10 min | Rate limit |
| 4 | 30 min | API cooldown |
| 5 | 2 hours | Daily limit |

**Behavior**: Continue after exhausted retries (không abort loop).

**Test flags**:
```bash
# Quick test với mock
./autoclaude-block.sh "/path/init.json" 1 --test-retry --mock-empty
```

## Timeout (MANDATORY)
**Mỗi loop PHẢI có timeout để tránh hang.**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--max-time` / `-t` | 600 (10 phút) | Timeout per loop (seconds) |

```bash
# Custom timeout: 15 phút per loop
./scripts/autoclaude-block.sh "/path/init.json" 10 --max-time 900
```

**Exit codes:**
- `124` = Timeout (exceeded max-time)
- `137` = Force killed (didn't respond to SIGTERM)

**Telegram alerts:** Tự động gửi khi timeout xảy ra.

## Verification Rule (CRITICAL)
After launching nonblock, ALWAYS verify:
```bash
pgrep -af autoclaude-block  # Must show running process
tail -f scripts/debug.log   # Must show iteration logs
```
If no process → terminal crashed → re-run or debug.

## Docs Reference
| File | Content |
|------|---------|
| `06-claude-cli.md` | CLI flags |
| `08-telegram.md` | Notification |
| `12-pattern-linear-loop-prompt.md` | LLP pattern |

---
**Read more**: `ftask/00-ftask.md` (SSoT Framework)
