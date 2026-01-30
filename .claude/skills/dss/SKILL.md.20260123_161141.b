---
name: dss
description: This skill should be used when the user asks to "research", "investigate", "survey", "khảo sát", "tìm hiểu", "decision support", uses {DSS}, {DSS5}, {DSS7}, or needs multi-source verification before action.
version: 1.0.0
user-invocable: true
disable-model-invocation: false
instructions_source: /home/fong/Projects/dropbox-obsidian/FongObsidian/.fong/instructions/instructions-DSS-decision-support-system.md
---

# DSS - Decision Support System Skill

Khảo sát đa nguồn với output .md chuẩn citation footnote.

**CRITICAL - MANDATORY FIRST ACTION**:
```
READ /home/fong/Projects/dropbox-obsidian/FongObsidian/.fong/instructions/instructions-DSS-decision-support-system.md
```
Use Read tool with ABSOLUTE PATH. Do NOT skip this step.

## Core Concept

DSS = Decision Support System. Query ≥3 sources. Synthesize. Decide.
Gut feeling ≠ evidence. DSS output = evidence.

## Protocol Selection

| Protocol | Trigger Keywords | Min Tools |
|----------|-----------------|-----------|
| **{DSS5}** | fix, build, implement, code | 5 tools |
| **{DSS7}** | research, paper, thesis, academic | 7 tools |

## DSS5 Tools (Non-Academic) - BẮT BUỘC ĐỦ 5

| # | Tool | MCP | Fallback |
|---|------|-----|----------|
| 1 | NewRAG | `mcp__dkm-knowledgebase__queryNewRAG` | `/home/fong/Projects/mini-rag/run.sh "query"` |
| 2 | Perplexity | `mcp__dkm-knowledgebase__queryPerplexity` | - |
| 3 | Gemini | - | `.fong/instructions/instructions-google-gemini-cli/gemini-rcifeni-o.sh` |
| 4 | Copilot | `mcp__dkm-knowledgebase__queryCopilot` | `.fong/instructions/instructions-github-copilot-cli/copilot-free.sh` |
| 5 | Z.AI | `mcp__mcp-zai__chinese-zai` | - |

## DSS7 Tools (Academic) - BẮT BUỘC ĐỦ 7

| # | Tool | MCP | Fallback |
|---|------|-----|----------|
| 1-5 | (DSS5 tools) | (như trên) | (như trên) |
| 6 | ArXiv | `mcp__dkm-knowledgebase__queryArXiv` | `/home/fong/Projects/arxiv-searcher/arxiv-searcher.sh "query"` |
| 7 | SLR | - | `/home/fong/Projects/slr-paper-downloader/slr.sh "query"` |
| + | Context7 | `mcp__context7__resolve-library-id` | - (coding only) |

## Retry Mechanism (MANDATORY)

**Rule:** Mỗi tool PHẢI retry tối thiểu 3 lần trước khi chuyển sang fallback.

### Retry Strategy

| Attempt | Wait | Action |
|---------|------|--------|
| 1 | 0s | First try |
| 2 | 3s | Retry after timeout/error |
| 3 | 5s | Final retry with exponential backoff |
| Fail | - | Use fallback script |

### Retry Workflow

```
╔═══════════════════════════════════════════════════════════╗
║  FOR each tool in DSS{5|7}:                               ║
║    attempt = 0                                            ║
║    WHILE attempt < 3:                                     ║
║      TRY: Call MCP tool                                   ║
║      IF success → BREAK                                   ║
║      IF error (timeout, ETIMEDOUT, connection):           ║
║        attempt++                                          ║
║        WAIT: 3s (attempt 2) or 5s (attempt 3)             ║
║        LOG: "Retry {attempt}/3 for {tool}"                ║
║    IF all 3 failed → USE FALLBACK SCRIPT                  ║
║    LOG: "Using fallback for {tool}"                       ║
╚═══════════════════════════════════════════════════════════╝
```

### Error Types to Retry

