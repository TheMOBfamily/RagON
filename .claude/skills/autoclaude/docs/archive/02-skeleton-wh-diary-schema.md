---
title: "Skeleton-WH: Diary Schema v2.0 (8:2 Ratio + 5W1H + 6 Hats)"
parent: 00-skeleton-wh-index.md
version: "2.1.0"
updated: "2025-12-06"
---

## Diary Schema v2.0

> **AI đọc diary → trả lời 5W1H + 6 Hats → làm ngay không mất thời gian**

**Note**: Đây là diary schema cho Skeleton-WH. Cho LLP pattern, xem `13-diary-template.json`.

```json
{
  "version": "2.0",
  "okr": "Mô tả OKR ngắn gọn",

  "5w1h": {
    "what": "Task gì?",
    "why": "Tại sao làm?",
    "where": "Files/folders nào?",
    "when": "Deadline?",
    "who": "AI model nào?",
    "how": "Cách làm (link to 02-*.md)"
  },

  "six_hats": {
    "white_facts": "Dữ liệu: X files, Y LOC",
    "red_intuition": "Cảm nhận: Phức tạp/Đơn giản",
    "black_risks": "Rủi ro: Breaking changes?",
    "yellow_benefits": "Lợi ích: Performance/Maintainability",
    "green_alternatives": "Phương án khác?",
    "blue_process": "Tiến trình: Step X of Y"
  },

  "cycles": {
    "work_count": 0,
    "review_count": 0,
    "adversarial_count": 0,
    "ratio_target": "8:2:1",
    "next_action": "work|review|adversarial"
  },

  "progress": {
    "current_step": 1,
    "total_steps": 5,
    "status": "in_progress|completed|failed"
  },

  "completed": [],
  "pending": [],
  "artifacts": [],
  "errors": [],
  "last_updated": "ISO8601"
}
```

---

## Cycle Logic (8:2:1)

```
work_count < 8  → next_action = "work"
work_count >= 8 AND review_count < 2 → next_action = "review"
review_count >= 2 AND adversarial_count < 1 → next_action = "adversarial"
adversarial_count >= 1 → RESET (work_count=0, review_count=0, adversarial_count=0)
```

---

## AI Quick Parse

AI đọc diary → **1 giây** biết:

| Câu hỏi | Đọc từ |
|---------|--------|
| Làm gì? | `5w1h.what` |
| Tại sao? | `5w1h.why` |
| Đã làm bao nhiêu? | `cycles.work_count` |
| Đã review chưa? | `cycles.review_count > 0` |
| Phản biện chưa? | `cycles.adversarial_count > 0` |
| Tiếp theo làm gì? | `cycles.next_action` |
| Rủi ro? | `six_hats.black_risks` |
| Progress? | `progress.current_step / total_steps` |

---

## Example

```json
{
  "version": "2.0",
  "okr": "Rename 31 PDFs theo pattern",
  "5w1h": {
    "what": "Rename PDFs",
    "why": "Chuẩn hóa naming",
    "where": "./pdfs/",
    "when": "2025-12-05",
    "who": "haiku",
    "how": "./02-rename-steps.md"
  },
  "six_hats": {
    "white_facts": "31 files, avg 2MB",
    "red_intuition": "Simple task",
    "black_risks": "Overwrite existing",
    "yellow_benefits": "Easy search",
    "green_alternatives": "Symlinks?",
    "blue_process": "Step 3/5"
  },
  "cycles": {
    "work_count": 8,
    "review_count": 1,
    "adversarial_count": 0,
    "ratio_target": "8:2:1",
    "next_action": "review"
  },
  "progress": {"current_step": 3, "total_steps": 5, "status": "in_progress"}
}
```
