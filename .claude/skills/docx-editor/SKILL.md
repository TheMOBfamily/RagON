---
name: docx-editor
description: This skill should be used when the user asks to "edit a DOCX file", "modify Word document", "replace text in DOCX", "change DOCX formatting", "fix DOCX styles", "extract text from DOCX", or mentions XMLStarlet, docxBox, python-docx, lxml for Word editing.
version: 1.0.0
user-invocable: true
disable-model-invocation: false
instructions_source: /home/fong/Projects/docx-cli-tools/instructions-xmlstarlet-docxbox-python.json
---

# DOCX Editor Skill

Edit Microsoft Word (.docx) files using CLI tools on Linux.

**CRITICAL - MANDATORY FIRST ACTION**:
```
READ /home/fong/Projects/docx-cli-tools/instructions-xmlstarlet-docxbox-python.json
```
Use Read tool with ABSOLUTE PATH. Do NOT use relative path. Do NOT skip this step.

## Core Concept

DOCX = ZIP archive containing XML files. Workflow: Unzip → Edit XML → Zip back.

## Tools Priority

| Tool | Use Case |
|------|----------|
| Python/lxml | Complex edits (formatting, structure) - RECOMMENDED |
| XMLStarlet | Simple text replacement, quick queries |
| docxBox | Template filling, batch operations |

## Critical Rules

1. **NEVER edit original file** - Always create timestamped output
2. **NEVER mental math** - Use math tools for width/margin calculations
3. **Dual-source verification** - Search local docs AND query Perplexity

## File Workflow (IMMUTABLE)

```bash
# 1. Backup
cp input.docx "input.$(date +%Y%m%d_%H%M%S).b.docx"

# 2. Extract
unzip input.docx -d _work_$(date +%Y%m%d_%H%M%S)

# 3. Edit XML in work folder
# ... edit word/document.xml ...

# 4. Repack to NEW file
cd _work_* && zip -r ../output.$(date +%Y%m%d_%H%M%S).docx .

# 5. Verify
unzip -l output.*.docx
```

## Namespace (Required)

```python
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
```

## Common XPath

| Element | XPath |
|---------|-------|
| All text | `//w:t` |
| Paragraphs | `//w:p` |
| Tables | `//w:tbl` |
| Bold | `//w:b` |
| Font size | `//w:sz` |

## Math Calculations

Content width = page_width - left_margin - right_margin

```bash
# Use math tool, NOT mental math
python3 -c 'print(12240 - 940 - 560)'  # → 10740 twips
```

Unit conversions:
- 1 inch = 1440 twips
- 1 cm = 567 twips
- Font size: pt × 2 = half-points (12pt = 24)

## Additional Resources

### Reference Files
- **`references/patterns.md`** - Common editing patterns with Python/lxml

### Example Files
- **`examples/basic-edit.sh`** - Basic text replacement workflow

### Scripts
- **`scripts/validate-docx.sh`** - Validate DOCX structure

## Local Documentation (ABSOLUTE PATHS - USE READ TOOL)

**Master Instructions (MUST READ FIRST with Read tool):**
```
Read tool → file_path: /home/fong/Projects/docx-cli-tools/instructions-xmlstarlet-docxbox-python.json
```
⚠️ ABSOLUTE PATH only. NEVER use relative path like `./instructions-*.json`

Search before editing:
```bash
smart-search 'keyword' /home/fong/Projects/docx-cli-tools/docs/ --show-content
```

Key docs:
- `/home/fong/Projects/docx-cli-tools/docs/ecma-376-extracted/` - ECMA-376 specification
- `/home/fong/Projects/docx-cli-tools/docs/ecma-376-extracted/00-wordprocessingml-quick-reference.md` - Quick reference
- `/home/fong/Projects/docx-cli-tools/docs/ooxml-wordprocessingml-structure.md` - OOXML structure
- `/home/fong/Projects/docx-cli-tools/docs/xmlstarlet-manual.md` - XMLStarlet manual
- `/home/fong/Projects/docx-cli-tools/docs/docxbox-manual.md` - docxBox manual
- `/home/fong/Projects/docx-cli-tools/docs/lesson-learned/` - Lesson learned từ các task trước

## AI Workflow (từ instructions JSON)

**⚠️ STEP 0 - MANDATORY FIRST (Zero Skip):**
```
Read tool → /home/fong/Projects/docx-cli-tools/instructions-xmlstarlet-docxbox-python.json
```

1. **Nhận prompt** → Parse yêu cầu
2. **Search local docs** (BẮT BUỘC): `smart-search 'keyword' /home/fong/Projects/docx-cli-tools/docs/`
3. **Query Perplexity** (BẮT BUỘC): OOXML/WordprocessingML context
4. **Cross-verify** 2 nguồn → Tìm consensus
5. **Execute** với evidence từ CẢ 2 nguồn
6. **Record** lesson learned nếu thành công
