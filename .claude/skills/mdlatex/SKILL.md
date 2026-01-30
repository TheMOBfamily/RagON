---
name: mdlatex
description: This skill should be used when the user asks to "create document", "write markdown", "export PDF", "tao tai lieu", "xuat PDF", "add diagram", "Mermaid", "PlantUML", "TikZ", "mdlatex", "textor", uses {mdlatex}, {textor}, or needs markdown-to-PDF conversion with diagrams.
version: 1.0.0
user-invocable: true
disable-model-invocation: false
instructions_source: .fong/instructions/textor-mdlatex/
script_path: /home/fong/Projects/textor-doc-converter/run-807f321188c6.sh
veta_instructions: .fong/instructions/instructions-VETA-Viet-Eng-Term-Analyzer.json
output_language: Vietnamese
---

# MD LaTeX - Markdown Document & PDF Export Skill

Tạo tài liệu Markdown chuẩn với diagram (Mermaid, PlantUML, TikZ) và export PDF qua Textor.


## Output Language: TIẾNG VIỆT CÓ DẤU (MANDATORY)

> **VIỆT HÓA CỰC ĐOAN** - Tất cả output phải bằng tiếng Việt CÓ DẤU đầy đủ.

**Ref:** `.fong/instructions/instructions-VETA-Viet-Eng-Term-Analyzer.json`

**Rules:**

- Output file .md/.pdf = TIẾNG VIỆT CÓ DẤU (không được viết không dấu)
- Thuật ngữ kỹ thuật = Inline format: "Tên Việt (English term)"
- KHÔNG tạo bảng thuật ngữ riêng (render xấu trong PDF)
- Dùng VETA để Việt hóa chính xác
- **CRITICAL:** Viết không dấu = VIOLATION. Phải có đầy đủ dấu tiếng Việt.

**VETA Execution:**

```
# Có file path
.fong/tools/veta-gemini.sh /path/to/file

# Fallback
.fong/tools/veta-copilot.sh /path/to/file

# Không có file path
mcp__dkm-knowledgebase__queryCopilot
```


## Input Types: GENERAL (Mọi loại đều được)

> **KHÔNG FIX CỨNG** - Skill nhận BẤT KỲ loại input nào.

| Input Type | Ví dụ | Output |
|------------|-------|--------|
| **Document** | Tài liệu, báo cáo, hướng dẫn | .md + .pdf |
| **Diagram** | Flowchart, sequence, mindmap | .md với diagram blocks |
| **Template** | Skeleton document | .md từ skeleton |
| **Existing .md** | File cần export | .pdf qua Textor |
| **Mixed** | Text + diagrams + math | .md + .pdf đầy đủ |


**CRITICAL - MANDATORY FIRST ACTIONS (Zero Skip)**:

```
READ .fong/instructions/textor-mdlatex/00-instructions-textor-doc-converter-mermaid-plantuml-mdlatex.md
READ .fong/instructions/textor-mdlatex/01-critical-rules.md
READ .fong/instructions/textor-mdlatex/01b-critical-rules-diagrams.md
READ .fong/instructions/textor-mdlatex/01c-critical-rules-plantuml-quality.md
READ .fong/instructions/textor-mdlatex/12-footnote-citation.md
READ .fong/instructions/textor-mdlatex/99-skeleton-template.md
```

Use Read tool with ABSOLUTE PATH. Do NOT skip ANY step.


## Core Concept

MD LaTeX = Markdown LaTeX. Markdown with diagrams to PDF.
Textor converts Mermaid/PlantUML/TikZ to images, embeds in PDF.
Pandoc alone CANNOT render diagrams. Textor CAN.


---


## Critical Rules (6 Rules - MANDATORY)


### Rule 1: NO EMOJI

XeLaTeX không render emoji. Professional docs không có emoji.
Exception: Chỉ khi user EXPLICITLY yêu cầu.


### Rule 2: Max 3 Heading Levels

