---
name: write-paper
description: This skill should be used when the user asks to "write paper", "write academic paper", "viet bai bao", "viet luan van", "research paper", "Q1 paper", "journal article", uses {write-paper}, {paper}, or needs structured academic writing workflow.
version: 2.0.0
user-invocable: true
disable-model-invocation: false
instructions_source: .fong/instructions/academic/
latex_instructions: .fong/instructions/LaTeX/
dss_instructions: .claude/skills/dss/SKILL.md
professor_v2: .fong/instructions/instructions-do-take-note-stick-the-plan-professor-v2.json
manifest: .claude/skills/write-paper/manifest.json
output_language: Vietnamese
---

# Write Paper - Agile-Kaizen Academic Writing

Viết bài báo học thuật theo workflow agile. Skeleton first. Query while writing. Fill as you go.

**Philosophy:** Có gì làm đó. Không đợi đủ mới làm. Vừa làm vừa đắp. Hướng về mục tiêu.


---


## MANDATORY FIRST ACTIONS (Zero Skip)

```
READ .claude/skills/write-paper/manifest.json
READ .fong/instructions/academic/scientific-plain-vietnamese-checklist.md
READ .fong/instructions/LaTeX/00-latex-principles.md
READ .fong/instructions/instructions-do-take-note-stick-the-plan-professor-v2.json
```


---


## Core Concept

| Principle | Description |
|-----------|-------------|
| **Skeleton First** | Tạo khung LaTeX trước. Fill content sau. |
| **Query While Writing** | DSS query TRONG KHI viết. Không chỉ trước khi viết. |
| **One Section at a Time** | Viết 1 section → Commit → Next section. |
| **Wrong Draft > No Draft** | Draft sai tốt hơn không có draft. Sửa sau. |
| **Good Enough > Perfect** | 85% hoàn thiện > 100% không bao giờ xong. |


---


## WP6: 6-Phase Agile Workflow

| Phase | Name | Goal | Output |
|-------|------|------|--------|
| **WP0** | CONJECTURE | Form hypotheses + OKR | Plan file JSON |
| **WP1** | INVESTIGATE | DSS query, literature | Evidence map |
| **WP2** | SKELETON | Create LaTeX structure | main.tex + sections/ |
| **WP3** | FILL | Write sections (Methods first) | Draft sections |
| **WP4** | REFINE | Red Team + DSS verify | Polished draft |
| **WP5** | SUBMIT | Final check + package | Submission-ready |


---


## WP0: CONJECTURE (Plan File)

**Goal:** Tạo plan file JSON với OKR + Topic + Hypotheses.

**Location:** `.fong/docs/plans/plan-paper-{short-title}-{YYYYMMDD}.json`

**Required Sections:**

```json
{
  "meta": {"title": "", "target_journal": "", "status": "draft"},
  "okr": {"objective": "...", "key_results": ["KR1", "KR2", "KR3"]},
  "topic": {
    "research_question": "...",
    "gap_statement": "...",
    "contribution": "..."
  },
  "hypotheses": [
    {"id": "H1", "confidence": "H", "statement": "...", "status": "proposed"}
  ],
  "5w1h": {"what": "", "why": "", "where": "", "when": "", "who": "", "how": ""}
}
```

**Mindsets:** `{brainstorm}`, `{5w1h}`


---


## WP1: INVESTIGATE (DSS Query)

**Goal:** Gather evidence. Map to hypotheses.

**Protocol:** DSS7 (academic = 7 sources minimum)

**Query Pattern:**

```
queryNewRAG: ["{topic} methodology", "{topic} literature"]
queryPerplexity: "{topic} research gap 2026"
queryArXiv: "{topic}" (recent papers)
queryCopilot: Cross-check findings
```

**Rule:** Query 3x mỗi tool. Map evidence to H1, H2, H3.

**Mindsets:** `{evidence first}`, `{double check}`


---


## WP2: SKELETON (LaTeX Structure)

