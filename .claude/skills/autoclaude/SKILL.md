---
name: autoclaude
description: This skill should be used when the user asks to "run autoclaude", "automation", "one-shot", "single prompt", "batch automation", "loop automation", uses {autoclaude}, {oneshot}, {one-shot}, or needs Claude Code CLI automation (loop or one-shot).
version: 1.0.0
user-invocable: true
disable-model-invocation: false
instructions_source: .claude/skills/autoclaude/readme-instructions-autoclaude-claude-code-automation.md
output_language: Vietnamese
---

## Autoclaude - Claude Code CLI Automation

Hai mode thực thi:
- **Loop mode**: Chạy N lần theo init file (LLP pattern). Cho batch tasks.
- **One-shot mode**: Chạy 1 lần với prompt trực tiếp. Cho test nhanh.


## Mode 1: Loop (LLP - Linear Loop Prompt)

Chạy Claude CLI N lần, mỗi lần đọc task tiếp theo từ init file.

### Workflow

```
init.json (tasks) → autoclaude-block.sh → build 3-layer prompt → claude CLI × N
```

### Commands

```bash
# Non-block (gnome-terminal, background)
.claude/skills/autoclaude/scripts/autoclaude-nonblock.sh "/path/init.json" 30 [--cheap]

# Block (inline, sequential)
.claude/skills/autoclaude/scripts/autoclaude-block.sh "/path/init.json" 30 [--cheap]

# List sessions
.claude/skills/autoclaude/scripts/list-sessions.sh

# Kill session
.claude/skills/autoclaude/scripts/kill-stop-autoclaude.sh [SESSION_ID]
```

### Flags (Loop mode)

| Flag | Default | Description |
|------|---------|-------------|
| Position 1 | (required) | Init file path |
| Position 2 | 1 | Loop count |
| `--cheap` | opus | Use haiku model |
| `--delay N` | 5 | Seconds between loops |
| `--max-time N` | 600 | Timeout per loop (seconds) |
| `--summary TEXT` | init basename | Task summary for Telegram |
| `--test-retry` | false | Fast retry delays (1s,2s,3s) |


## Mode 2: One-shot (Direct Prompt)

Chạy Claude CLI 1 lần duy nhất. Prompt trực tiếp từ CLI, không cần init file.

### Workflow

```
"prompt string" → autoclaude-oneshot.sh → wrap prefix/suffix → claude CLI × 1
```

### Commands

```bash
# Direct prompt
.claude/skills/autoclaude/scripts/autoclaude-oneshot.sh "Check PHP for SQL injection"

# With model
.claude/skills/autoclaude/scripts/autoclaude-oneshot.sh "Fix login bug" --cheap

# From file
.claude/skills/autoclaude/scripts/autoclaude-oneshot.sh -f task.md

# Raw (no prefix/suffix wrapping)
.claude/skills/autoclaude/scripts/autoclaude-oneshot.sh "Just test this" --raw

# Silent (no Telegram)
.claude/skills/autoclaude/scripts/autoclaude-oneshot.sh "Quick test" --no-telegram
```

### Flags (One-shot mode)

| Flag | Default | Description |
|------|---------|-------------|
| Position 1 | (required) | Prompt text |
| `--cheap` | opus | Use haiku model |
| `--raw` | false | No prefix/suffix wrapping |
| `--max-time N` | 600 | Timeout (seconds) |
| `-f FILE` | - | Read prompt from file |
| `--no-telegram` | false | Skip Telegram notifications |
| `--save` | false | Save prompt to prompts/ folder |


## Khi nào dùng mode nào

| Tình huống | Mode | Lý do |
|------------|------|-------|
| Batch 10+ tasks | Loop | Init file quản lý tasks, auto mark done |
| Test nhanh 1 prompt | One-shot | Không cần tạo file, chạy thẳng |
| CI/CD pipeline | One-shot + --raw | Prompt từ pipeline, không cần prefix |
| Long-running project | Loop | Session tracking, retry, checkpoints |
| Debug 1 step | One-shot + --cheap | Nhanh, rẻ |


## Architecture

```
.claude/skills/autoclaude/          <- Skill home (scripts + docs)
  ├── SKILL.md                      <- This file
  ├── config.json                   <- SSoT config (flags, telegram, patterns)
  ├── scripts/                      <- All executable scripts
  │   ├── autoclaude-block.sh       <- Loop mode (blocking)
  │   ├── autoclaude-nonblock.sh    <- Loop mode (gnome-terminal)
  │   ├── autoclaude-oneshot.sh     <- One-shot mode (NEW)
  │   ├── kill-stop-autoclaude.sh   <- Kill sessions
  │   ├── list-sessions.sh          <- List active sessions
  │   └── start-prompt.md           <- Prompt template (loop mode)
  ├── docs/                         <- Documentation
  └── examples/                     <- Usage examples

.fong/claude-code-automation/       <- Prompts storage ONLY
  └── prompts/                      <- Generated prompt files
```


## Config (SSoT)

File: `.claude/skills/autoclaude/config.json`

Key settings:
- `claude_flags.dangerously_skip_permissions`: true (auto-approve)
- `prompt_prefix`: [ultrathink] + mandatory rules
- `prompt_suffix`: NO-QUIT-RULE + Telegram reporting
- `telegram.token` + `telegram.chat_id`: Notification credentials
- `patterns.linear-loop-prompt.checkpoint_interval`: 5 (git commit every 5 loops)


## Prompts Storage

Prompts vẫn ở `.fong/claude-code-automation/prompts/`. Không có symlinks. Chỉ prompts.


## References

- `docs/12-pattern-linear-loop-prompt.md` - LLP pattern chi tiet
- `docs/06-claude-cli.md` - Claude CLI flags
- `docs/07-config.md` - Config documentation
- `docs/08-telegram.md` - Telegram setup
- `docs/16-block-inline-mode.md` - Block vs non-block comparison
- `readme-instructions-autoclaude-claude-code-automation.md` - Full instructions
