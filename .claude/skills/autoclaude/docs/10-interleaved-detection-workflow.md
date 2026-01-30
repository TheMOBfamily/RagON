# Interleaved Detection + Adversarial Review Workflow

**Version**: 1.0.0
**Created**: 2025-12-03

## Overview

Workflow xen kẽ giữa Detection và Adversarial Review để đảm bảo chất lượng classification.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Detection 1 │────▶│ Adversarial │────▶│ Detection 2 │
│ (10 files)  │     │ Review 1    │     │ (10 files)  │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Lessons     │
                    │ Learned     │
                    └─────────────┘
```

## Prompts

### 1. Detection Prompt

- **Task**: Tìm papers (<3MB) và duplicates
- **Output**: Report với classifications
- **Key**: KHÔNG tự động move

### 2. Adversarial Prompt

- **Task**: Challenge mỗi classification
- **Mindset**: "Assume WRONG, prove it"
- **Output**: Confirmed actions + lessons learned

## Script Usage

```bash
# Full interleaved run
./scripts/autoclaude-interleaved-detection.sh

# Background run
nohup ./scripts/autoclaude-interleaved-detection.sh > /dev/null 2>&1 &
```

## Safety Measures

1. **No auto-move**: Chỉ report, không move
2. **Double-check**: Adversarial review sau mỗi detection
3. **Logging**: Mọi action đều được log
4. **Telegram**: Notification khi start/complete

## References

- `/home/fong/Projects/mini-rag/.fong/instructions/mindset-proof-by-contradiction-null-hypothesis-adversarial-validation-red-team-exploratory-testing.md`
- `/home/fong/Projects/mini-rag/.fong/instructions/customs/instructions-pdf-batch-processing-workflow/15-cleanup-dkm-and-papers.md`
