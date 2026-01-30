---
title: "Haiku Model Guidelines"
version: "1.0.0"
created: "2025-12-07"
lessons_from: "Hub 9000 Books - Z-Library Autochrome"
---

# Haiku Model Guidelines

> **Bài học từ thực tế**: Haiku CÓ THỂ thực hiện tasks phức tạp nếu được hướng dẫn đúng cách.

---

## 1. Đặc điểm Haiku

| Aspect | Haiku | Sonnet/Opus |
|--------|-------|-------------|
| Context window | Ngắn hơn | Dài hơn |
| Multi-step | Khó | Dễ |
| Cost | Rẻ | Đắt |
| Speed | Nhanh | Chậm hơn |

---

## 2. Nguyên tắc cho Haiku

### 2.1 Atomic Steps (BẮT BUỘC)

```
❌ SAI: "Navigate to URL, parse books, download all"
✅ ĐÚNG:
  STEP 1: Navigate to URL
  STEP 2: Check error
  STEP 3: Parse books
  STEP 4: Click download (1 book)
  STEP 5: Verify download
  ... repeat
```

**Rule**: 1 step = 1 action = 1 MCP call

### 2.2 Explicit MCP Calls

```
❌ SAI: "Use Autochrome to navigate"
✅ ĐÚNG: "Call mcp__autochrome-mcp__executeScript with script: window.location.href = 'URL';"
```

### 2.3 Verification Steps

```
❌ SAI: Trust diary status
✅ ĐÚNG: Verify actual output (Downloads folder, file exists, etc.)
```

---

## 3. Prompt Template cho Haiku

```
Read [instruction file], THEN READ [atomic steps file],
ultrathink, no quit,
PHẢI GỌI [mcp_tool_name] cho mỗi step,
KHÔNG generate fake data,
follow atomic steps exactly,
start from [state file]
```

---

## 4. Anti-patterns (TRÁNH)

| Anti-pattern | Hậu quả | Giải pháp |
|--------------|---------|-----------|
| Combine steps | Haiku skip bước | 1 step = 1 action |
| Implicit MCP | Haiku không gọi | Ghi rõ MCP tool name |
| Trust diary | Fake data | Verify actual files |
| Can thiệp giữa chừng | Interrupt process | Monitor không can thiệp |

---

## 5. Workflow Haiku

```
1. Chuẩn bị:
   - Tạo atomic steps file (từng bước riêng)
   - State file (init-autoclaude.json)

2. Chạy:
   - autoclaude-xterm.sh với prompt explicit
   - --model haiku --count 1 (test trước)

3. Monitor:
   - Check actual outputs (Downloads, files created)
   - KHÔNG can thiệp process đang chạy
   - Đợi hoàn thành rồi mới đánh giá

4. Verify:
   - So sánh diary với actual files
   - Nếu không khớp → Fix prompt → Retry
```

---

## 6. Case Study: Z-Library Downloads

**Vấn đề ban đầu:**
- Diary ghi `"status": "simulated_downloaded"`
- Không có file thực trong Downloads

**Root cause:**
- Prompt không explicit MCP calls
- Haiku extract data nhưng không click download

**Giải pháp:**
1. Tạo `03-haiku-atomic-steps.md` với từng step
2. Mỗi step có MCP call sẵn
3. Thêm verification step

**Kết quả:**
- 20+ PDFs downloaded trong 10 phút
- Rate: ~2 PDF/phút
- Process ổn định

---

## 7. Checklist trước chạy Haiku

```
□ Có atomic steps file? (1 step = 1 action)
□ MCP calls explicit? (tên đầy đủ)
□ State file ready? (init-autoclaude.json)
□ Verification method? (actual output check)
□ Monitor plan? (không can thiệp)
```

---

## 8. Khi nào dùng Haiku vs Sonnet

| Use Case | Model | Lý do |
|----------|-------|-------|
| Simple repetitive | Haiku | Rẻ, nhanh |
| Complex reasoning | Sonnet | Context dài |
| Browser automation | Haiku + atomic | Cost effective |
| Code generation | Sonnet | Quality cao |
| Batch processing | Haiku | Volume cao |