**Goal:** Tạo khung LaTeX. Chưa cần nội dung.

**File Naming Convention (MANDATORY):**

```
{năm}-{tên-bài-os-friendly}-{tác-giả}.tex
```

| Component | Rule | Example |
|-----------|------|---------|
| **năm** | 4 digits | `2026` |
| **tên-bài** | lowercase, hyphen, OS-safe | `gwfe-vs-moodle-bayesian` |
| **tác-giả** | lowercase, hyphen | `anhnam`, `nguyen-tran` |

**Examples:**
- `2026-gwfe-vs-moodle-bayesian-anhnam.tex`
- `2026-tam-utaut-comparison-nguyen.tex`
- `2025-deep-learning-education-tran-le.tex`

**NEVER use:** `main.tex`, spaces, Vietnamese diacritics in filename.

**Folder Structure:**

```
LaTeX/
├── {năm}-{tên-bài}-{tác-giả}.tex   # Entry point (XeLaTeX)
├── sections/
│   ├── 01-introduction.tex
│   ├── 02-literature.tex
│   ├── 03-methodology.tex
│   ├── 04-results.tex
│   ├── 05-discussion.tex
│   └── 06-conclusion.tex
├── figs/                 # Vector (PDF/SVG) or PNG >=300dpi
├── bib/
│   └── references.bib
├── build.sh              # XeLaTeX build (--quick, --full, --clean)
└── watch.sh              # Auto-rebuild with threshold
```

**Template Priority:**

1. Journal official template (REQUIRED if available)
2. elsarticle, IEEEtran, acmart
3. `.fong/instructions/LaTeX/templates/`

**Build Command:**

```bash
# Quick build (1 pass, no bibliography)
./build.sh --quick

# Full build (3 passes + bibtex)
./build.sh --full

# Watch mode with threshold (auto-rebuild)
./watch.sh --quick
```

**XeLaTeX Required (Vietnamese):**
- Engine: `xelatex` (NOT pdflatex)
- Fonts: `fontspec` + `polyglossia`
- Font family: `TeX Gyre Termes` (Times equivalent, full Unicode)

**Mindsets:** `{agile}`, `{checklist}`


---


## Autodebug PDF (Post-Build Verification)

**Philosophy:** Machine validates machine. No "I think it works."

**Workflow:**

```
BUILD → PDF → PNG (random pages) → AI visual check → Pass/Fail
```

**Implementation:**

```bash
# Convert PDF to PNG (specific page or random)
pdftoppm -png -r 150 -f $PAGE -l $PAGE output.pdf /tmp/page

# Random page selection
TOTAL_PAGES=$(pdfinfo output.pdf | grep Pages | awk '{print $2}')
RANDOM_PAGE=$((RANDOM % TOTAL_PAGES + 1))
```

**Verification Checklist:**

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Vietnamese diacritics | Visual | All dấu hiển thị đúng |
| Figures rendered | Visual | No broken images |
| Tables aligned | Visual | Columns proper |
| Math formulas | Visual | Symbols correct |
| Page numbers | Visual | Sequential |
| Bibliography | Visual | Citations resolved |

**Auto-check Strategy:**

| Paper Size | Pages to Check |
|------------|----------------|
| 1-5 pages | All pages |
| 6-12 pages | 3 random + first + last |
| 13+ pages | 5 random + first + last |

**Mindsets:** `{auto debug}`, `{no quit}`


---


## WP3: FILL (Write Sections)

**Goal:** Viết từng section. Query DSS trong khi viết.

**Section Order (MANDATORY):**

| Order | Section | Focus |
|-------|---------|-------|
| 1st | Methods | Replicable. Parameters. Software versions. |
| 2nd | Results | Primary finding first. Numbers. Effect size. |
| 3rd | Discussion | Interpret. Compare. Limitations. |
| 4th | Introduction | Gap. Contribution. Structure. |
| 5th | Conclusion | Brief. No repeat. Future work. |
| **LAST** | Abstract | Write AFTER paper done. 150-300 words. |

