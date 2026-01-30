# DOCX Editing Patterns

Common patterns for editing DOCX with Python/lxml.

## Setup

```python
from lxml import etree
import zipfile

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
```

## Pattern 1: Find Paragraph by Text

```python
tree = etree.parse('work_dir/word/document.xml')
paras = tree.findall('.//w:p', NS)

for p in paras:
    text = ''.join(t.text or '' for t in p.findall('.//w:t', NS))
    if 'KEYWORD' in text:
        target_p = p
        break
```

## Pattern 2: Replace Text with Formatting

```python
# Clear existing runs
for child in list(target_p):
    if child.tag == f'{W}r':
        target_p.remove(child)

# Create new run with bold + font size
new_run = etree.SubElement(target_p, f'{W}r')
rPr = etree.SubElement(new_run, f'{W}rPr')
etree.SubElement(rPr, f'{W}b')  # Bold
sz = etree.SubElement(rPr, f'{W}sz')
sz.set(f'{W}val', '24')  # 12pt (half-points)
new_text = etree.SubElement(new_run, f'{W}t')
new_text.text = 'New content here'
```

## Pattern 3: Change Style

```python
# Find pPr (paragraph properties)
pPr = target_p.find('w:pPr', NS)
if pPr is None:
    pPr = etree.SubElement(target_p, f'{W}pPr')
    target_p.insert(0, pPr)

# Set style
pStyle = pPr.find('w:pStyle', NS)
if pStyle is None:
    pStyle = etree.SubElement(pPr, f'{W}pStyle')
pStyle.set(f'{W}val', 'Heading1')
```

## Pattern 4: Save XML

```python
tree.write(
    'work_dir/word/document.xml',
    xml_declaration=True,
    encoding='UTF-8',
    standalone=True
)
```

## Pattern 5: XMLStarlet Quick Replace

```bash
# Simple text replacement
xmlstarlet ed -u "//w:t[text()='OLD']" -v "NEW" document.xml > document.xml.new
mv document.xml.new document.xml
```

## OOXML Elements Reference

| Element | Description |
|---------|-------------|
| `w:p` | Paragraph |
| `w:r` | Run (text with same formatting) |
| `w:t` | Text content |
| `w:rPr` | Run properties (formatting) |
| `w:pPr` | Paragraph properties |
| `w:b` | Bold |
| `w:i` | Italic |
| `w:sz` | Font size (half-points) |
| `w:pStyle` | Paragraph style reference |