- H1 (#): YAML title only - KHÔNG dùng trong content
- H2 (##): Main sections
- H3 (###): Sub-sections
- KHÔNG DÙNG H4 (####) trở xuống
- Thay thế H4: dùng **bold text**


### Rule 3: 2 Newlines Spacing

Header hoặc bold text -> 2 newlines -> Content.
1 newline = SAI. 2 newlines = ĐÚNG.


### Rule 4: YAML Frontmatter (MANDATORY)

```yaml
---
title: "Tiêu đề tài liệu"
subtitle: "Mô tả ngắn"
author: "Fong"
date: "YYYY-MM-DD"
version: "1.0.0"
---
```


### Rule 5: Footnote Citation

```markdown
Trong text: Kết quả nghiên cứu[^1]. Nguồn khác xác nhận[^2].

Cuối file:
[^1]: Author (Year). Title. Publisher, p.XX.
[^2]: Author (Year). Title. arXiv:XXXX.
```

Bắt buộc dấu `^`. `[^1]` KHÔNG phải `[1]`.


### Rule 6: Diagram Quality

- PlantUML: `skinparam dpi 300` BẮT BUỘC
- Bảng màu Blue-Gray CUD (colorblind-friendly)
- Mermaid: 13 loại diagram hỗ trợ
- TikZ: Full LaTeX math, vector output


---


## Diagram Types


### Mermaid (13 Types)

| Type | Syntax | Best For |
|------|--------|----------|
| Flowchart | `graph LR/TD` | Process flows |
| Sequence | `sequenceDiagram` | API interactions |
| Class | `classDiagram` | OOP structure |
| State | `stateDiagram-v2` | State machines |
| ER | `erDiagram` | Database design |
| Gantt | `gantt` | Project timeline |
| Pie | `pie` | Distribution |
| Mindmap | `mindmap` | Brainstorming |
| Timeline | `timeline` | History |
| Git | `gitGraph` | Branch strategy |

**Ref:** `.fong/instructions/textor-mdlatex/03-mermaid-guide.md`


### PlantUML (11 Types)

| Type | Syntax | Best For |
|------|--------|----------|
| Sequence | `@startuml` | Interactions |
| Use Case | `@startuml` | Requirements |
| Class | `@startuml` | Architecture |
| Activity | `@startuml` | Workflows |
| Component | `@startuml` | System design |
| Salt | `@startsalt` | UI mockups |

**Ref:** `.fong/instructions/textor-mdlatex/06-plantuml-guide.md`

**PlantUML Skeleton (Blue-Gray CUD):**

```plantuml
@startuml diagram-name
skinparam dpi 300
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam defaultFontColor #2C3E50
skinparam shadowing false
skinparam component {
  BackgroundColor #E8ECED
  BorderColor #5D6D7E
}
title Tiêu đề Diagram
' [Content here]
@enduml
```


### TikZ (LaTeX Native)

```markdown
```tikz
\draw[->] (0,0) -- (2,0);
\node at (1,0.5) {Hello TikZ};
```
```

**Ref:** `.fong/instructions/textor-mdlatex/13-tikz-guide.md`


### Mermaid vs PlantUML vs TikZ

| Criteria | Mermaid | PlantUML | TikZ |
|----------|---------|----------|------|
| Output | PNG | PNG | Vector |
| Syntax | Simple | Verbose | LaTeX |
| Math | No | No | Full LaTeX |
| Positioning | Auto | Auto | Manual |
| Best for | Quick diagrams | UML, Salt UI | Math, precision |


---


## Textor Export Commands


### Basic Export

```bash
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"/absolute/path/file.md"}'
```


### Page Size and Orientation

```bash
# A4 landscape
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"file.md","page_size":"A4","orientation":"landscape"}'

# A3 portrait
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"file.md","page_size":"A3","orientation":"portrait"}'
```

| Page Size | Orientation | Margins |
|-----------|-------------|---------|
| A4 | portrait | top/bottom 25mm, left 30mm, right 20mm |
| A4 | landscape | top/bottom 20mm, left/right 25mm |
| A3 | portrait | top/bottom 30mm, left 35mm, right 25mm |
| A3 | landscape | top/bottom 25mm, left/right 30mm |


### Brand Logo Watermark (icon param)

| Preset | Alias | Logo | Height |
|--------|-------|------|--------|
| `hub` | `buh` | HUB University | 20mm |
| `deutschfuns` | `de` | DeutschFuns | 25mm |
| `irontan` | - | IronTan | 3.5mm |
| `nexiumlab` | - | NexiumLab | 7.5mm |
| Custom path | - | Any PNG | 10mm (default) |

```bash
# Preset
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"file.md","icon":"hub"}'

# Custom logo (absolute path)
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"file.md","icon":"/path/to/logo.png"}'
```

Logo hiển thị watermark mờ (50% opacity) ở góc trái-trên. Không ảnh hưởng content.


### AI Disclaimer Box (disclaimer param)

Hiển thị hộp khuyến cáo AI ở góc phải-trên, CHỈ trang 1.

| Giá trị | Ngôn ngữ | Nội dung |
|---------|----------|----------|
| `"vi"` | Tiếng Việt | Khuyến cáo: AI có thể sai. Liên hệ tác giả. |
| `"en"` | English | Disclaimer: AI may err. Contact author. |
| null/omit | Không hiện | Không có disclaimer box |

```bash
# Vietnamese disclaimer
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"file.md","disclaimer":"vi"}'

# English disclaimer
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"file.md","disclaimer":"en"}'

# Kết hợp icon + disclaimer
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"file.md","icon":"hub","disclaimer":"vi"}'
```


### Per-Diagram Dimensions (diagrams param)

Kiểm soát kích thước từng diagram riêng lẻ.

```bash
# All auto (recommended)
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"file.md","diagrams":[{"index":1,"width":"auto","height":"auto"}]}'

# Mixed auto and explicit
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"file.md","diagrams":[{"index":1,"width":"auto","height":600},{"index":2,"width":500,"height":"auto"}]}'

# Full control
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"file.md","diagrams":[{"index":1,"width":550,"height":700}]}'
```

| Field | Type | Description |
|-------|------|-------------|
| `index` | int | Thứ tự diagram trong file (1-based) |
| `width` | int/"auto" | Chiều rộng (pixels hoặc auto) |
| `height` | int/"auto" | Chiều cao (pixels hoặc auto) |


### Legacy Engine (legacy param)

```bash
# Default: XeLaTeX (recommended)
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"file.md"}'

# Legacy: WeasyPrint (chỉ dùng khi XeLaTeX fail)
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"export-md-to-pdf","data":"file.md","legacy":true}'
```

| Engine | Flag | Quality | Use When |
|--------|------|---------|----------|
| XeLaTeX | default | High | Mọi trường hợp (recommended) |
| WeasyPrint | `"legacy":true` | Lower | XeLaTeX fail hoặc compatibility |


### Validate Before Export

```bash
# Validate PlantUML
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"validate-plantuml","data":"@startuml\nAlice->Bob\n@enduml"}'

# Validate Mermaid
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"validate-mermaid","data":"graph LR\nA-->B"}'

# Validate MD with PlantUML
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"validate-md-plantuml","data":"file.md"}'

# Validate MD with Mermaid
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh '{"command":"validate-md-mermaid","data":"file.md"}'
```


### Show Full Help

```bash
/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh --help
```


---


## All CLI Params (SSoT from source code)

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `command` | string | - | Command name (REQUIRED) |
| `data` | string | - | File path or inline code (REQUIRED) |
| `page_size` | string | "A4" | "A4" or "A3" |
| `orientation` | string | "portrait" | "portrait" or "landscape" |
| `icon` | string | null | Logo watermark: preset or abs path |
| `disclaimer` | string | null | AI disclaimer box: "vi", "en", or null |
| `diagrams` | array | null | Per-diagram dimensions [{index, width, height}] |
| `legacy` | bool | false | true = WeasyPrint engine (fallback) |


---


## Output Location

**Default:** Same folder as input .md file.

**Output files:**

| File | Purpose |
|------|---------|
| `{filename}.pdf` | PDF output |
| `{filename}_img/` | Diagram images (PNG + SVG) |


---


## Blue-Gray CUD Palette (Quick Reference)

| Hex | Usage |
|-----|-------|
| #2C3E50 | Text, font |
| #34495E | Arrows |
| #5D6D7E | Borders |
| #85929E | Package borders |
| #D5DBDB | Database, notes |
| #E8ECED | Component backgrounds |
| #F4F6F6 | Package backgrounds |
| #FFFFFF | Main background |

**SSoT:** `.fong/instructions/LaTeX/color-CUD-palette.json`


---


## Document Skeleton Template

```markdown
---
title: "Tiêu đề tài liệu"
subtitle: "Mô tả ngắn"
author: "Fong"
date: "YYYY-MM-DD"
version: "1.0.0"
updated: "YYYY-MM-DD"
---


## Tóm tắt


[Giải thích đơn giản 1-2 câu, dùng ví dụ đời thường]


## Tổng quan


[Mô tả chung về nội dung]


## Nội dung chính


### Phần 1


[Nội dung]


### Phần 2


[Nội dung]


## Ghi chú


[Các lưu ý quan trọng]


[^1]: Nguồn tham khảo 1.

[^2]: Nguồn tham khảo 2.
```


---


## Pre-Prompt Template (RCIFENI-O)

Khi user invoke `/mdlatex`, AI PHẢI output response theo format sau:

```
`Think BIG, DO small steps`, `step by step`. Best effort to `get things done`. ULTRATHINK activated.
Skill: /mdlatex | Tool: Textor Doc Converter
{YYYY-MM-DD HH:MM:SS} (+07)

# 1. Role:
Document Creator + Diagram Designer + Textor Expert

# 2. Context:
Topic: {user's topic}
Output: .md file with diagrams -> .pdf via Textor
Diagrams: {Mermaid / PlantUML / TikZ / None}

# 3. Instructions:
1. READ all required textor-mdlatex instruction files
2. Create .md with YAML frontmatter
3. Add diagrams if needed (Mermaid/PlantUML/TikZ)
4. Add footnote citations [^N]
5. Validate diagrams
6. Export .md to .pdf via Textor

# 4. Output Format:
- File: {filename}.md
- YAML frontmatter required
- Max H3, NO emoji, 2 newlines spacing
- Footnote citations [^N]
- Export: {filename}.pdf via Textor

# 5. Cautions:
- anti: Emoji in content (XeLaTeX fail)
- anti: H4+ headings (Textor fail)
- anti: 1 newline spacing (must be 2)
- anti: Endnote [1] (must be footnote [^1])
- anti: Missing YAML frontmatter
- anti: Low DPI diagrams (must be 300)
- anti: Pandoc for files with diagrams (use Textor)
- anti: Forget disclaimer param (ask user if needed)
- anti: Forget icon param (ask user if brand logo needed)
- anti: Forget diagrams param (per-diagram dimensions if complex)

# 6. OKR:
O: Create {topic} document with diagrams and export PDF
KR1: .md file with correct formatting
KR2: Diagrams rendered correctly
KR3: .pdf exported via Textor without errors
```


---


## AI Workflow

**STEP 0 - MANDATORY FIRST (Zero Skip):**

```
Read tool -> textor-mdlatex/00-instructions-textor-doc-converter-mermaid-plantuml-mdlatex.md
Read tool -> textor-mdlatex/01-critical-rules.md
Read tool -> textor-mdlatex/01b-critical-rules-diagrams.md
Read tool -> textor-mdlatex/01c-critical-rules-plantuml-quality.md
Read tool -> textor-mdlatex/12-footnote-citation.md
Read tool -> textor-mdlatex/99-skeleton-template.md
```

1. **Print Pre-Prompt** -> Show RCIFENI-O template above
2. **Nhận yêu cầu** -> Xác định loại document và diagrams cần thiết
3. **Chọn diagram type**: Mermaid (quick) / PlantUML (UML) / TikZ (math) / None
4. **Create .md file** với:
   - YAML frontmatter (title, subtitle, author, date, version)
   - Content theo skeleton template
   - Diagrams (nếu có)
   - Footnote citations
5. **Validate** diagrams trước khi export
6. **Export PDF** via Textor
7. **Verify** PDF output

**Validation workflow:**

```
IF has PlantUML -> validate-plantuml FIRST
IF has Mermaid -> validate-mermaid FIRST
IF has both -> validate-md-plantuml + validate-md-mermaid
THEN -> export-md-to-pdf
```


---


## Checklist (15 items - MANDATORY)

- [ ] Textor instruction files read?
- [ ] YAML frontmatter complete (title, subtitle, author, date, version)?
- [ ] Max H3 heading depth (no H4+)?
- [ ] NO emoji in content?
- [ ] 2 newlines between headers and content?
- [ ] Tiếng Việt có dấu đầy đủ?
- [ ] Diagram DPI = 300 (PlantUML)?
- [ ] Blue-Gray CUD palette used (PlantUML)?
- [ ] Footnote citations correct (`[^N]` not `[N]`)?
- [ ] Diagrams validated before export?
- [ ] `disclaimer` param considered? (vi/en/null)
- [ ] `icon` param considered? (brand logo watermark)
- [ ] `diagrams` param considered? (per-diagram dimensions if needed)
- [ ] PDF exported via Textor?
- [ ] PDF renders correctly (diagrams, footnotes, disclaimer, logo)?


---


## Cross-References

| Context | File |
|---------|------|
| **Main Index** | `.fong/instructions/textor-mdlatex/00-instructions-textor-doc-converter-mermaid-plantuml-mdlatex.md` |
| **Critical Rules 1** | `.fong/instructions/textor-mdlatex/01-critical-rules.md` |
| **Critical Rules 2** | `.fong/instructions/textor-mdlatex/01b-critical-rules-diagrams.md` |
| **Critical Rules 3** | `.fong/instructions/textor-mdlatex/01c-critical-rules-plantuml-quality.md` |
| **VETA Localization** | `.fong/instructions/textor-mdlatex/01d-critical-rules-veta-localization.md` |
| **Command Reference** | `.fong/instructions/textor-mdlatex/02-command-reference.md` |
| **Mermaid Guide** | `.fong/instructions/textor-mdlatex/03-mermaid-guide.md` |
| **Mermaid Examples** | `.fong/instructions/textor-mdlatex/04-mermaid-examples.md` |
| **Mermaid Advanced** | `.fong/instructions/textor-mdlatex/05-mermaid-examples-advanced.md` |
| **PlantUML Guide** | `.fong/instructions/textor-mdlatex/06-plantuml-guide.md` |
| **PlantUML Examples** | `.fong/instructions/textor-mdlatex/07-plantuml-examples.md` |
| **Salt Guide** | `.fong/instructions/textor-mdlatex/08-plantuml-salt-guide.md` |
| **Salt Advanced** | `.fong/instructions/textor-mdlatex/09-plantuml-salt-advanced.md` |
| **XeLaTeX Alternative** | `.fong/instructions/textor-mdlatex/11-xelatex-alternative.md` |
| **Footnote Citation** | `.fong/instructions/textor-mdlatex/12-footnote-citation.md` |
| **TikZ Guide** | `.fong/instructions/textor-mdlatex/13-tikz-guide.md` |
| **Quick Reference** | `.fong/instructions/textor-mdlatex/99-quick-reference.md` |
| **Skeleton Template** | `.fong/instructions/textor-mdlatex/99-skeleton-template.md` |
| **CUD Palette** | `.fong/instructions/LaTeX/color-CUD-palette.json` |
| **VETA Analyzer** | `.fong/instructions/instructions-VETA-Viet-Eng-Term-Analyzer.json` |


---


## Additional Resources


### Reference Files

- **`references/diagram-types.md`** - Mermaid vs PlantUML vs TikZ comparison


### Example Files

- **`examples/basic-document.md`** - Basic document with skeleton template


### Scripts

- **`scripts/export-pdf.sh`** - Quick export helper script
