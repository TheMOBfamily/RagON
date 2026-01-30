---
title: Claude CLI Reference
updated: 2025-12-09
---

# Claude CLI Reference

## Models - Chỉ 2 Options

| Option | Model | Use Case |
|--------|-------|----------|
| (mặc định) | opus | Complex tasks, critical decisions |
| `--cheap` | haiku | Simple, repetitive, high volume |

**Đơn giản hóa**: Không cần nhớ nhiều. Mặc định = opus. Tiết kiệm = `--cheap`.

## Non-interactive mode

```bash
# Mặc định (opus)
claude -p "prompt"

# Cheap mode (haiku)
claude -p "prompt" --model haiku
```

## Flags

| Flag | Mô tả |
|------|-------|
| `-p "prompt"` | Print & exit |
| `--model haiku` | Cheap mode (tiết kiệm) |
| `--dangerously-skip-permissions` | Skip approval |
| `-c` | Continue session |
| `--output-format json` | Output JSON |

## Verified

✅ 2025-12-09 - Simplified to 2 options only
