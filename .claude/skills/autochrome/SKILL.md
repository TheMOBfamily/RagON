---
name: autochrome
description: This skill should be used when the user asks to "automate browser", "scrape web", "download from website", "z-lib download", "chrome automation", "web scraping", uses {autochrome}, or needs Chrome DevTools Protocol automation.
version: 1.1.0
user-invocable: true
disable-model-invocation: false
instructions_source: /home/fong/Projects/mini-rag/.fong/instructions/instructions-autochrome.md
lesson_learned: /home/fong/Projects/MCPs/autochrome-mcp/lesson-learned/
---

# AutoChrome - Browser Automation Skill

Chrome automation via MCP với jQuery injection, sessionless architecture.

## CHECKLIST BẮT BUỘC (TRƯỚC-TRONG-SAU)

### TRƯỚC khi dùng AutoChrome

```bash
# 1. Search lesson-learned cho vấn đề tương tự
mcp__smart-search__smart-search pattern="{vấn đề}" path="/home/fong/Projects/MCPs/autochrome-mcp/lesson-learned"

# 2. Check dom-structures nếu có domain đã lưu
ls /home/fong/Projects/MCPs/autochrome-mcp/lesson-learned/dom-structures/

# 3. Read instructions
Read /home/fong/Projects/mini-rag/.fong/instructions/instructions-autochrome.md
```

### TRONG KHI dùng AutoChrome

```
1. Gặp lỗi → Ghi NGAY vào lesson-learned/ (WHEN/THEN/FIX format)
2. DOM mới → extractDOM() → Copy vào dom-structures/{domain}.html
3. Script hay → Lưu vào scripts/{action}.sh
```

### SAU KHI dùng AutoChrome

```bash
# 1. Tạo lesson file nếu có vấn đề mới
Write /home/fong/Projects/MCPs/autochrome-mcp/lesson-learned/{domain}-{issue}.md

# 2. Update README index
Edit /home/fong/Projects/MCPs/autochrome-mcp/lesson-learned/README.md
```

**{memetic} mindset**: Retrieve → Record → Evolve. Missing either = VIOLATION.

---

**CRITICAL - MANDATORY FIRST ACTION**:
```
1. Smart-search lesson-learned TRƯỚC (absolute path - SSoT)
   mcp__smart-search__smart-search pattern="{issue}" path="/home/fong/Projects/MCPs/autochrome-mcp/lesson-learned"

2. READ instructions (relative path - clone-friendly)
   Read .fong/instructions/instructions-autochrome.md
```
Do NOT skip this step.

## Core Concept

AutoChrome = Chrome DevTools Protocol automation.
Sessionless = Không cần tạo session, system tự quản lý.
jQuery = Auto-inject cho mọi script.

## MCP Tools Available

| Tool | Purpose |
|------|---------|
| `mcp__autochrome-mcp__listTabs` | Liệt kê tất cả Chrome tabs |
| `mcp__autochrome-mcp__getCurrentTab` | Lấy tab đang active |
| `mcp__autochrome-mcp__selectTab` | Chuyển sang tab khác |
| `mcp__autochrome-mcp__executeScript` | Chạy JavaScript (jQuery auto-inject) |
| `mcp__autochrome-mcp__extractDOM` | Trích xuất HTML DOM |
| `mcp__autochrome-mcp__extractText` | Trích xuất plain text |
| `mcp__autochrome-mcp__captureScreenshot` | Chụp viewport |
| `mcp__autochrome-mcp__captureFullPageScreenshot` | Chụp full page |
| `mcp__autochrome-mcp__captureRegionScreenshot` | Chụp vùng cụ thể |
| `mcp__autochrome-mcp__typeText` | Gõ text char-by-char (Vietnamese support) |
| `mcp__autochrome-mcp__pasteByWords` | Paste word-by-word |
| `mcp__autochrome-mcp__pressKey` | Nhấn phím đặc biệt + modifiers |

## Workflow Pattern