| Error | Retry? | Example |
|-------|--------|---------|
| ETIMEDOUT | ✅ Yes | `spawnSync /bin/bash ETIMEDOUT` |
| Connection timeout | ✅ Yes | MCP server not responding |
| Exit code 1 | ✅ Yes | Script error, may be transient |
| Invalid response | ✅ Yes | Empty or malformed response |
| Auth error | ❌ No | API key invalid (fix config) |
| Not found | ❌ No | Tool/script doesn't exist |

### Fallback Scripts (khi 3 retries fail)

| Tool | MCP | Fallback Script |
|------|-----|-----------------|
| NewRAG | `mcp__dkm-knowledgebase__queryNewRAG` | `/home/fong/Projects/mini-rag/run.sh "query"` |
| Perplexity | `mcp__dkm-knowledgebase__queryPerplexity` | ❌ No fallback (MCP only) |
| Gemini | N/A | `/home/fong/Projects/dropbox-obsidian/FongObsidian/.fong/instructions/instructions-google-gemini-cli/gemini-rcifeni-o.sh` |
| Copilot | `mcp__dkm-knowledgebase__queryCopilot` | `/home/fong/Projects/dropbox-obsidian/FongObsidian/.fong/instructions/instructions-github-copilot-cli/copilot-free.sh "prompt"` |
| Z.AI | `mcp__mcp-zai__chinese-zai` | ❌ No fallback (MCP only) |
| ArXiv | `mcp__dkm-knowledgebase__queryArXiv` | `/home/fong/Projects/arxiv-searcher/arxiv-searcher.sh "query"` |
| SLR | N/A | `/home/fong/Projects/slr-paper-downloader/slr.sh "query"` |

### Gemini CLI Correct Usage

```bash
# ĐÚNG: Dùng named parameters
/home/fong/.fong/instructions/instructions-google-gemini-cli/gemini-rcifeni-o.sh \
  -r "Expert Role" \
  -c "Context here" \
  -i "Instructions" \
  -f "Output format" \
  -I "Actual input/question" \
  -o "OKR"

# SAI: Positional argument
gemini-rcifeni-o.sh "Role: Expert..." ← WRONG!
```

### Logging Format

```
[DSS] Tool: NewRAG | Attempt: 1/3 | Status: TIMEOUT
[DSS] Tool: NewRAG | Attempt: 2/3 | Wait: 3s | Status: TIMEOUT
[DSS] Tool: NewRAG | Attempt: 3/3 | Wait: 5s | Status: TIMEOUT
[DSS] Tool: NewRAG | FALLBACK: /home/fong/Projects/mini-rag/run.sh
[DSS] Tool: NewRAG | FALLBACK: SUCCESS
```

---

## Critical Rules

1. **NEVER single-source answer** - Always ≥3 sources, ≥2 agree
2. **NEVER mental math** - Use `mcp__safe-calculation__calculate`
3. **OUTPUT MUST be .md file** - With footnote citations `[^1]`
4. **Aphoristic output** - Request `output_format: "Aphoristic. 1 line = 1 idea."`
5. **ALWAYS retry 3x** - Before fallback. Log each attempt.

## Output Workflow (IMMUTABLE)

```
╔═══════════════════════════════════════════════════════════╗
║  1. SELECT PROTOCOL: DSS5 or DSS7                         ║
║  2. QUERY SOURCES: In priority order                      ║
║  3. SYNTHESIZE: Cross-verify, resolve conflicts           ║
║  4. OUTPUT FILE: .md with footnote citations              ║
║  5. VERIFY: ≥2 sources agree → publish                    ║
╚═══════════════════════════════════════════════════════════╝
```

## Query Pattern

**Style:** SHORT (2-4 words). SPECIFIC. MULTIPLE.
**Rule:** Mỗi tool query **3 lần** với các góc nhìn khác nhau (5W1H + 6 Thinking Hats)

### Multi-Query Strategy (3x per tool)

Ref: `.fong/instructions/mindsets/mindset-brainstorm-5w1h-6-thinking-hats.md`

