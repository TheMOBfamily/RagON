---
name: todo
description: This skill should be used when the user asks to "todo", "task", "asana", "list tasks", "upcoming", "what to do", "việc cần làm", uses {todo}, {asana}, or needs Asana task management.
version: 1.0.0
user-invocable: true
disable-model-invocation: false
instructions_source: .fong/instructions/fongasana/00-fongasana.md
output_language: Vietnamese
---

<!-- CRITICAL: Tiếng Việt CÓ DẤU - ZERO TOLERANCE -->

# Todo - Asana Task Management Skill

Quản lý tasks Asana. Search, sync, CRUD. Tách biệt theo project.


## Scripts (SSoT)

```bash
alias asana='.fong/instructions/fongasana/scripts/asana-api.sh'
SYNC='.fong/instructions/fongasana/scripts/sync-asana-v2.sh'
```

NEVER curl trực tiếp. ALWAYS qua scripts.


## Project IDs (TÁCH BIỆT)

Chi tiết: `references/project-ids.md`

### Workspace: Self (`1159540075171841`)

| Project | ID | Ghi chú |
|---------|-----|---------|
| **HUB ThS MIS/BIS** | `1208349044334842` | Thạc sĩ |
| **Co-Linh Forecasting** | `1208349044335291` | Nghiên cứu cô Linh |
| **Irontan** | `1208349044335334` | Website quỹ tín dụng |
| **Ideas** | `1208349044335343` | Ý tưởng |
| **FongTodo** | `1208349044335387` | Cá nhân chung |
| **PhD** | `1208349044335436` | Nghiên cứu tiến sĩ |

### Workspace: Deutschfuns (`1211300418667644`)

| Project | ID | Ghi chú |
|---------|-----|---------|
| **Deutschfuns** | `1211300559260717` | LMS chính |

CRITICAL: Mỗi project là RIÊNG BIỆT. Khi tạo task PHẢI chỉ rõ project ID.


## Task Tree (SSoT)

**File**: `/home/fong/Dropbox/pool-memory/asana-task-tree.json`

- Dùng chung cho MỌI dự án (shared across projects)
- Structure: `incomplete_tasks` (focus) -> `complete_tasks` (reference)
- On-the-fly: Đọc ngay khi script đang chạy


## Sync Rules

Sync khi:
1. Tìm không ra task
2. Nghi ngờ dữ liệu cũ
3. Lần update trước quá lâu (> vài giờ)

```bash
# Sync background (on-the-fly readable)
$SYNC sync &

# Xem tree
$SYNC tree

# Search
$SYNC search "keyword"

# Upcoming sorted by due date
$SYNC upcoming
```


## AI Workflow (MANDATORY)

```
1. TÌM trong incomplete_tasks (jq hoặc script search)
   ↓
2. KHÔNG TÌM THẤY? → Thử API search
   ↓
3. VẪN KHÔNG CÓ? → Sync background (on-the-fly)
   ↓
4. TÌM LẠI ngay (không cần đợi sync xong)
   ↓
5. VẪN KHÔNG CÓ? → Tạo task mới
```


## CRUD Operations

### READ

```bash
asana task {TASK_ID}              # Chi tiết task
asana full {TASK_ID}              # Full: content + attachments + comments + subtasks
asana url "https://..."           # Task từ URL
asana projects                    # Danh sách projects
asana subtasks {TASK_ID}          # Subtasks
asana attachments {TASK_ID}       # Attachments
asana comments {TASK_ID}          # Comments
```

### CREATE

```bash
asana create {PROJECT_ID} "Tên task" "Ghi chú"
asana create-subtask {PARENT_TASK_ID} "Tên subtask"
```

**CRITICAL - Subtask PHẢI có assignee + project:**

Subtask tạo bằng `create-subtask` KHÔNG tự kế thừa assignee và project từ parent.
SAU KHI tạo subtask, PHẢI chạy thêm 2 lệnh:

```bash
# 1. Gán assignee (A Fong = 1133089446774381)
asana raw PUT "/tasks/{SUBTASK_ID}" '{"data":{"assignee":"1133089446774381"}}'

# 2. Thêm vào project
asana raw POST "/tasks/{SUBTASK_ID}/addProject" '{"data":{"project":"{PROJECT_ID}"}}'
```

VIOLATION: Subtask không có assignee + project = task MẤT TÍCH trong Asana (không hiện ở My Tasks, không hiện ở project board).

### UPDATE

```bash
asana update {TASK_ID} name "Tên mới"
asana update {TASK_ID} notes "Ghi chú mới"
asana update {TASK_ID} due_on "2026-01-15"
asana complete {TASK_ID} true       # Hoàn thành
asana complete {TASK_ID} false      # Chưa xong
```

### DELETE

```bash
asana raw DELETE /tasks/{TASK_ID}
```

### DOWNLOAD

```bash
asana download {ATTACHMENT_ID} .temp/
```

### RAW API

```bash
asana raw GET /users/me
asana raw GET /projects/{PROJECT_ID}/tasks
asana raw GET "/workspaces/1159540075171841/tasks/search?text=keyword"
```


## Quick Search (jq)

```bash
# Incomplete tasks sorted by due date
jq -r '[.incomplete_tasks[] | .projects[] | .tasks[] | {due: .due_on, name: .name, id: .gid}] | sort_by(.due // "9999") | .[] | "\(.due // "no-due") | \(.id) | \(.name)"' /home/fong/Dropbox/pool-memory/asana-task-tree.json | head -20

# Filter by project name
jq -r '.incomplete_tasks[] | select(.workspace_name == "Deutschfuns" or (.projects[] | .project_name == "Deutschfuns")) | .projects[] | .tasks[] | "\(.due_on // "no-due") | \(.gid) | \(.name)"' /home/fong/Dropbox/pool-memory/asana-task-tree.json
```


