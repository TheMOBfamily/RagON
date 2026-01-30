---
title: "Skeleton-WH: Memetic Mindset Mode"
parent: 00-skeleton-wh-index.md
version: "1.1.0"
updated: "2025-12-06"
---

## Note

Memetic Mode áp dụng cho CẢ Skeleton-WH và LLP pattern.
→ LLP Context: Memetic evolution trong `notes.lessons_learned[]` của diary

---

## Khái niệm

**Memetic Mindset** = "Vừa làm, vừa học, vừa cải tiến" - AI không chỉ thực thi mà còn có thể tiến hóa instructions khi phát hiện cách làm tốt hơn.

> **Meme** (Richard Dawkins, 1976): Đơn vị thông tin văn hóa có khả năng tự sao chép và tiến hóa.

---

## Khi nào dùng?

| Mode | Use Case |
|------|----------|
| **Strict Compliance** (default) | Critical workflows, first-time tasks, reproducibility required |
| **Memetic Mindset** (opt-in) | Iterative improvement, experimentation, long-running tasks |

### Activation trong Init File

```yaml
---
memetic_mode: true
memetic_scope: [instructions|workflow|verification]
---
```

---

## Quy tắc An toàn (CRITICAL)

| Quy tắc | Mô tả |
|---------|-------|
| **Explicit Permission** | PHẢI có `memetic_mode: true` trong init file |
| **Only Improve** | Chỉ thay đổi nếu kết quả tốt hơn, nhanh hơn, chính xác hơn |
| **Document Everything** | PHẢI ghi chép: WHY, OLD way, NEW way, ROLLBACK |
| **Stateless Clarity** | AI đọc sau PHẢI hiểu được toàn bộ evolution |

---

## Documentation Schema

```json
{
  "memetic_evolution": [
    {
      "change_id": 1,
      "date": "ISO8601",
      "trigger": "Tại sao cần thay đổi",
      "old_way": "Cách làm cũ (exact text)",
      "new_way": "Cách làm mới (exact text)",
      "rationale": "Tại sao cách mới tốt hơn",
      "rollback": "Cách revert nếu cần",
      "verified": true
    }
  ]
}
```

---

## Anti-patterns

| ❌ Anti-pattern | ✅ Nên làm |
|----------------|-----------|
| Thay đổi không ghi chép | LUÔN document trong memetic_evolution |
| Thay đổi không verify | Test và confirm improvement TRƯỚC khi apply |
| Thay đổi nhiều cùng lúc | Một thay đổi mỗi lần, verify trước khi tiếp |
| Không có rollback plan | PHẢI có cách revert |
| Thay đổi ngoài scope | Chỉ modify những gì trong memetic_scope |

---

## Example: Memetic Evolution

**Before:**
```markdown
## Step 3: Extract Year
Use regex `\d{4}` to extract year from filename.
```

**After (với evolution log):**
```markdown
## Step 3: Extract Year
Use regex `(\d{4})(?=[-_.]|$)` to extract year from filename.

## Memetic Evolution Log

### Change #1: Year Extraction Regex
- **Date**: 2025-12-05T16:10:00+07:00
- **Trigger**: Original regex matched incorrectly on "report-2024-Q1.pdf"
- **Old Way**: `\d{4}` (first 4-digit match)
- **New Way**: `(\d{4})(?=[-_.]|$)` (4-digit at word boundary)
- **Rationale**: Avoids false matches, 100% accuracy on test set
- **Rollback**: Revert to `\d{4}` if edge cases appear
- **Verified**: Yes - tested on 50 filenames
```
