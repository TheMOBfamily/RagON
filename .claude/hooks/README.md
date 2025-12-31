# Claude Hooks Setup Guide

@DEPRECIATED

## Overview

Directory này chứa các hooks cho Claude Code được kích hoạt tự động khi sử dụng.

## Initial Setup - QUAN TRỌNG

### 1. Cập nhật PROJECT_ROOT 

Khi setup lần đầu, **BẮT BUỘC** phải cập nhật đường dẫn PROJECT_ROOT trong file:

```bash
/home/fong/Projects/boiler-plate-cursor-project-with-init-prompt/.claude/hooks/search-memory-on-prompt.sh
```

Tìm dòng này:
```bash
# Configuration
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-/home/fong/Dropbox/Projects/boiler-plate-cursor-project-with-init-prompt}"
```

Thay đổi thành đường dẫn project của bạn:
```bash
# Configuration
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-/path/to/your/actual/project/root}"
```

### 2. Cấu trúc thư mục yêu cầu

Project phải có cấu trúc:
```
your-project-root/
├── .claude/
│   └── hooks/
│       ├── search-memory-on-prompt.sh
│       ├── .env (optional)
│       └── README.md (file này)
└── .fong/
    └── .memory/
        └── (various .md and .json files)
```

### 3. Quyền thực thi

Đảm bảo hook có quyền execute:
```bash
chmod +x /path/to/your/project/.claude/hooks/search-memory-on-prompt.sh
```

## Các Files

### search-memory-on-prompt.sh
- **Chức năng**: Tự động search memory khi user gửi prompt
- **Event**: UserPromptSubmit 
- **Yêu cầu**: Cập nhật PROJECT_ROOT khi setup
- **Output**: Tạo context.json với kết quả search

### .env (optional)
- **Chức năng**: Chứa OpenAI API key và config
- **Format**: KEY=value
- **Example**: Xem example.env

### example.env
- **Chức năng**: Template cho file .env
- **Usage**: `cp example.env .env` và edit

## Troubleshooting

### Memory directory không tìm thấy
```
📭 Memory directory not found
```
**Giải pháp**: Kiểm tra PROJECT_ROOT path và đảm bảo `.fong/.memory/` tồn tại

### Hook không chạy
**Kiểm tra**: 
- Quyền execute của file
- PROJECT_ROOT path đúng
- Cấu trúc thư mục `.fong/.memory/` tồn tại

### API key issues
**Giải pháp**: 
- Tạo file `.env` với OPENAI_API_KEY 
- Hoặc hook sẽ fallback về simple keyword extraction

## Lưu ý

- **KHÔNG** commit file `.env` vào git (chứa API key)
- **LUÔN** cập nhật PROJECT_ROOT khi copy sang project mới
- Memory search hoạt động với files `.md`, `.json`, `.txt` trong `.fong/.memory/`

---

## NO-QUIT-RULE Hook

### Mô tả
Hook tự động inject reminder messages để AI hoàn thành tasks đến cùng, không dừng giữa chừng.

### Files

| File | Mô tả |
|------|-------|
| `no-quit-rule.sh` | PostToolUse hook script |
| `no-quit-rule-config.json` | Config với 30 messages |

### Cách hoạt động

1. **PostToolUse event**: Mỗi khi AI gọi tool xong
2. **Probability 50%**: Random hiển thị hoặc skip
3. **Random message**: 50% warning, 50% từ array 30 messages

### Config (no-quit-rule-config.json)

```json
{
  "active": {
    "probability": 50,
    "warning_message": "AI MUST print..."
  },
  "messages": [
    "NO-QUIT-RULE activated: Complete ALL tasks...",
    // ... 30 messages
  ]
}
```

### Toggle ON/OFF

Trong `no-quit-rule.sh`:
```bash
ACTIVATED=1  # Bật
ACTIVATED=0  # Tắt
```

### Test

```bash
cd .claude/hooks
./no-quit-rule.sh
```

### Behavior khi bật

- AI nhận `system-reminder` với NO-QUIT-RULE message
- AI phải in message verbatim (nếu là warning)
- AI tiếp tục làm việc không dừng giữa chừng
