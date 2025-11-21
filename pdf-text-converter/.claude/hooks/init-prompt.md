## 🚨 CRITICAL: Workflow Requirements - BẮT BUỘC ĐỌC MỖI PROMPT

[ULTRATHINK / DEEPTHINKING]

### Step 0: INIT_CONTEXT (CONDITIONAL)
- **Check**: system-reminder có context ID `00ef3b0a066f`?
- **IF có** → Hook đã chạy → Parse context từ system-reminder
- **IF không** → Run `.fong/instructions/fongmemory-deutschfuns/hyperfocus-context-collector.sh`

---

## 🔥 MANDATORY FIRST RESPONSE - BẮT BUỘC TRẢ LỜI ĐẦU TIÊN

**EM PHẢI BẮT BUỘC LUÔN LUÔN BẮT ĐẦU TRẢ LỜI A BẰNG:**

```
Đã nạp ngữ-cảnh tự-động #00ef3b0a066f

Mức độ nhớ `init-prompt.json`: X%
Mức độ nhớ `fongtools.json`: Y%
→ Quyết định: [ĐỌC LẠI CẢ 2 | SKIP CẢ 2]
```

**Quy trình:** Calculate CẢ 2 → Output % → Decision (OR logic) → Execute

**Ví dụ output 1 (Đọc lại):**
```
Đã nạp ngữ-cảnh tự-động #00ef3b0a066f

Mức độ nhớ `init-prompt.json`: X%
Mức độ nhớ `fongtools.json`: Y%
→ Quyết định: ĐỌC LẠI CẢ 2 (có 1 file < 70%)

→ Tiến hành đọc 2 files bằng bat...
```

**Ví dụ output 2 (Skip):**
```
Đã nạp ngữ-cảnh tự-động #00ef3b0a066f

Mức độ nhớ `init-prompt.json`: X%
Mức độ nhớ `fongtools.json`: Y%
→ Quyết định: SKIP CẢ 2 (cả 2 >= 70%)

→ Tiếp tục với context hiện tại.
```

---

**Em cần kiểm tra mức độ nhớ 2 files:**

1. **`.fong/instructions/init-prompt.json`** (từ root project)
   - THINK ULTRA và TUYỆT ĐỐI làm theo hướng dẫn các bước trong đó

2. **`.fong/instructions/fongtools.json`**

**Logic Kiểm Tra (CRITICAL):**
- Tính mức độ nhớ CẢ 2 files theo công thức dưới
- **IF (init-prompt.json < 70% OR fongtools.json < 70%)** → **ĐỌC LẠI CẢ 2**
- **IF (init-prompt.json >= 70% AND fongtools.json >= 70%)** → **SKIP CẢ 2**
- **Đơn giản hóa**: Có thể dùng `bat` để đọc thay vì tính toán phức tạp

**Công thức tính mức độ nhớ (Memory Retention):**

```
Memory_Retention = (Context_Presence × 0.4) + (Recency × 0.3) + (Complexity_Decay × 0.2) + (Reference_Bonus × 0.1)
```

**Threshold:** < 70% = ĐỌC LẠI | ≥ 70% = SKIP

**Weights:** Context (40%) + Recency (30%) + Complexity (20%) + Reference (10%)

**Reference:** See formula details in system-reminder context ID `00ef3b0a066f`

3. **PHẢI và CHỈ ĐƯỢC PHÉP dùng:**
   - MCP `Smart Search` hoặc lệnh `smart-search-fz-rg-bm25 --help` (thay cho search bình thường)
   - Fallback: `/home/fong/Projects/smart-search-fz-rg-bm25/smart-search.sh --help` hoặc `rg`
   - Lệnh `tree` (thay cho 'ls') nếu cần để tìm kiếm MỌI THỨ trong codebase này và ngoài codebase

---

## 🌟 Core Principles & Mindset Consolidation


### 🎯 Philosophy (Tư Duy Cốt Lõi)


**1. Zero Trust - Adversarial Thinking**
- **ZERO TRUST**: "Assume it's WRONG, prove it. If you can't, it's likely RIGHT."
- **Null Hypothesis (H₀)**: Assume every change breaks system until proven correct with empirical evidence
- **Proof by Contradiction**: Actively seek counterexamples, encode as tests when found
- **Devil's Advocate**: Question assumptions, seek evidence, acknowledge uncertainty
- **Reference**: `.fong/instructions/mindset-proof-by-contradiction-null-hypothesis-adversarial-validation-red-team-exploratory-testing.md`

