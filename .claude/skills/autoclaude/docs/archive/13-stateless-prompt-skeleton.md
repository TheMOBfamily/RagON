---
title: "LLP Stateless Prompt Skeleton"
version: "2.0.0"
updated: "2025-12-09"
ssot_ref: "fongtask/05-stateless-prompt-skeleton.md"
skeleton_ssot: ".fong/instructions/fongtask/TEMPLATE-SKELETON.md"
pattern: "LLP - ONLY ONE PATTERN"
---

<!--
╔══════════════════════════════════════════════════════════════════════════════╗
║  🚨 CHỈ CÓ 1 PATTERN: Linear Loop Prompt (LLP)                              ║
║                                                                              ║
║  Mọi stateless prompt/task PHẢI:                                            ║
║  1. Clone từ: .fong/instructions/fongtask/TEMPLATE-SKELETON.md              ║
║  2. Fill vào các placeholders [...]                                         ║
║                                                                              ║
║  ❌ FORBIDDEN: Tự viết file task từ đầu                                      ║
║  ✅ REQUIRED: cp TEMPLATE-SKELETON.md → prompts/XX-task.md → Edit           ║
╚══════════════════════════════════════════════════════════════════════════════╝
-->

# LLP Stateless Prompt Skeleton

> **Core skeleton đã định nghĩa tại fongtask (SSoT). File này = LLP-specific additions.**

---

## 🔴 CRITICAL: Clone Skeleton Rule

**Mọi task/prompt PHẢI clone từ TEMPLATE-SKELETON.md, KHÔNG được tự viết.**

```bash
# ✅ ĐÚNG: Clone skeleton → Fill vào
cp .fong/instructions/fongtask/TEMPLATE-SKELETON.md prompts/prompt-XX-task.md

# Sau đó edit file vừa clone, fill các placeholders [...]
```

| ❌ FORBIDDEN | ✅ REQUIRED |
|--------------|-------------|
| Write tool tạo file mới từ đầu | cp TEMPLATE-SKELETON.md → target |
| Tự viết prompt structure | Clone skeleton → Fill placeholders |
| Bỏ qua skeleton format | Tuân thủ 8-Section Framework |

---

## SSoT Reference

**🔴 Template SSoT**: `fongtask/TEMPLATE-SKELETON.md`
**Skeleton Guide**: `fongtask/05-stateless-prompt-skeleton.md`

```bash
# Tạo task mới → Clone từ template
cp .fong/instructions/fongtask/TEMPLATE-SKELETON.md tasks/XX-task-name.md
```

**Template bao gồm**:
- Mô tả ngắn → OKR → Checklist (80% task + 20% verify)
- Iterative Reading Tracker (min 3 lần)
- Config & Mindsets (đọc nếu nhớ < 50%)
- Telegram commands (copy-paste)
- Execution Log (update on-the-fly)
- Entry Point: init*.json
- Done Marking: done-* prefix

---

## LLP-Specific Additions

### 1. Prompt Naming

```
prompt-{XX}-{task-name}.md      # Chưa xong
done-prompt-{XX}-{task-name}.md  # Đã xong
```

### 2. Diary Per Prompt

```
diary-{prompt-id}-{timestamp}.json
```

Ví dụ: `diary-prompt-05-20251207-143000.json`

### 3. Loop Workflow

```
┌─────────────────────────────────────────┐
│ 1. Find: ls *.md | grep -v "^done-"     │
│ 2. Read prompt + diary trước (nếu có)   │
│ 3. Execute steps                        │
│ 4. Update diary on-the-fly              │
│ 5. Cross-check results                  │
│ 6. Mark done: mv prompt-XX done-prompt-XX│
│ 7. Next loop                            │
└─────────────────────────────────────────┘
```

### 4. Checkpoint (Every 5 Loops)

```bash
# Loop 5, 10, 15, 20...
git add . && git commit -m "CHECKPOINT: Loop {N}"
```

---

## LLP Prompt Template (Compact)

```markdown
---
title: "Prompt XX: [Task Name]"
loop: XX
status: pending
---
## OKR
**O**: [1 sentence] | **KR1**: [Measurable] | **KR2**: [Verifiable]

## 5W1H
What: [Task] | Why: [Obj] | Where: [Paths] | When: [Priority] | Who: [Owner] | How: [Approach]

## Steps
1. [Command]

## Cross-Check
Double: [Re-run] | Cross: [Independent tool]

## Done
- [ ] KR1 ✓ | - [ ] KR2 ✓ | - [ ] Cross-check PASSED
```

**Iterative Reading**: Track trong diary `files_read: {"file.md": 2}` (min 2 reads/file)

→ Full skeleton: `fongtask/05-stateless-prompt-skeleton.md` | LLP core: `12-pattern-linear-loop-prompt.md`