**Agile Loop (per section):**

```
Draft section → Query DSS (gaps?) → Refine → Commit → Next section
```

**Writing Rules:**

- 1 paragraph = 1 job. Topic sentence first.
- Văn xuôi liên mạch. Không bullet points trong body.
- Mỗi khẳng định có trích dẫn.
- Số liệu thay tính từ ("15.4%" không phải "tăng mạnh").
- Hedging: "suggests", "indicates", not "proves".

**Mindsets:** `{no skip}`, `{agile}`


---


## WP4: REFINE (Red Team + Verify)

**Goal:** Attack own work. Verify numbers. Polish language.

**Red Team Protocol:**

```
H₀ = "This section is WRONG"
Attack: 5W1H + 3 Levels
Verify: Numbers, claims, citations
```

**Verification Checklist:**

- [ ] All claims cited?
- [ ] Numbers verified (Safe Math MCP)?
- [ ] Terminology consistent?
- [ ] Grammar/spelling checked?

**Mindsets:** `{red team}`, `{double check}`


---


## WP5: SUBMIT (Final Package)

**Goal:** Prepare submission-ready package.

**Checklist (21 items):**

**Kill Items (abort if fail):**

- [ ] FFP verified? (No Fabrication, Falsification, Plagiarism)
- [ ] Data real & unmodified?
- [ ] Reproducibility ensured?

**Standard Items:**

- [ ] Journal guidelines read?
- [ ] Word/page limit OK?
- [ ] All figures high quality?
- [ ] Bibliography complete?
- [ ] Cover letter written?
- [ ] Data availability stated?
- [ ] PDF compiles without errors?

**Mindsets:** `{checklist}`, `{safety first}`


---


## Research Ethics (CRITICAL)

**FFP Rule (Zero Tolerance):**

| Code | Violation | Consequence |
|------|-----------|-------------|
| **F** | Fabrication | ABORT paper |
| **F** | Falsification | ABORT paper |
| **P** | Plagiarism | ABORT paper |

**Reproducibility Requirements:**

| Requirement | Evidence |
|-------------|----------|
| Data availability | DOI, repository link |
| Code availability | GitHub, Zenodo URL |
| Software versions | R 4.3.2, Python 3.11, etc. |
| Random seeds | set.seed(12345) |


---


## DSS Integration

**Protocol:** DSS7 (academic tasks)

**Query Timing:** DURING writing, not just BEFORE

| Phase | DSS Tools |
|-------|-----------|
| WP0-WP1 | NewRAG, Perplexity, ArXiv |
| WP2-WP3 | NewRAG (writing guides), Copilot |
| WP4 | Safe Math, Red Team, Copilot |
| WP5 | Perplexity (journal policies) |

**Rule:** Query >= 3 per section. Total >= 21 queries per paper.


---


## Pre-Prompt Template (RCIFENI-O)

Khi invoke `/write-paper`:

```
`Think BIG, DO small steps`, `step by step`. ULTRATHINK activated.
Skill: /write-paper | Protocol: WP6 (6 phases)
{YYYY-MM-DD HH:MM:SS} (+07)

# 1. Role:
Academic Paper Writer + Agile Researcher

# 2. Context:
Topic: {topic}
Target Journal: {journal}
Protocol: WP6 (Conjecture → Investigate → Skeleton → Fill → Refine → Submit)

# 3. Instructions:
1. Create plan file JSON (WP0)
2. DSS query (WP1)
3. Create LaTeX skeleton (WP2)
4. Fill sections one by one (WP3)
5. Red Team + verify (WP4)
6. Prepare submission (WP5)

# 4. Output Format:
- Plan: .fong/docs/plans/plan-paper-{title}-{date}.json
- Paper: paper-{title}/ folder with LaTeX

# 5. Cautions:
- anti: FABRICATION → ABORT
- anti: FALSIFICATION → ABORT
- anti: PLAGIARISM → ABORT
- anti: Write abstract first (LAST only)
- anti: Mental math (use Safe Math)
- anti: Single-source claims (use DSS7)

# 6. OKR:
O: Write {topic} paper for {journal}
KR1: Complete all 6 phases
KR2: LaTeX compiles without errors
KR3: All claims cited and numbers verified
```


