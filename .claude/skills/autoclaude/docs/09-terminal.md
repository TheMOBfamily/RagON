---
title: Terminal Background Mode
updated: 2025-12-20
---

# Terminal Background Mode

> gnome-terminal preferred. More stable than xterm.

## Command
```bash
gnome-terminal --title="Claude Automation" -- bash -c "./script.sh"
```

## Flags
| Flag | Description |
|------|-------------|
| `--title "X"` | Window title |
| `-- bash -c "cmd"` | Run command |
| `&` | Background |

## Verification (CRITICAL)
After launching, ALWAYS verify:
```bash
pgrep -af autoclaude-block  # Must show process
tail -f scripts/debug.log   # Must show iteration
```
If no process → terminal crashed → re-run.

## Auto-close
Script waits for Enter at end:
```bash
echo "Press Enter to close..."
read
```

## Verified
✅ 2025-12-20 - gnome-terminal with verification
