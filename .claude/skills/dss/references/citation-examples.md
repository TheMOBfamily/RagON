# Citation Examples (Footnote Format)

## In-text Citation

```markdown
Nghiên cứu cho thấy kết quả quan trọng[^1]. Nguồn khác xác nhận[^2].
Clean Architecture giúp tách biệt concerns[^3].
```

## Footnote Definitions (End of File)

### Book/PDF từ RAG

```markdown
[^1]: Martin, R. (2008). Clean Code. Prentice Hall, p.145.

[^2]: Martin, R. (2017). Clean Architecture. Prentice Hall, p.89.

[^3]: NewRAG: DKM-Clean-Architecture-2017.pdf.P89.
```

### Academic Paper (ArXiv)

```markdown
[^4]: Liu et al. (2023). Lost in the Middle. arXiv:2307.03172.

[^5]: Vaswani et al. (2017). Attention Is All You Need. arXiv:1706.03762.
```

### Web Source (Perplexity)

```markdown
[^6]: Perplexity (2026-01-23). Query: "clean architecture patterns 2025".

[^7]: Perplexity (2026-01-23). Query: "microservices best practices".
```

### Copilot/Gemini/Z.AI

```markdown
[^8]: Copilot (2026-01-23). Query: "dependency injection patterns".

[^9]: Gemini (2026-01-23). Query: "SOLID principles explanation".

[^10]: Z.AI (2026-01-23). Query: "clean code principles".
```

### SLR (Systematic Literature Review)

```markdown
[^11]: SLR (2026-01-23). Query: "machine learning security". Papers: 15 analyzed.
```

## Full Example Output

```markdown
---
title: "Clean Architecture Research"
date: "2026-01-23"
protocol: "DSS5"
sources_used: 5
---

# Clean Architecture

## Tóm tắt

Clean Architecture là kiến trúc phần mềm tập trung vào separation of concerns[^1].

## Nguyên tắc cốt lõi

### Dependency Rule

Dependencies phải hướng vào trong (inward)[^2]. Outer layers có thể phụ thuộc inner layers, không ngược lại[^3].

### Entities

Business rules thuần túy, không phụ thuộc framework[^4].

## Kết luận

Clean Architecture giúp code testable và maintainable[^5].

---

[^1]: Martin, R. (2017). Clean Architecture. Prentice Hall, p.89.

[^2]: NewRAG: DKM-Clean-Architecture-2017.pdf.P145.

[^3]: Perplexity (2026-01-23). Query: "clean architecture dependency rule".

[^4]: Copilot (2026-01-23). Query: "clean architecture entities layer".

[^5]: Gemini (2026-01-23). Query: "benefits clean architecture".
```

## Rules

1. **Bắt buộc `[^N]`** - Dấu `^` là bắt buộc
2. **Unique keys** - Mỗi `[^N]` phải unique
3. **Định nghĩa cuối file** - Sau nội dung chính
4. **Format ngắn gọn** - Author (Year). Title, p.XX.
5. **Include query** - Ghi rõ query đã dùng cho AI sources