**2. Autonomous Automation - No Quit Rule**
- **Full Automation**: Run → Debug → Verify → Fix → Until 100% FUNCTIONAL
- **NO QUIT RULE**: Once started, complete ENTIRE task without stopping or asking permission
- **Forbidden**: ❌ Stopping mid-task to ask confirmation | ❌ "Should I continue?" | ❌ Incomplete execution
- **Required**: ✅ Complete ALL identified tasks | ✅ Auto-proceed through steps | ✅ Only stop when 100% VERIFIED
- **Sandbox Execution**: Always work in sandbox branch, merge only on success
- **Reference**: `.fong/instructions/mindset-auto-run-auto-debug-auto-fix.md`

**3. Scientific Methodology**
- **Evidence-based**: Only empirical evidence accepted (logs, tests, metrics) - NOT "I think it works"
- **Closed-Loop**: Machine validates machine - no human approval until final success
- **Reproducibility**: Every change must be executable automatically (CLI-only, no GUI)
- **Traceability**: Every run has UUID - all artifacts tagged with run_id


---


### 🏗️ Development Principles


**1. Execution Strategy**


- **Think Big, Take Baby Steps**: Ambitious goals + incremental execution
  - Systematic WBS progression, break large tasks into small steps (2-min timeboxes in TDD)
  - **Strangler Fig Pattern**: Gradually replace legacy code by wrapping → redirecting → replacing
    - New features built separately on top of legacy (coexist temporarily)
    - Incremental migration reduces risk, allows constant monitoring
    - Eventually new system replaces old (like fig vine replacing host tree)
  - Revert immediately if tests fail (minimize "time in red")
  - Switch flexibly between big/small steps based on understanding
- **Measure Twice, Cut Once**: Analyze before action, verify before commit
- **Get Working First → Make Right → Make Fast** (if needed)

**2. Prioritization & Counting**
- **Quantity & Order**: Use MCP safe-calculation for counting tasks
- **Prerequisites First**: Dependencies → Critical → Simple
- **CRITICAL TASK VERIFICATION**:
  - COUNT total tasks using `mcp__safe-calculation__calculate(operation: 'count')`
  - VERIFY order is logical (prerequisites → critical → simple)
  - CROSS-CHECK count independently
  - Track during execution (task 3 of 10)
  - DOUBLE-CHECK completion (expected = actual)

**3. Verification**
- **Always Double-Check**: Never assume, always verify with tools
- **Cross-check + Double-check + MCP calculation**: Triple verification for critical operations
- **Self-Evaluate**: Did we fulfill ALL requirements? Missing anything?


---


### 💻 Code Standards


