---
title: "Telegram Notification"
updated: "2025-12-20"
---

# Telegram Notification

## Credentials
```bash
TOKEN="8550967390:AAEZcUW78U6QA9CI71YA1eDWTlttkbj4O7M"
CHAT_ID="7274005773"
```

## Context Fields
| Field | Source |
|-------|--------|
| PROJECT | `basename $(pwd)` |
| PROMPT | Folder name or init.json |
| OKR | `jq '.okr.objective' init.json` |
| LOOP | `jq '.loops.current/.total'` |

## Send Message
```bash
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d chat_id="${CHAT_ID}" \
  -d parse_mode="HTML" \
  -d text="🚀 <b>START</b>
📂 ${PROJECT}
📛 ${PROMPT}
🎯 ${OKR}
🔢 ${LOOP}
⏰ $(TZ='Asia/Ho_Chi_Minh' date '+%Y-%m-%d %H:%M:%S')"
```

## When to Send
| Event | Send? |
|-------|-------|
| Session start | ✅ |
| Loop complete | ✅ |
| All done | ✅ |
| Error (needs human) | ✅ |
| Error (can retry) | ❌ |

## Checklist
1. Credentials valid? (`curl .../getMe`)
2. Context extractable?
3. Message sent? (`"ok":true`)
4. No empty placeholders?
5. Vietnam timezone? (UTC+7)