| Query # | Góc nhìn | Ví dụ (topic: "Chi phí PhD") |
|---------|----------|------------------------------|
| 1 | **WHAT** (White Hat - Facts) | "chi phí học phí PhD" |
| 2 | **WHY/HOW** (Yellow Hat - Benefits) | "lợi ích đầu tư PhD" |
| 3 | **RISKS** (Black Hat - Caution) | "rủi ro tài chính PhD" |

### 5W1H Framework cho Query

| Aspect | Query Template |
|--------|----------------|
| **What** | "{topic} definition", "{topic} components" |
| **Why** | "why {topic} important", "benefits {topic}" |
| **How** | "how to {topic}", "step-by-step {topic}" |
| **When** | "timeline {topic}", "when {topic}" |
| **Where** | "{topic} locations", "{topic} sources" |
| **Who** | "experts {topic}", "stakeholders {topic}" |

### 6 Thinking Hats cho Query

| Hat | Focus | Query Style |
|-----|-------|-------------|
| 🎩 White | Facts & Data | "{topic} statistics", "{topic} numbers" |
| 🎩 Red | Emotions | "concerns about {topic}", "feelings {topic}" |
| 🎩 Black | Risks | "risks {topic}", "problems {topic}" |
| 🎩 Yellow | Benefits | "benefits {topic}", "advantages {topic}" |
| 🎩 Green | Alternatives | "alternatives {topic}", "options {topic}" |
| 🎩 Blue | Process | "how to decide {topic}", "framework {topic}" |

### Example: DSS5 với 3x Query mỗi tool

```python
# Tool 1: NewRAG (3 queries)
queryNewRAG(["chi phí học phí PhD", "nguồn tài trợ PhD", "học bổng PhD VN"])

# Tool 2: Perplexity (3 queries)
queryPerplexity("chi phí PhD CS Việt Nam 2024")
queryPerplexity("so sánh chi phí PhD trong nước vs nước ngoài")
queryPerplexity("học bổng PhD computer science 2025")

# Tool 3: Gemini (3 queries)
gemini("phân tích chi phí-lợi ích PhD")
gemini("rủi ro tài chính khi học PhD")
gemini("timeline hoàn vốn đầu tư PhD")

# ... tương tự cho Copilot, Z.AI
```

**Total queries DSS5:** 5 tools × 3 queries = **15 queries minimum**
**Total queries DSS7:** 7 tools × 3 queries = **21 queries minimum**

## Output Location

**Default folder:** `.fong/docs/dss-output-{YYYYMMDD-HHMMSS}/`
**Override:** User-specified path

**Output files trong folder:**

| File | Mục đích |
|------|----------|
| `{topic}-research.md` | Research output với footnotes |
| `{topic}-research.pdf` | PDF export via Textor |
| `{topic}-deep-research-prompt.md` | Prompt RCIFENI-O cho Deep Research tools |

---

## Output File Template

**Filename:** `{topic}-research.md`

```markdown
---
title: "{Topic} Research"
date: "{YYYY-MM-DD}"
protocol: "DSS5|DSS7"
sources_used: N
---

# {Topic}

## Tóm tắt

[Summary here][^1]

## Phân tích chi tiết

### Khía cạnh 1

Content với citation[^2].

### Khía cạnh 2

Content[^3].

## Kết luận

Final synthesis[^4].

---

[^1]: Source1 (Year). Title. Publisher/URL.

[^2]: Source2 (Year). Title. arXiv:XXXX.

[^3]: NewRAG query: "keyword". DKM-BookName.pdf.P##.

[^4]: Perplexity (2026-01-23). Query: "keyword".
```

## Citation Format (Footnote - MANDATORY)

**In text:**
```markdown
Nghiên cứu cho thấy kết quả quan trọng[^1]. Nguồn khác xác nhận[^2].
```

**End of file:**
```markdown
[^1]: Author (Year). Title. Publisher, p.XX.

[^2]: NewRAG: DKM-CleanCode-2008.pdf.P145.

[^3]: Perplexity (2026-01-23). Query: "clean architecture patterns".

[^4]: ArXiv: Author (Year). Title. arXiv:XXXX.XXXXX.
```

## Consensus Rule

