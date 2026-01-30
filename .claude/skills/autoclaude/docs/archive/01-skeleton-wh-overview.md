---
title: "Skeleton-WH: Tổng quan và 10 WH Questions v3.0"
parent: 00-skeleton-wh-index.md
version: "3.1.0"
updated: "2025-12-06"
---

## Tổng quan

**Skeleton-WH** là framework thiết kế prompt stateless cho AI agent automation.

**v3.1 Changes**: Add LLP pattern reference, update diary schema.

**Alternative**: Nếu task đơn giản, tuần tự → Dùng **Linear Loop Prompt (LLP)**: `12-pattern-linear-loop-prompt.md`

---

## Nguyên tắc Stateless

### 1. Idempotent Execution[1]

Mỗi loop có thể chạy lại mà không phá vỡ kết quả trước:
- Tự động alter existing target nếu cần
- Hoặc discard existing + recreate fresh

### 2. Checkpoint Recovery[2]

Lưu trạng thái tại các điểm quan trọng:
- Rollback về checkpoint nếu thất bại
- Không mất progress đã hoàn thành

### 3. State Persistence[3]

JSON files lưu trạng thái giữa các sessions:
- `init-autoclaude.json`: SSoT cho task state + checklists
- `diary-{loop}-{timestamp}.json`: Loop execution logs
- Atomic writes để tránh corruption

---

## Skeleton-WH Questions (10 câu) - v3.0

| # | Câu hỏi | Ý nghĩa | Ghi vào |
|---|---------|---------|---------|
| 1 | **What-Done** | Đã làm gì? | `init.loops.completed` |
| 2 | **What-Have** | Đang có gì (artifacts)? | `init.artifacts[]` |
| 3 | **What-Need** | Cần làm gì tiếp? | `diary.execution.steps_pending[]` |
| 4 | **How-Do** | Làm như thế nào? | Đọc từ instruction files |
| 5 | **How-Order** | Thứ tự trước/sau? | `init.continue_instructions` |
| 6 | **What-Output** | Output cuối là gì? | `init.okr.key_results` |
| 7 | **How-Verify** | Xác nhận đúng/sai? | `init.checklist_verification[]` |
| 8 | **How-DoubleCheck** | Cross-check độc lập? | Independent tool verification |
| 9 | **What-OKR** | Kim chỉ nam cuối cùng? | `init.okr` |
| 10 | **Where-Diary** | Ghi on-the-fly ở đâu? | `init.diary_files[]` → latest |

---

## Anti-patterns (Tránh)

| ❌ Anti-pattern | ✅ Nên làm |
|----------------|-----------|
| Bắt đầu làm mà không đọc init | Luôn đọc init-autoclaude.json TRƯỚC |
| Bỏ qua kill items checklist | Check checklist_kill_items[] TRƯỚC khi làm |
| Ghi diary cuối session | Ghi diary SAU MỖI step |
| Skip verification | Verify theo checklist_verification[] |
| Làm lại từ đầu khi restart | Đọc continue_instructions + tiếp tục |
| File instruction >50 LOC | Split thành nhiều files nhỏ |

---

## References

[1] Engineering AI Systems Architecture, p.49
[2] Distributed Systems, p.506
[3] Building Event-Driven Microservices, p.214
[4] Gawande, A. (2009). Checklist Manifesto, p.324