---


## AI Workflow

**STEP 0 - MANDATORY FIRST:**

```
Read tool → .claude/skills/write-paper/manifest.json
Read tool → .fong/instructions/instructions-do-take-note-stick-the-plan-professor-v2.json
```

1. **Print Pre-Prompt** → RCIFENI-O template
2. **WP0: Create plan file** → JSON with OKR + Topic + Hypotheses
3. **WP1: DSS query** → Evidence map
4. **WP2: Create skeleton** → LaTeX structure
5. **WP3: Fill sections** → One by one, commit each
6. **WP4: Red Team** → Verify numbers, claims
7. **WP5: Submit** → Final package
8. **Commit** → `{git flow}`


---


## Code Rules (R/Python)

**Philosophy:** Modular. JSON-driven. One entry point.

**Core Rules:**

| Rule | Description |
|------|-------------|
| **<100 LOC** | Mỗi file <100 dòng code. Split if larger. |
| **JSON data** | Raw → Clean → JSON. Không CSV trong final. |
| **JSON config** | Parameters trong config/parameters.json |
| **init.sh** | Entry point duy nhất. Chạy 1 lần cho tất cả. |
| **CUD colors** | Dùng Okabe-Ito palette cho mọi plots. |

**CUD Color Palette (MANDATORY):**

```r
# R
cud_colors <- c(
  black = "#000000", orange = "#E69F00", skyblue = "#56B4E9",
  bluishgreen = "#009E73", yellow = "#F0E442", blue = "#0072B2",
  vermilion = "#D55E00", reddishpurple = "#CC79A7"
)
```

```python
# Python
CUD_COLORS = {
    "black": "#000000", "orange": "#E69F00", "skyblue": "#56B4E9",
    "bluishgreen": "#009E73", "yellow": "#F0E442", "blue": "#0072B2",
    "vermilion": "#D55E00", "reddishpurple": "#CC79A7"
}
```

**R Structure:**

```
R/
├── init.sh                 # Entry point
├── config/
│   └── parameters.json     # All config
├── data/
│   └── *.json              # Clean data
├── src/
│   ├── 01-load-data.R      # <100 LOC
│   ├── 02-clean-data.R
│   ├── 03-analysis.R
│   └── 04-visualize.R
└── output/
    └── figures/
```

**Python Structure:**

```
python/
├── init.sh                 # Entry point
├── config/
│   └── parameters.json
├── data/
│   └── *.json
├── src/
│   ├── 01_load_data.py     # <100 LOC
│   ├── 02_clean_data.py
│   ├── 03_analysis.py
│   └── 04_visualize.py
└── output/
    └── figures/
```

**init.sh Template:**

```bash
#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Running analysis pipeline ==="
Rscript src/01-load-data.R
Rscript src/02-clean-data.R
Rscript src/03-analysis.R
Rscript src/04-visualize.R
echo "=== Done. Check output/ ==="
```

**Code Checklist:**

- [ ] All files <100 LOC?
- [ ] Data in JSON format?
- [ ] Config in JSON?
- [ ] init.sh runs all?
- [ ] CUD colors used?
- [ ] Output reproducible?


---


## SLR Workflow (Systematic Literature Review)

**Tool:** `/home/fong/Projects/slr-paper-downloader/slr.sh`

**Sources (ALL 3 required):**

| Source | Strength | Query Style |
|--------|----------|-------------|
| **arxiv** | Preprints, CS/AI | Technical terms |
| **openalex** | Broad academic | Author names, titles |
| **semantic_scholar** | Citations, AI | Concept-based |

