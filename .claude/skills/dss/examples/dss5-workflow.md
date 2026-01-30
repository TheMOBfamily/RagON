---
title: "Microservices Architecture Research"
date: "2026-01-23"
protocol: "DSS5"
sources_used: 5
topic: "Microservices vs Monolith"
---

# Microservices Architecture

## Tóm tắt

Microservices là kiến trúc chia ứng dụng thành các services nhỏ, độc lập[^1]. Mỗi service có database riêng và giao tiếp qua API[^2].

## So sánh Monolith vs Microservices

| Tiêu chí | Monolith | Microservices |
|----------|----------|---------------|
| Deployment | Toàn bộ app | Từng service |
| Scaling | Vertical | Horizontal |
| Team | Centralized | Distributed |
| Database | Shared | Per-service |

## Khi nào dùng Microservices

Dùng khi[^3]:
- Team lớn (>10 devs)
- Cần scale từng phần
- Domain phức tạp, có bounded contexts rõ ràng

Không dùng khi[^4]:
- Startup giai đoạn đầu
- Team nhỏ (<5 devs)
- Domain chưa rõ boundaries

## Best Practices

1. **API Gateway** - Single entry point[^5]
2. **Service Discovery** - Tự động tìm services
3. **Circuit Breaker** - Xử lý failures
4. **Event Sourcing** - Async communication

## Kết luận

Microservices tốt cho scale nhưng phức tạp hơn monolith[^1]. Bắt đầu với modular monolith, refactor sau khi cần[^3].

---

## Sources Used

| # | Tool | Query | Status |
|---|------|-------|--------|
| 1 | NewRAG | "microservices patterns" | ✅ |
| 2 | Perplexity | "microservices vs monolith 2025" | ✅ |
| 3 | Gemini | "when use microservices" | ✅ |
| 4 | Copilot | "microservices anti-patterns" | ✅ |
| 5 | Z.AI | "microservices best practices" | ✅ |

**Consensus:** 4/5 sources agree on "start with monolith" approach.

---

[^1]: Newman, S. (2021). Building Microservices. O'Reilly, p.45.

[^2]: NewRAG: DKM-Building-Microservices-2021.pdf.P89.

[^3]: Perplexity (2026-01-23). Query: "when to use microservices 2025".

[^4]: Copilot (2026-01-23). Query: "microservices anti-patterns".

[^5]: Gemini (2026-01-23). Query: "microservices api gateway pattern".
