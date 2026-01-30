---
title: "Autoclaude CLI Flags Quick Reference"
date: "2026-01-26"
---

## All Scripts Quick Reference


### autoclaude-oneshot.sh (One-shot)

```
autoclaude-oneshot.sh "prompt" [flags]
autoclaude-oneshot.sh -f file.md [flags]
```

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| (positional 1) | | required | Prompt text |
| `--cheap` | | opus | Haiku model |
| `--haiku` | | opus | Alias for --cheap |
| `--raw` | | false | Skip prefix/suffix |
| `--max-time` | `-t` | 600 | Timeout (seconds) |
| `--file` | `-f` | - | Read from file |
| `--no-telegram` | | false | No notifications |
| `--save` | | false | Save prompt to prompts/ |


### autoclaude-block.sh (Loop - blocking)

```
autoclaude-block.sh "/path/init.json" COUNT [flags]
```

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| (positional 1) | | required | Init file path |
| (positional 2) | | 1 | Loop count |
| `--cheap` | | opus | Haiku model |
| `--haiku` | | opus | Alias for --cheap |
| `--delay` | `-d` | 5 | Seconds between loops |
| `--max-time` | `-t` | 600 | Timeout per loop |
| `--summary` | `-s` | init basename | Task summary |
| `--test-retry` | | false | Fast retry (1s,2s,3s) |
| `--mock-empty` | | false | Simulate empty output |


### autoclaude-nonblock.sh (Loop - gnome-terminal)

Same flags as block.sh. Spawns gnome-terminal in background.

```
autoclaude-nonblock.sh "/path/init.json" COUNT [flags]
```


### kill-stop-autoclaude.sh

```
kill-stop-autoclaude.sh              # Kill all
kill-stop-autoclaude.sh SESSION_ID   # Kill specific
```


### list-sessions.sh

```
list-sessions.sh   # List all active sessions
```


## Claude CLI Flags (Reference)

| Flag | Description |
|------|-------------|
| `-p` | Print mode (non-interactive) |
| `--verbose` | Verbose output |
| `--dangerously-skip-permissions` | Auto-approve all tool calls |
| `--model MODEL` | Model selection (opus, haiku) |


## Config SSoT

Location: `.claude/skills/autoclaude/config.json`

Toàn bộ flags, telegram credentials, prompt prefix/suffix được quản lý trong config.json.
Scripts đọc config tại runtime. Không hardcode.