**Workflow Pattern:**

```bash
# 1. Multi-angle search (5-7 queries)
slr.sh --query "main topic framework" --sources arxiv,openalex,semantic_scholar
slr.sh --query "alternative term technology" --sources arxiv,openalex,semantic_scholar
slr.sh --query "application domain region" --sources arxiv,openalex,semantic_scholar

# 2. Download PDFs
slr.sh --download --limit 50

# 3. Extract abstracts
slr.sh --abstracts --output SLR/abstracts/
```

**Query Formulation Strategy:**

| Query Type | Example | Purpose |
|------------|---------|---------|
| **Framework** | "TAM technology acceptance model" | Core theory |
| **Technology** | "Google Workspace Education G Suite" | Specific tool |
| **Alternative** | "Moodle LMS teacher satisfaction" | Comparison |
| **Method** | "Bayesian simulation acceptance" | Methodology |
| **Context** | "e-learning Vietnam higher education" | Geographic |
| **Theory** | "UTAUT unified theory technology" | Extension |

**SLR Output Structure:**

```
SLR/
├── pdfs/                    # Downloaded papers
├── abstracts/
│   └── slr-papers-selected.json  # Top 50 with abstracts
└── notes/
    └── synthesis.md         # Manual synthesis
```

**Quality Filters:**

- Year: >= 2019 (5 years)
- Citations: >= 10 (established)
- Source: Peer-reviewed journals preferred
- Language: English primary

**Integration with WP1:**

```
WP1: INVESTIGATE
├── SLR.sh queries (5-7 searches)
├── Download relevant PDFs
├── Extract abstracts to JSON
├── Synthesize to evidence map
└── Map to hypotheses H1, H2, H3
```


---


## Đắp Thịt Workflow (Iterative Content Enrichment)

**Philosophy:** Đại cương → chi tiết. Ít citation → mọi thứ đều có citation. Sai nhiều → sai ít.

**Quy trình 5 bước:**

| Bước | Hành động | Output |
|------|-----------|--------|
| 1 | Đọc TẤT CẢ sections + bib hiện tại | Citation gap map |
| 2 | Xác định gaps: section nào thiếu citation | Gap table |
| 3 | DSS queries: NewRAG + SLR RAG + Abstracts | Evidence collection |
| 4 | Ghi chép kết quả vào `.memory/` | Memory file |
| 5 | Edit sections: thêm citation + bổ sung nội dung | Updated .tex files |

**DSS Query Strategy cho Đắp Thịt:**

```
# 1. NewRAG (DKM books) - general knowledge
queryNewRAG: ["TAM technology acceptance", "LMS education"]

# 2. SLR RAG (project-specific papers) - specific evidence
/home/fong/Projects/mini-rag/LLM-RAG-query/run2.sh "query" SLR/pdfs

# 3. Abstracts cross-check
jq '.[] | select(.title | contains("keyword"))' SLR/abstracts/*.json

# 4. SSoT verification
rg "exact quote" SLR/pdfs-md/
```

**Anti-patterns:**
- ❌ Edit sections TRƯỚC khi query → hallucination risk
- ❌ Query mà không ghi chép → mất evidence
- ❌ Thêm citation không có trong bib → build error
- ❌ Skip cross-check với SSoT → sai thông tin

**Rule:** Query → Ghi chép → Edit → Cross-check → Commit. Không bỏ bước.


---


## Citation Verification (MANDATORY)

**Philosophy:** RAG = hypothesis. SSoT = PDF→MD + Abstracts. APA7 verify = final gate.

**Source Hierarchy (Trust Level):**

| Priority | Source | Trust | Use For |
|----------|--------|-------|---------|
| 1 | PDF→MD files | **SSoT** | Final cross-check. Exact quotes. |
| 2 | `SLR/abstracts/slr-papers-selected.json` | HIGH | Author, year, title verification |
| 3 | RAG query (SLR/pdfs/) | MEDIUM | Discovery. Initial research. |
| 4 | APA7 verify workflow | GATE | Confirm unknown sources |

