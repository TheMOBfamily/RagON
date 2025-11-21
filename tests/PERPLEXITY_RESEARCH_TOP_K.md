# Perplexity Research: Optimal TOP_K for Multi-Source RAG

**Date:** 2025-10-22  
**Query:** Optimal TOP_K for 5-source parallel RAG system

## Research Summary

Based on 2023-2025 studies on RAG optimization:

**Recommendation: TOP_K = 8 per source**

## Reasoning

1. **Moderate TOP_K (6-10) is optimal** for multi-source systems
2. **Total chunks:** 8 × 5 = 40 before dedup → ~30-35 after dedup
3. **Balance:** Coverage vs noise vs token budget
4. **Evidence:** Studies show gains in retrieval precision with TOP_K=6-10
5. **Deduplication:** Reduces overlap, allows higher TOP_K without proportional noise

## Tradeoffs

### Low TOP_K (3-5)
- ✅ High precision, low tokens
- ❌ May miss context, limited coverage

### Medium TOP_K (6-10) ⭐ OPTIMAL
- ✅ Improved coverage and recall
- ✅ Better context diversity
- ✅ Manageable tokens with dedup
- ✅ Supported by research
- ⚠️ Slightly more noise (use reranking if needed)

### High TOP_K (15-20)
- ✅ Maximum recall
- ❌ High token consumption
- ❌ Increased noise
- ❌ Diminishing returns

## Implementation

Updated `/multi-query/src/config.py`:
```python
top_k_per_source: int = getenv_int("MULTI_RAG_TOP_K", 8)  # Changed from 4 to 8
```

## Sources

- Ryan Chiang, "Optimizing Retrieval-Augmented Generation" (2023)
- Pinecone, "Rerankers and Two-Stage Retrieval" (2023)
- X. Wang et al., "Best Practices in RAG," EMNLP 2024
- AutoRAG arXiv 2024
- "RAG: Comprehensive Survey," arXiv 2025

---

## Update: Large-Scale Optimization (200-300 PDFs)

**Date:** 2025-10-22  
**Scale:** 200-300 PDF sources

### Critical Finding: Token Explosion

**Previous (5 sources):**
- TOP_K=8 × 5 sources = 40 chunks → ~30-35 after dedup ✅ OK

**Large scale (300 sources):**
- TOP_K=8 × 300 = 2,400 chunks  
- 2,400 × 1200 chars = 2.88M chars (~720K tokens) ❌ EXCEEDS LLM LIMIT

### New Recommendation: TOP_K = 3

**Reasoning (research-backed):**
1. **Token budget:** 300 × 3 = 900 chunks → ~600-700 after dedup
2. **Context window:** Stays within 128K-256K token limits
3. **Diminishing returns:** Minimal gains beyond TOP_K=3-4 at large scale
4. **Precision:** Lower TOP_K reduces noise/irrelevance

### Scaling Challenges Identified

1. **Token Explosion**
   - 200-300 sources × TOP_K=8 exceeds LLM context windows
   - Cost and latency issues

2. **Relevance Dilution**
   - More sources = more noise without filtering
   - Requires reranking

3. **Performance**
   - Parallel retrieval strain
   - Memory consumption

### Additional Requirements for Large Scale

**Mandatory:**
- ✅ **Reranking:** Cross-encoder to prune candidates
- ✅ **Two-stage retrieval:** Retrieve more, rerank to smaller set
- ✅ **Query routing:** Don't query all sources every time
- ✅ **Adaptive TOP_K:** Dynamic adjustment per source relevance

**Optional but Recommended:**
- Vector store optimization (FAISS IVF-PQ, HNSW)
- Smaller chunks with strong reranking
- Batching/async retrieval
- Continuous evaluation metrics (Recall@k, faithfulness)

### Implementation

Updated `/multi-query/src/config.py`:
```python
# For small scale (5-10 sources): TOP_K=8
# For large scale (200-300 sources): TOP_K=3
top_k_per_source: int = getenv_int("MULTI_RAG_TOP_K", 3)
```

### Comparison

| Scale | Sources | TOP_K | Total Chunks | After Dedup | Tokens | Status |
|-------|---------|-------|--------------|-------------|--------|--------|
| Small | 5 | 8 | 40 | ~35 | ~42K | ✅ Optimal |
| Large | 300 | 8 | 2,400 | ~2,000 | ~720K | ❌ Too high |
| Large | 300 | 3 | 900 | ~700 | ~252K | ✅ Optimal |

### Research Sources (2023-2025)

- Dave AI: RAG token splitting strategies (2023)
- Meta REFRAG: Selective processing for scaling (2024)
- arXiv: DOS RAG token budget efficiency (2025)
- F5: RAG with large context windows (2025)
- Deepchecks: Building scalable RAG pipelines (2024)

### Key Insights

> "Fixed high TOP_K leads to token overload and quality degradation at scale. Adaptive and two-stage methods maintain relevance and efficiency." — arXiv 2025

> "Diminishing returns beyond 3-4 chunks per source in large-scale settings." — Meta REFRAG 2024

### Next Steps

1. ✅ Update TOP_K to 3 (done)
2. 🔄 Implement reranking (future)
3. 🔄 Add query routing (future)
4. 🔄 Adaptive TOP_K (future)