| Sources Agree | Action |
|---------------|--------|
| ≥2 agree | Publish |
| Conflict | Investigate more |
| 1 only | NOT sufficient |

## Additional Resources

### Reference Files
- **`references/patterns.md`** - DSS query patterns
- **`references/citation-examples.md`** - Citation format examples

### Example Files
- **`examples/dss5-workflow.md`** - DSS5 example output
- **`examples/dss7-academic.md`** - DSS7 academic example

## Local Documentation (ABSOLUTE PATHS)

**Master Instructions:**
```
Read tool → /home/fong/Projects/dropbox-obsidian/FongObsidian/.fong/instructions/instructions-DSS-decision-support-system.md
```

**Related files:**
- `/home/fong/Projects/dropbox-obsidian/FongObsidian/.fong/instructions/instructions-do-take-note-stick-the-plan-professor-v2.json`
- `/home/fong/Projects/dropbox-obsidian/FongObsidian/.fong/instructions/textor-mdlatex/12-footnote-citation.md`

## Pre-Prompt Template (RCIFENI-O)

Khi user invoke `/dss`, AI PHẢI output response theo format sau:

```
`Think BIG, DO small steps`, `step by step`. Best effort to `get things done`. ULTRATHINK activated.
Skill: /dss | Protocol: {DSS5|DSS7}
{YYYY-MM-DD HH:MM:SS} (+07)

# 1. Role:
DSS Researcher + Evidence Synthesizer

# 2. Context:
Topic: {user's topic}
Protocol: {DSS5 or DSS7}
Output: .md file with footnote citations

# 3. Instructions:
1. Query ≥{5|7} sources in priority order
2. Cross-verify: ≥2 sources agree
3. Synthesize findings
4. Output .md with [^N] citations

# 4. Output Format:
- File: {YYYY-MM-DD}-{topic}-research.md
- Footnote citations [^1], [^2]...
- Aphoristic style. 1 line = 1 idea.

# 5. Cautions:
- anti: Single-source answer
- anti: Mental math (use Safe Math MCP)
- anti: Missing citations
- anti: Verbose output (use aphoristic)

# 6. OKR:
O: Research {topic} với multi-source verification
KR1: Query ≥{5|7} tools
KR2: ≥2 sources agree on key findings
KR3: Output .md with proper footnote citations
```

---

## AI Workflow

**⚠️ STEP 0 - MANDATORY FIRST (Zero Skip):**
```
Read tool → /home/fong/Projects/dropbox-obsidian/FongObsidian/.fong/instructions/instructions-DSS-decision-support-system.md
```

1. **Print Pre-Prompt** → Show RCIFENI-O template above
2. **Nhận prompt** → Xác định DSS5 hoặc DSS7
3. **Create output folder**: `.fong/docs/dss-output-{YYYYMMDD-HHMMSS}/` (hoặc user-specified)
4. **Query sources** (BẮT BUỘC - **3x mỗi tool** + **3 retries mỗi call**):
   ```
   FOR each tool:
     FOR each query (3 queries per tool):
       attempt = 0
       WHILE attempt < 3:
         TRY MCP tool
         IF success → next query
         IF fail → wait (3s/5s) → retry
       IF 3 fails → use fallback script
   ```
   - DSS5: NewRAG(3) → Perplexity(3) → Gemini(3) → Copilot(3) → Z.AI(3) = **15 queries**
   - DSS7: + ArXiv(3) + SLR(3) = **21 queries**
   - **Max attempts per tool**: 3 queries × 3 retries = **9 attempts**
5. **Cross-verify** → ≥2 sources agree
6. **Create `{topic}-research.md`** với footnote citations
7. **Create `{topic}-deep-research-prompt.md`** theo RCIFENI-O format
8. **Verify** citations đầy đủ, format đúng
9. **Export PDF** via Textor → `{topic}-research.pdf`

**Output folder structure:**
```
.fong/docs/dss-output-{YYYYMMDD-HHMMSS}/
├── {topic}-research.md           # Main research output
├── {topic}-research.pdf          # PDF export
├── {topic}-deep-research-prompt.md  # RCIFENI-O prompt for Deep Research tools
└── {topic}-research_img/         # (nếu có diagrams)
```