## Critical Rules

1. **USE SCRIPTS** - NEVER curl trực tiếp
2. **UTF-8** - Tiếng Việt có dấu đầy đủ
3. **WBS Scan** - Scan hierarchy TRƯỚC khi tạo task
4. **Plain Text** - NO markdown trong Asana notes
5. **Rate Limit** - 150 requests/minute
6. **SYNC TRƯỚC** - Khi nghi ngờ hoặc tìm không ra
7. **PROJECT ID** - Ghi rõ ID khi tạo/tìm task
8. **TÁCH BIỆT** - Deutschfuns != Cá nhân != iOS != Read
9. **DATE FORMAT** - YYYY-MM-DD


## Output Format (khi user invoke /todo)

```
Skill: /todo | Asana Task Manager
{YYYY-MM-DD HH:MM:SS} (+07)

Project: {tên project} (ID: {project_id})
---
[Kết quả: danh sách tasks / chi tiết task / action result]
```


## Key Files

| Resource | Path |
|----------|------|
| API Script (SSoT) | `.fong/instructions/fongasana/scripts/asana-api.sh` |
| Sync Script v2 | `.fong/instructions/fongasana/scripts/sync-asana-v2.sh` |
| Download Script | `.fong/instructions/fongasana/scripts/asana-download.sh` |
| Task Tree | `/home/fong/Dropbox/pool-memory/asana-task-tree.json` |
| Tracking File | `/home/fong/Dropbox/pool-memory/asana-fong.json` |
| Full Docs | `.fong/instructions/fongasana/` |


## Cross-References

| Context | File |
|---------|------|
| Main Index | `.fong/instructions/fongasana/00-fongasana.md` |
| Authentication | `.fong/instructions/fongasana/01-authentication.md` |
| WBS Methodology | `.fong/instructions/fongasana/02-wbs-methodology.md` |
| Tracking System | `.fong/instructions/fongasana/03-tracking-system.md` |
| CRUD Operations | `.fong/instructions/fongasana/04-crud-operations.md` |
| Subtask Management | `.fong/instructions/fongasana/05-subtask-management.md` |
| Helper Functions | `.fong/instructions/fongasana/06-helper-functions.md` |
| Attachments | `.fong/instructions/fongasana/07-attachments.md` |
| Workflow | `.fong/instructions/fongasana/08-workflow.md` |
| Checklist | `.fong/instructions/fongasana/09-checklist.md` |
| UTF-8 Encoding | `.fong/instructions/fongasana/10-utf8-encoding.md` |
| Quick Reference | `.fong/instructions/fongasana/99-quick-reference.md` |
| Camera OCR | `.fong/instructions/instructions-camera-uploads-ocr-hash.md` |
| Obsidian Notes | `.fong/instructions/instructions-CRUD-obsidian-notes/` |


## Camera Uploads (OCR Todo)

Todo từ ảnh chụp camera. OCR tự động.

```bash
# Xem ảnh gần đây
"/home/fong/Camera Uploads/.ocr-hash/run.sh" list 20

# Tìm todo trong OCR content
rg "keyword" "/home/fong/Camera Uploads/.ocr-hash/hashes/"

# Đọc OCR content của 1 ảnh
"/home/fong/Camera Uploads/.ocr-hash/run.sh" read "filename.jpeg"

# Process ảnh mới (nếu chưa OCR)
"/home/fong/Camera Uploads/.ocr-hash/run.sh" process 10
```

Workflow: `list` -> `rg keyword` -> `read` -> tạo task Asana nếu cần.

Ref: `.fong/instructions/instructions-camera-uploads-ocr-hash.md`


## Obsidian Notes

Todo/notes cũng lưu ở Obsidian vault.

**Base Path**: `/home/fong/Projects/dropbox-obsidian/FongObsidian/`

### MCP fnote (ưu tiên)

```bash
# Search
mcp__fnote__obsidian-search keywords=["todo", "task"]

# Read
mcp__fnote__obsidian-read path="/home/fong/Projects/dropbox-obsidian/FongObsidian/path/to/note.md"

# Create
mcp__fnote__obsidian-create title="Todo Title" content="Content" folder="AI"

# Update
mcp__fnote__obsidian-update path="/path/to/note.md" content="Updated"
```

### CLI fallback

```bash
# Search trong vault
rg "keyword" /home/fong/Projects/dropbox-obsidian/FongObsidian/
smart-search "keyword" /home/fong/Projects/dropbox-obsidian/FongObsidian/ -e .md
```

Ref: `.fong/instructions/instructions-CRUD-obsidian-notes/`


## Checklist (9 items)

- [ ] Task tree đọc trước?
- [ ] Sync nếu dữ liệu cũ?
- [ ] Project ID đúng?
- [ ] Tách biệt projects?
- [ ] Scripts (không curl)?
- [ ] UTF-8 tiếng Việt?
- [ ] Plain text (không markdown) trong notes?
- [ ] WBS scan trước khi tạo?
- [ ] Subtask có assignee? (KHÔNG tự kế thừa!)
- [ ] Subtask nằm trong project? (KHÔNG tự kế thừa!)
- [ ] Ghi rõ task ID cho user?
