---
title: "Skeleton-WH Framework - DEPRECATED"
version: "5.0.0"
updated: "2025-12-09"
status: "DEPRECATED"
redirect_to: "12-pattern-linear-loop-prompt.md"
ssot_reference: "ftask/00-ftask.md"
skeleton_ssot: ".fong/instructions/ftask/TEMPLATE-SKELETON.md"
---

<!--
╔══════════════════════════════════════════════════════════════════════════════╗
║  ⚠️ DEPRECATED: Skeleton-WH đã merge vào Linear Loop Prompt (LLP)           ║
║                                                                              ║
║  → Redirect to: docs/12-pattern-linear-loop-prompt.md                        ║
║  → Skeleton SSoT: .fong/instructions/ftask/TEMPLATE-SKELETON.md           ║
╚══════════════════════════════════════════════════════════════════════════════╝
-->

# ⚠️ DEPRECATED: Skeleton-WH Framework

**Pattern này đã deprecated và merge vào Linear Loop Prompt (LLP).**

---

## 🔴 CHỈ CÓ 1 PATTERN: Linear Loop Prompt (LLP)

**→ Redirect to: `docs/12-pattern-linear-loop-prompt.md`**

---

## 🔴 SKELETON SSoT: TEMPLATE-SKELETON.md

**Mọi task/prompt PHẢI clone từ skeleton, KHÔNG được tự viết.**

```bash
# ✅ ĐÚNG: Clone skeleton → Fill vào
cp .fong/instructions/ftask/TEMPLATE-SKELETON.md prompts/XX-task.md
```

| ❌ FORBIDDEN | ✅ REQUIRED |
|--------------|-------------|
| Tự viết file mới | Clone TEMPLATE-SKELETON.md |
| Bỏ qua skeleton | Tuân thủ 8-Section Framework |

---

## 🔗 SSoT Reference: ftask

**autoclaude = ftask + Automation Layer**

Core concepts đã được merge vào ftask (SSoT):

| Concept | Reference (ftask) |
|---------|---------------------|
| **🔴 SSoT Template** | `ftask/TEMPLATE-SKELETON.md` |
| Core Concepts | `ftask/01-core-concepts.md` |
| Diary Schema | `ftask/02-diary-schema.md` |
| AI Workflow | `ftask/05-ai-workflow.md` |
| Error Handling | `ftask/07-auto-debug-fix.md` |
| Mindsets | `mindsets/mindset-*.md` |
| Quick Reference | `ftask/99-quick-reference.md` |

> **🔴 Tạo task mới**: `cp ftask/TEMPLATE-SKELETON.md tasks/XX-task.md`

→ Xem: `.fong/instructions/ftask/00-ftask.md`

---

## Pattern: Linear Loop Prompt (LLP) - ONLY

**CHỈ CÓ 1 PATTERN: Linear Loop Prompt (LLP)**

```
1 prompt = 1 loop → diary per prompt → done marking
```

**Mọi task type** → Dùng **LLP** + Clone từ TEMPLATE-SKELETON.md

→ See: `12-pattern-linear-loop-prompt.md`
→ See: `15-haiku-model-guidelines.md` (cho Haiku model)

---

## 🔥 DRY Exception cho Prompts

**Chấp nhận vi phạm DRY khi tạo prompts.** Mỗi prompt = self-contained.

| Rule | Reason |
|------|--------|
| Copy context OK | AI không có memory giữa sessions |
| Redundancy > Missing | Cold start mỗi prompt |

→ Chi tiết: `ftask/04-micro-task-template.md` § DRY Exception

---

## Core Concept: 8:2:1 Ratio

```
8 work → 2 review → 1 adversarial → RESET
```

→ Chi tiết: `ftask/02-diary-schema.md` § 8:2:1 Cycle Logic

---

## File Map (Autoclaude-Specific Only)

| # | File | Nội dung |
|---|------|----------|
| 00 | **00-skeleton-wh-index.md** | Entry point (file này) |
| 06 | [06-claude-cli.md](./06-claude-cli.md) | Claude CLI flags |
| 07 | [07-config.md](./07-config.md) | Config patterns |
| 08 | [08-telegram.md](./08-telegram.md) | Telegram notification |
| 09 | [09-xterm.md](./09-xterm.md) | Background execution |
| 10 | [10-interleaved-detection-workflow.md](./10-interleaved-detection-workflow.md) | Interleaved detection |
| 11 | [11-init-autoclaude-schema.md](./11-init-autoclaude-schema.md) | init-autoclaude.json schema |
| 12 | [12-pattern-linear-loop-prompt.md](./12-pattern-linear-loop-prompt.md) | LLP Pattern |
| 13 | [13-diary-template.json](./13-diary-template.json) | Diary template |
| 15 | [15-haiku-model-guidelines.md](./15-haiku-model-guidelines.md) | 🆕 Haiku atomic steps |

**Archived**: `archive/` folder chứa deprecated docs đã merge vào ftask.

---

## Quick Reference

- **SSoT**: ftask/00-ftask.md
- **State**: init-autoclaude.json + diary-{loop}.json
- **Checklists**: 9 items (3 kill + 3 exec + 3 verify)
- **Idempotent**: Step có thể chạy lại an toàn
- **Atomic**: Write tmp → rename (POSIX safe)

---

## References

- Gawande, A. (2009). Checklist Manifesto, p. 324.
- ftask Framework: `.fong/instructions/ftask/`
