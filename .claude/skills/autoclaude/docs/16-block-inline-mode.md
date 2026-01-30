---
title: "Block vs Non-Block Mode"
updated: "2025-12-20"
---

# Execution Modes

## Comparison
| Mode | Script | Behavior |
|------|--------|----------|
| Non-block | `autoclaude-nonblock.sh` | Spawn gnome-terminal, verify, continue |
| Block | `autoclaude-block.sh` | Inline, wait for completion |

## When to Use
| Scenario | Mode |
|----------|------|
| Long task (>10 min) | Non-block |
| Need result first | Block |
| Sequential workflow | Block |

## Commands
```bash
# Non-block (parallel)
./scripts/autoclaude-nonblock.sh "prompt" 3 [--cheap]

# Block (sequential)
./scripts/autoclaude-block.sh "prompt" 3 [--cheap]
```

## Flags
| Flag | Description |
|------|-------------|
| `N` (number) | Loop count |
| `--cheap` | Use haiku model |
