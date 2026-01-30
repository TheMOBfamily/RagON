# DSS Query Patterns

## Query Style

**Rule:** SHORT (2-4 words). SPECIFIC. MULTIPLE.

## Good Patterns

```python
# Single topic, multiple angles
queryNewRAG(["SOLID principles", "clean architecture", "dependency injection"])

# What + Why + How
queryNewRAG(["define microservices", "why microservices", "microservices patterns"])

# Comparison
queryNewRAG(["monolith vs microservices", "when use microservices"])
```

## Bad Patterns

```python
# Too long
queryNewRAG(["what are the SOLID principles in software engineering and how do they apply"])

# Too vague
queryNewRAG(["best practices"])

# Single query only
queryNewRAG(["microservices"])  # Need 2-3 queries minimum
```

## Multiquery Strategy (3-5 queries)

| # | Type | Template |
|---|------|----------|
| 1 | WHAT | "Define [Concept]" |
| 2 | WHY | "Why [Concept] matters" |
| 3 | HOW | "Step-by-step [Concept]" |
| 4 | WHO | "Expert opinion [Concept]" |
| 5 | PITFALLS | "Common mistakes [Concept]" |

## Perplexity Query Format

```python
queryPerplexity({
    "role": "Expert researcher",
    "context": "Researching [topic] for [purpose]",
    "instructions": ["List key concepts", "Compare approaches", "Identify best practices"],
    "output_format": "Aphoristic. 1 line = 1 idea. Minimal words.",
    "question": "[Specific question]",
    "okr_krs": "Objective: [Goal]. KR: [Measurable result]"
})
```

## ArXiv Query Format

```python
queryArXiv({
    "query": "machine learning security",
    "max_results": 10,
    "sort_by": "Relevance"
})
```

## Timing Pattern

| Phase | NewRAG | Perplexity | Others |
|-------|--------|------------|--------|
| BEFORE | 3 | 1 | 1 each |
| DURING | 4-20 | 1-2 | As needed |
| AFTER | 2-7 | 1-2 | Verify |

**Anti-pattern:** Query 9x → then work.
**Best practice:** Query → Reason → Do → Query → Reason → Do.