**Locations:**

```
SLR/
├── pdfs/                    # 37 papers (741 pages)
├── pdfs-md/                 # PDF→MD converted (SSoT)
└── abstracts/
    └── slr-papers-selected.json  # Metadata (title, authors, year, doi)
```

**Citation Workflow (MANDATORY):**

```
1. RAG Query → Get initial info
2. Cross-check với abstracts.json (title, authors, year)
3. Final verify với PDF→MD hoặc rg trong PDF
4. Unknown source? → APA7 verify workflow
5. Confirm → Write citation
```

**PDF→MD Conversion (SSoT):**

```bash
# Convert PDF to searchable MD
pdftotext "file.pdf" "file.md"

# Or extract with structure
pdftk "file.pdf" dump_data | grep -A2 "InfoKey"
```

**Cross-Check Commands:**

```bash
# Search in abstracts
jq '.[] | select(.title | contains("keyword"))' SLR/abstracts/slr-papers-selected.json

# Search in PDF→MD (SSoT)
rg "exact quote" SLR/pdfs-md/

# RAG query (discovery only)
/home/fong/Projects/mini-rag/LLM-RAG-query/run2.sh "query" SLR/pdfs
```

**APA7 Verify Workflow (for UNIDENTIFIED sources):**

Ref: `.fong/instructions/academic/instructions-apa7-citation-verify.json`

```
Input: filename + content (50-200 words) + 3 hypotheses
Tool: Perplexity → Gemini → Copilot (fallback chain)
Output: CONFIRMED / CORRECTED / UNVERIFIED
```

**Citation Rules:**

| Rule | Description |
|------|-------------|
| **Every claim needs citation** | No uncited statements in paper |
| **RAG ≠ truth** | RAG là gợi ý, không phải nguồn cuối |
| **SSoT = PDF→MD** | Chỉ tin PDF gốc hoặc MD converted |
| **Unknown → Verify** | Dùng APA7 verify workflow |
| **Format: APA7** | Author (Year). Title. Publisher. |

**Checklist (KILL ITEMS):**

- [ ] Mọi số liệu có citation?
- [ ] Citation cross-check với abstracts.json?
- [ ] Exact quote verify với PDF→MD?
- [ ] Unknown source → APA7 verified?
- [ ] Format APA7 đúng?


---


## Cross-References

| Context | File |
|---------|------|
| **Manifest** | `.claude/skills/write-paper/manifest.json` |
| **DSS Skill** | `.claude/skills/dss/SKILL.md` |
| **Professor v2** | `.fong/instructions/instructions-do-take-note-stick-the-plan-professor-v2.json` |
| **LaTeX Guide** | `.fong/instructions/LaTeX/` |
| **Color Palette** | `.fong/instructions/LaTeX/04-color-palette.md` |
| **SLR Tool** | `/home/fong/Projects/slr-paper-downloader/slr.sh` |
| **Academic VN** | `.fong/instructions/academic/scientific-plain-vietnamese-checklist.md` |
| **Academic EN** | `.fong/instructions/academic/scientific-plain-english-checklist.md` |
| **APA7 Verify** | `.fong/instructions/academic/instructions-apa7-citation-verify.json` |
| **RAG Instructions** | `.fong/instructions/instructions-fong-RAG.md` |
| **SLR PDFs** | `SLR/pdfs/` (37 papers, 741 pages) |
| **SLR Abstracts** | `SLR/abstracts/slr-papers-selected.json` |


---


## References

[1] Farley, D. (2021). Modern Software Engineering. Addison-Wesley. P91.
[2] Cotton, R. (2017). Efficient R Programming. P84.
[3] Murray, R. (2018). Developing Research Writing.
[4] instructions-do-take-note-stick-the-plan-professor-v2.json
[5] mindset-agile-kaizen-think-big-do-baby-steps.md