---

## Textor PDF Export (MANDATORY)

**Ref:** `.fong/instructions/textor-mdlatex/*`

Sau khi tạo file .md → PHẢI export PDF:

```bash
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"{output-file}.md"}'
```

**Output:**
- `{output-file}.pdf` - PDF file
- `{output-file}_img/` - Embedded images (nếu có diagrams)

**Critical Rules (từ textor):**
1. YAML frontmatter bắt buộc
2. No emoji in content
3. Max heading level: H3 (###)
4. LaTeX math: `$...$` hoặc `$$...$$`
5. Footnotes: `[^1]` format

**Textor Docs:**
- Entry: `.fong/instructions/textor-mdlatex/00-instructions-textor-doc-converter-mermaid-plantuml-mdlatex.md`
- Citation: `.fong/instructions/textor-mdlatex/12-footnote-citation.md`

---

## Deep Research Prompt (MANDATORY)

**Ref:** `.fong/instructions/instructions-rcifeni-o-prompt-engineering.md`

Tạo file `{topic}-deep-research-prompt.md` theo chuẩn RCIFENI-O để dùng với:
- Perplexity Pro (Deep Research mode)
- Gemini Deep Research
- ChatGPT Deep Research
- Các tool có Deep Research capability

### Template: `{topic}-deep-research-prompt.md`

```markdown
---
title: "Deep Research Prompt: {Topic}"
date: "{YYYY-MM-DD}"
format: "RCIFENI-O"
target_tools: ["Perplexity Pro", "Gemini Deep Research", "ChatGPT Deep Research"]
---

# Deep Research Prompt: {Topic}

## 1. Role (-r) [MANDATORY]

{Domain} expert với deep research capability.
Ví dụ: "PhD-level researcher specializing in {topic}"

## 2. Context (-c) [MANDATORY] (5W1H)

**What:** Nghiên cứu về {topic}
**Why:** {Mục đích - từ OKR của user}
**When:** Thông tin cập nhật đến {current year}
**Where:** Global context với focus {region nếu có}
**Who:** Target audience: {user type}
**How:** Multi-source triangulation với deep analysis

**Background:**
{Context từ research đã làm - summary từ file output}

**Constraints:**
- Yêu cầu academic-level citations
- Verify từ primary sources
- Cross-reference multiple perspectives

## 3. Instructions (-i) [MANDATORY]

1. Tìm kiếm comprehensive về {topic}
2. Phân tích từ multiple perspectives (5W1H)
3. Cross-verify thông tin từ ≥3 sources
4. Identify gaps và contradictions
5. Synthesize findings với citations
6. Provide actionable insights

## 4. Format (-f) [MANDATORY]

- Structured report với headings
- Tables cho so sánh
- Bullet points cho key findings
- Citations với source URLs
- Summary section đầu và cuối

## 5. Example (-e) [OPTIONAL]

{Ví dụ output mong muốn nếu có}

## 6. Notices/Cautions (-n) [SUGGESTED]

- Verify dates (thông tin phải current)
- Cross-check statistics từ official sources
- Identify potential biases trong sources
- Note conflicting information

## 7. OKRs (-o) [MANDATORY]

**Objective:** {O từ user request}

**Key Results:**
- KR1: {Measurable result 1}
- KR2: {Measurable result 2}
- KR3: {Measurable result 3}

## 8. Input (-I) [MANDATORY]

<<< INPUT:

{Topic và specific questions từ user}

**Key questions to answer:**
1. {Question 1 - WHAT}
2. {Question 2 - WHY}
3. {Question 3 - HOW}
4. {Question 4 - RISKS}
5. {Question 5 - ALTERNATIVES}
```

### Deep Research Tools

| Tool | Mode | Link |
|------|------|------|
| Perplexity | Pro Search / Deep Research | perplexity.ai |
| Gemini | Deep Research | gemini.google.com |
| ChatGPT | Deep Research | chat.openai.com |

**Usage:** Copy nội dung file prompt → Paste vào Deep Research tool
