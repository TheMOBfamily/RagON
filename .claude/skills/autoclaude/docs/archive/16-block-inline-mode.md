---
title: Block vs Non-Block Execution Mode
updated: 2025-12-08
---

# Block vs Non-Block Mode

## Khái niệm

| Mode | Script | Hành vi |
|------|--------|---------|
| **Non-block** | `autoclaude-xterm.sh` | Spawn xterm riêng, AI chính tiếp tục ngay |
| **Block** | `autoclaude-loop.sh` | Chạy inline, AI chính đợi agent hoàn thành |

## Khi nào dùng?

### Non-block (xterm)
- Chạy task dài (>10 phút)
- Không cần kết quả ngay
- Muốn AI chính làm việc khác song song

### Block (inline)
- Cần kết quả trước khi tiếp tục
- Task ngắn (<5 phút)
- Workflow tuần tự: Agent A → Kết quả → Agent B

## Cách chạy

### Non-block (mặc định)
```bash
./scripts/autoclaude-xterm.sh "prompt" --count 3
# Hoặc với haiku: ./scripts/autoclaude-xterm.sh "prompt" --count 3 --cheap
```
- Mở xterm mới
- AI chính return ngay, tiếp tục làm việc khác

### Block (inline)
```bash
./scripts/autoclaude-loop.sh "prompt" --count 3
# Hoặc với haiku: ./scripts/autoclaude-loop.sh "prompt" --count 3 --cheap
```
- Chạy trực tiếp trong terminal hiện tại
- AI chính phải đợi đến khi hoàn thành

## Ví dụ workflow tuần tự (block)

```bash
# Agent 1: Research (block - đợi kết quả)
./scripts/autoclaude-loop.sh "Research topic X, save to /tmp/research.md" --count 1

# Agent 2: Sử dụng kết quả từ Agent 1 (block)
./scripts/autoclaude-loop.sh "Read /tmp/research.md, write summary" --count 1
```

## Ví dụ workflow song song (non-block)

```bash
# Spawn 3 agents chạy song song
./scripts/autoclaude-xterm.sh "Task A" --count 2 &
./scripts/autoclaude-xterm.sh "Task B" --count 2 &
./scripts/autoclaude-xterm.sh "Task C" --count 2 &
```

## Flags chung

| Flag | Mô tả | Default |
|------|-------|---------|
| `--count N` | Số lần loop | 1 |
| `--cheap` | Dùng haiku (tiết kiệm) | opus (không truyền) |
| `--delay N` | Delay giữa các loop (giây) | 5 |

## Output

Cả 2 mode đều:
- Gửi Telegram notify (nếu config)
- Ghi log vào `scripts/debug.log`
- Tạo prompt file trong `prompts/`