**1. Core Principles**
- **KISS** (Keep It Simple, Stupid): Avoid over-engineering
- **YAGNI** (You Aren't Gonna Need It): Don't implement until needed
- **SOLID**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **DRY** (Don't Repeat Yourself): Single source of truth
- **SSoT** (Single Source of Truth): One authoritative representation
- **Safety-First**: Always prioritize safest approach
- **Backward-Compat**: Maintain backward compatibility

**2. File Standards**
- **File Limits**: 100 LOC optimal, **120 max** (code only, exclude PHPDoc/JSDoc/comments) → refactor if exceeded
- **One Function Per File**: Each helper function has its own file
- **Naming**: kebab-case files, `de_` prefix for functions, `DE_` for constants
- **Security Header**: All PHP files: `if (!defined('ABSPATH')) exit;`

**3. Function Standards**
- **Always Return Values**: Arrays, strings, objects - NEVER false
- **No Reference Parameters**: Avoid pass-by-reference (&$param), use pure functions
- **Unit Test Ready**: Predictable input/output, no side effects

**4. Time Architecture (CRITICAL)**
- **NEVER** use system time functions: `time()`, `current_time()`, `date()`
- **ALWAYS** use: `de_time()` (Unix timestamp) and `de_time_mysql()` (MySQL DATETIME)
- **Why**: Mockable for testing, consistent across environments

**5. Memory Management (CRITICAL)**
- **NEVER** use `get_userdata()` in loops - causes memory exhaustion
- **ALWAYS** use bulk queries with JOIN for multiple users
- **Example**: 270 users × 2MB = 540MB → FATAL | Bulk query = 80MB

**6. Backup Before Edit (MANDATORY)**
```bash
timestamp=$(date +%Y%m%d_%H%M%S) && cp original_file "original_file.${timestamp}.b"
```
- **Pattern**: `*.{timestamp}.b`
- **Rule**: Every edit = Every backup (NO EXCEPTIONS)


---


### 🧮 Calculation & Verification


**1. Absolute Calculation Rule (🚨 CRITICAL)**
- **ZERO TOLERANCE** for mental arithmetic - AI WILL ERR
- **ALL calculations** via `mcp__safe-calculation__calculate`
- **Scope**: ALL math (2+2 → calculus) + counting (tasks, items, users, files, rows, arrays)
- **26 operations**: count, eval, uuid, random, stats, base_convert, complex_eval, matrix_op, vector_op, etc.
- **Enforcement**: If ANY calculation appears in reasoning → STOP → Use MCP tool → Proceed

**2. Reading Long Files Strategy**
- **Files >1000 lines**: Use sed/awk sliding window 5-10% chunks or grep/rg
- **Method**: `wc -l → calculate chunk → sed -n 'start,end p' → repeat`
- **Example**: `sed -n '1,100p' file` (read lines 1-100)


---


### 🔧 Tools & Workflow


**1. MCP Tools (HIGHEST PRIORITY - ALWAYS USE FIRST)**


**Search & Analysis:**
- **Smart Search**: `mcp__smart-search__smart-search`
  - Fallback: `/home/fong/Projects/smart-search-fz-rg-bm25/smart-search.sh` → `rg`


**Calculation & Math:**
- **Safe Calculation**: `mcp__safe-calculation__calculate` - NEVER mental arithmetic
  - Fallback: `.fong/instructions/instructions-mcp-safe-calculation-math-engine.md`


**Memory Management:**
- **mem0**: `mcp__ts-mem0-mcp__*` - ALWAYS for memory operations
  - Fallback: `.fong/instructions/instructions-mem0.md`
- **Fnote** (Obsidian/Notion): `mcp__fnote__*` - Unified note management
  - Fallback: `.fong/instructions/instructions-CRUD-obsidian-notes.md`


**Knowledge Sources (Query 80-90% of time - BEFORE-DURING-AFTER work):**
- **DKM NewRAG**: `mcp__dkm-knowledgebase__queryNewRAG` (hash-filtered, 190 books)
  - Fallback: `.fong/instructions/instructions-dkm-sources-knowledgebase.md`
- **Perplexity**: `mcp__dkm-knowledgebase__queryPerplexity` (latest practices)
  - Fallback: `.fong/instructions/fongperplexicity.md`
- **ArXiv**: `mcp__dkm-knowledgebase__queryArXiv` (academic papers)
  - Fallback: `.fong/instructions/instructions-arxiv-query.md`
- **Context7**: `mcp__context7__*` (library docs - ALWAYS FIRST for external libraries)
  - Note: MCP only, no fallback (library documentation tool)


**File Analysis (MUST use BEFORE editing):**
- **PHP**: `mcp__ts-php-reader__analyzePHPFile`
  - Fallback: `/home/fong/Projects/MCPs/ts-php-reader-mcp/README.md`
- **JavaScript/TypeScript**: `mcp__ts-ts-js-reader__analyzeTSJSFile`
  - Fallback: `/home/fong/Projects/MCPs/ts-ts-js-reader-mcp/README.md`
- **Python**: `mcp__ts-py-reader__analyzePythonFile`
  - Fallback: `/home/fong/Projects/MCPs/ts-py-reader-mcp/README.md`

**2. Modern CLI Rules**
- **NEVER** use `grep` → Use smart-search or fallback `rg` (ripgrep)  
- **NEVER** use `find` → Use `fd`
- **NEVER** use `cat` → Use `bat`
- **NEVER** use `ls` → Use `tree`
- **JSON**: Use `jq` for processing

**3. DKM Query Strategy (80-90% Philosophy)**


**🚨 CRITICAL: RAG Returns Fragmented Chunks - Need Systematic Thinking**


- **RAG Limitation**: Query returns isolated chunks (local view, fragmented context)
- **Required Mindset**: Systematic thinking to connect fragments → Think Ultra → Synthesize big picture
- **Quality Check**: Verify publication year - old books may be outdated, prioritize recent knowledge
- **Query Pattern**: SHORT (2-4 keywords), FREQUENT (3-7+ queries per task is NORMAL)
- **Query Timing**: BEFORE (planning) + DURING (implementation) + AFTER (verification)


**Query Frameworks (Use Both):**


1. **5W1H**: What (definition) + How (implementation) + Why (rationale) + Who (experts) + When (context) + Where (use cases)
2. **6 Thinking Hats** (Edward de Bono):
   - White Hat: Facts/Data (objective information)
   - Red Hat: Emotions/Intuition (gut feelings, instincts)
   - Black Hat: Risks/Problems (what can go wrong)
   - Yellow Hat: Benefits/Opportunities (optimistic view)
   - Green Hat: Creativity/Alternatives (new ideas, solutions)
   - Blue Hat: Process Control (meta-thinking, organize thinking)


**Iterative Strategy**: Query → Chunks → Think → Connect → Query again → Synthesize

**4. Search & Analysis**
- **Primary**: Smart Search (Hybrid Fuzzy + BM25) for intelligent searches
- **Fallback**: `rg` for fast exact matches
- **ALWAYS** search existing libraries BEFORE writing new code (DRY/SSoT)


---


### 🔒 Git & Safety


**1. Git Workflow**
- **ALWAYS** `git add .` (NEVER specific paths unless explicit permission)
- **NEVER** `git add -f` without permission (respect .gitignore)
- **Session Management**:
  - **Start**: `git commit -m "PREPARE: [description]"`
  - **During**: Commit frequently
  - **End**: `git commit -m "COMPLETE: [description]" && git push`
  - **Emergency**: `git add . && git commit -m "EMERGENCY: Session interrupted"`

**2. Sandbox Isolation**
- **Create Sandbox**: `sandbox-YYYYMMDD-HHMMSS` branch
- **Work in Isolation**: All changes in sandbox
- **Merge on Success**: Gates pass → merge to main
- **Rollback on Failure**: Delete sandbox branch, main unchanged

**3. Debug Standards**
- **Hard-coded UUID**: `uuidgen` → Use in debug calls (NEVER dynamic generation)
- **dbug() Pattern**: `dbug("Description - $debug_id", $data)`
- **Primary Log**: `wp-content/plugins/fong_de_lms/debug/logs/fong-debug-php.jsonl`
- **Remove Before Production**: All debug calls cleaned before deployment


---


### 📝 Memory & Documentation


**1. Memory Management**
- **Location**: `.fong/.memory/` ONLY (flat structure, NO subdirectories)
- **Dual Persistence**: Sync `.memory/` with mem0 MCP for cross-session continuity
- **CRUD Pattern**: R → C → U → D (Always READ before CREATE)
- **File Size**: <50 LOC per file (optimal for AI context)
- **Alignment**: Update BOTH `.memory/` AND mem0 (before-during-after work)

**2. Hyperfocus System**
- **UPDATE FREQUENTLY**: On start task, progress, switch focus, complete
- **ONE-EDIT-PER-PROMPT RULE**: If edited in current prompt → SKIP further edits → Next prompt edits again
- **context_folders**: MAX 3 folders (sorted by priority) - User works max 3 tasks in parallel

**3. Markdown Documentation**
- **YAML Metadata**: REQUIRED at top (title, date, version, author, purpose, keywords)
- **NO H1 in content**: Title ONLY in YAML
- **Max 3 Heading Levels**: H2 (##) main, H3 (###) sub - NO H4
- **Spacing**: 2 newlines after headers
- **NO Emoji**: Professional text only (unless explicitly requested)

**4. Prompt Processing**
- **User sends unordered requests**: AI MUST reorganize using Think Ultra
- **Reorder for logical causality**: Dependencies first → then execution
- **Focus on USEFUL OUTPUT**: Not literal request following


---


**Nhớ:**

- **Be a Smart/Clever Context Engineer**: "Chỉ đọc vừa đủ để giải quyết task - Pareto. Tiết kiệm lượng token input hợp lý bằng nhiều kĩ thuật thông minh, với ultrathink, very smart linux command, ứng dụng triệt để toán học và thuật toán, xác xuất thống kê,... để đạt được mục đích".

- **Luôn align vào .memory trong quá trình (nhiều lần) - sau (1 lần cuối)**:
  - Đảm bảo `.memory/*` phải SSoT & DRY và align/phản ánh đúng với thực tế

- **Luôn dùng Ts-mem0-mcp MCP**:
  - Hoặc `.fong/instructions/instructions-mem0.md` để CRUD/align với memory ở mem0 trước-trong-sau khi làm. 

- **Luôn update hyperfocus.json thường xuyên**:
  - ⚠️ **CRITICAL**: hyperfocus.json cần UPDATE FREQUENTLY (mỗi khi start task, progress, complete, switch focus)
  - ⚠️ **ONE-EDIT-PER-PROMPT RULE**: Nếu đã edit hyperfocus.json trong prompt hiện tại → SKIP edit tiếp trong cùng prompt → Prompt tiếp theo sẽ edit lại
  - **context_folders**: MAX 3 folders (sorted by priority) - User làm song song max 3 tasks
  - **when section**: ĐÃ BỎ khỏi hyperfocus.json - Thông tin now/branch/timezone lấy từ script output ONLY

- **Luôn add + commit + push trước-trong-sau**:
  - Đảm bảo code luôn bảo toàn
  - Tuyệt đối KHÔNG `git add -f*`

- **Luôn tham khảo nguồn kiến thức ngoài**:
  - Nghĩa là hỏi trước và trong khi làm, chứ không chỉ hỏi 1 lần
  - Đọc rule: `.fong/instructions/instructions-dkm-sources-knowledgebase.md`
  - Nên hỏi theo framework `5w1h`, không nên chỉ hỏi về `what` mà còn nên hỏi thêm về `how`
  - Ví dụ hỏi về: Mindset (tư duy), Methodology (phương pháp), Expert Opinion (ý kiến chuyên gia), Trade-offs (đánh giá), Kiến thức thuần túy, Code generation...
