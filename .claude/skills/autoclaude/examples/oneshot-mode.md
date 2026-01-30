---
title: "Autoclaude One-shot Mode - Example"
date: "2026-01-26"
---

## One-shot Mode Example

### Scenario 1: Test nhanh

```bash
# Chạy 1 prompt trực tiếp, haiku model, không Telegram
.claude/skills/autoclaude/scripts/autoclaude-oneshot.sh \
  "List all PHP files with SQL injection vulnerabilities in modules/" \
  --cheap \
  --no-telegram
```


### Scenario 2: Prompt từ file

```bash
# Đọc prompt từ file, opus model, có Telegram
.claude/skills/autoclaude/scripts/autoclaude-oneshot.sh \
  -f /tmp/my-prompt.md \
  --max-time 300
```


### Scenario 3: Raw mode (không wrap prefix/suffix)

```bash
# Prompt thẳng, không ultrathink, không mandatory rules
.claude/skills/autoclaude/scripts/autoclaude-oneshot.sh \
  "echo 'hello world'" \
  --raw \
  --cheap \
  --no-telegram
```


### Scenario 4: Lưu prompt để debug

```bash
# Chạy và lưu prompt vào prompts/ folder
.claude/skills/autoclaude/scripts/autoclaude-oneshot.sh \
  "Refactor the OTP module validation logic" \
  --save
# Prompt lưu tại: .fong/claude-code-automation/prompts/oneshot-YYYYMMDD-HHMMSS-uuid.md
```


### So sánh Loop vs One-shot

| | Loop | One-shot |
|---|------|----------|
| Input | init.json file | Prompt string hoặc file |
| Loops | N lần | 1 lần |
| Session | Có (ID, kill, list) | Không |
| Retry | Có (exponential backoff) | Không |
| Prompt file | Tự động tạo | Chỉ khi --save |
| Telegram | Luôn bật | Mặc định bật, --no-telegram tắt |
| Prefix/suffix | Luôn wrap | Mặc định wrap, --raw tắt |