```
1. listTabs() → Tìm tab cần thao tác
2. selectTab(tabId) → Chuyển sang tab đó
3. extractDOM() → Hiểu cấu trúc trang (LUÔN LÀM TRƯỚC)
4. executeScript() → Thực hiện action với jQuery
5. captureScreenshot() → Verify kết quả
```

## Z-Library Download Workflow

**Pre-requisites:**
- Chrome đang chạy với remote debugging
- Đã đăng nhập Z-Library
- Đã link Telegram

**Steps:**

### Step 1: Navigate to Z-Library
```javascript
mcp__autochrome-mcp__executeScript({
  script: "window.location.href = 'https://z-lib.gd/?ts=0824'"
})
```

### Step 2: Search
```javascript
mcp__autochrome-mcp__executeScript({
  script: "$('#searchFieldx').val('SEARCH_TERM').closest('form').submit()"
})
```

### Step 3: Parse Results
```javascript
mcp__autochrome-mcp__executeScript({
  script: `
    const books = Array.from(document.querySelectorAll('.book-item z-bookcard')).map(el => ({
      title: el.querySelector('[slot="title"]')?.textContent?.trim(),
      author: el.querySelector('[slot="author"]')?.textContent?.trim(),
      href: el.getAttribute('href'),
      filesize: el.getAttribute('filesize'),
      year: el.getAttribute('year')
    }));
    JSON.stringify(books.slice(0, 10), null, 2);
  `
})
```

### Step 4: Download via Telegram (with duplicate check)
```javascript
mcp__autochrome-mcp__executeScript({
  script: `
    (function() {
      const zCover = document.querySelector('z-cover');
      const isDownloaded = zCover?.shadowRoot?.querySelector('.mark.downloaded');
      if (isDownloaded) return JSON.stringify({skip: true, reason: 'Already downloaded'});

      const sendBtn = document.querySelector('.button-send-book');
      if (!sendBtn) return JSON.stringify({error: 'Send button not found'});
      sendBtn.click();

      setTimeout(() => {
        document.querySelector('[data-send_to="telegram"]')?.click();
      }, 1200);

      return JSON.stringify({success: true});
    })()
  `
})
```

## Rate Limits

| Action | Delay |
|--------|-------|
| Between searches | 3 seconds |
| Between downloads | 5 seconds |
| After error | 10 seconds |

## jQuery Patterns (RECOMMENDED)

```javascript
// Get page title
$("title").text()

// Fill form
$("#input").val("value").focus().blur()

// Click button
$("button.submit").click()

// Extract links
$("a").map((i,el) => $(el).attr("href")).get()

// Scroll to element
$("h2").get(0).scrollIntoView({behavior: "smooth"})
```

## Critical Rules

1. **ALWAYS extractDOM() FIRST** - Hiểu trang trước khi action
2. **jQuery auto-inject** - Không cần khai báo `libraries: ["jquery"]`
3. **Rate limiting** - Delay giữa các action để tránh block
4. **Shadow DOM** - Z-Library dùng Shadow DOM cho badges
5. **Sessionless** - Không cần quản lý session

## Error Handling

| Error | Action |
|-------|--------|
| Tab not found | User cần mở trang manually |
| Script fails | captureScreenshot() để debug |
| Rate limited | Tăng delay |
| Login required | Báo user đăng nhập |

## Related Documents

### Internal (Relative - clone-friendly)
- **Instructions**: `.fong/instructions/instructions-autochrome.md`
- **Z-Library Workflow**: `docs/instructions/instructions-zlibrary-autochrome-download/`
- **Examples**: `./examples/`
- **References**: `./references/`

### External (Absolute - SSoT chung)
- **Lesson Learned**: `/home/fong/Projects/MCPs/autochrome-mcp/lesson-learned/`
- **MCP Source**: `/home/fong/Projects/MCPs/autochrome-mcp/`

## AI Workflow

1. **Print Pre-Prompt** → Show skill info
2. **listTabs()** → Tìm tab target
3. **selectTab()** → Chuyển tab nếu cần
4. **extractDOM()** → Hiểu cấu trúc
5. **executeScript()** → Thực hiện action
6. **Verify** → Screenshot hoặc DOM check
