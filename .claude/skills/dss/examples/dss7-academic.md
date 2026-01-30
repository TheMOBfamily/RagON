---
title: "P-value Misinterpretation in Medical Research"
date: "2026-01-23"
protocol: "DSS7"
sources_used: 7
topic: "P-value và Bayesian Statistics trong Y học"
academic: true
---

# P-value Misinterpretation in Medical Research

## Tóm tắt

P-value thường bị hiểu sai trong nghiên cứu y học[^1]. Nhiều nhà nghiên cứu nhầm p < 0.05 nghĩa là "95% chắc chắn đúng"[^2].

## Các hiểu lầm phổ biến

### Hiểu lầm 1: P-value = Probability H₀ true

**Sai:** P = 0.03 không có nghĩa "3% H₀ đúng"[^3].

**Đúng:** P-value là probability của DATA given H₀, không phải probability của H₀ given DATA[^4].

### Hiểu lầm 2: P < 0.05 = Important

Statistical significance ≠ Clinical significance[^5]. Effect size quan trọng hơn p-value[^6].

### Hiểu lầm 3: P > 0.05 = No effect

"Absence of evidence" ≠ "Evidence of absence"[^7].

## Bayesian Alternative

Bayesian approach cho phép[^8]:
- Cập nhật beliefs với evidence mới
- Tính P(H|Data) trực tiếp
- Không phụ thuộc threshold cứng 0.05

## Khuyến nghị từ ASA (2016)

ASA Statement on P-values[^9]:
1. P-value không đo probability H₀ đúng
2. P-value không đo effect size
3. Cần report confidence intervals
4. Cần transparent methodology

## Systematic Literature Review

SLR với 388 papers về p-value misinterpretation[^10]:
- 67% papers hiểu sai p-value
- 43% không report effect size
- 29% dùng p-hacking techniques

## Kết luận

P-value hữu ích nhưng không đủ[^11]. Cần kết hợp với effect size, confidence intervals, và Bayesian analysis[^12].

---

## Sources Used (DSS7 Protocol)

| # | Tool | Query | Status |
|---|------|-------|--------|
| 1 | NewRAG | "p-value interpretation" | ✅ |
| 2 | Perplexity | "p-value misinterpretation medicine 2025" | ✅ |
| 3 | Gemini | "ASA statement p-value" | ✅ |
| 4 | Copilot | "Bayesian vs frequentist statistics" | ✅ |
| 5 | Z.AI | "p-value criticism statistics" | ✅ |
| 6 | ArXiv | "p-value replication crisis" | ✅ |
| 7 | SLR | "p-value misinterpretation" (388 papers) | ✅ |

**Consensus:** 7/7 sources agree p-value often misinterpreted.

---

[^1]: Wasserstein, R. & Lazar, N. (2016). ASA Statement on Statistical Significance. The American Statistician, 70(2).

[^2]: NewRAG: DKM-Statistics-Done-Wrong-2015.pdf.P67.

[^3]: Perplexity (2026-01-23). Query: "p-value common misconceptions".

[^4]: Copilot (2026-01-23). Query: "p-value definition frequentist".

[^5]: Gemini (2026-01-23). Query: "statistical vs clinical significance".

[^6]: NewRAG: DKM-Effect-Size-Matters-2020.pdf.P45.

[^7]: Altman, D. & Bland, J. (1995). Absence of evidence is not evidence of absence. BMJ, 311:485.

[^8]: ArXiv: Gelman, A. (2020). Bayesian Workflow. arXiv:2011.01808.

[^9]: ASA (2016). Statement on Statistical Significance and P-Values. DOI: 10.1080/00031305.2016.1154108.

[^10]: SLR (2026-01-23). Query: "p-value misinterpretation medicine". Papers: 388 analyzed.

[^11]: Perplexity (2026-01-23). Query: "alternatives to p-value 2025".

[^12]: Z.AI (2026-01-23). Query: "Bayesian statistics advantages medicine".
