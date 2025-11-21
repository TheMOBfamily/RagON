# MCP queryRAG TOP_K Manual Test Guide

**Date**: 2025-10-26
**Purpose**: Manual testing guide for `mcp__dkm-knowledgebase__queryRAG` tool with various TOP_K values

---

## 📋 Prerequisites

1. Ensure MCP server `dkm-knowledgebase` is running
2. Have access to Claude Code interface
3. Available RAG collections (see `/mcp` command for list)

---

## 🧪 Test Cases

### **TC-01: TOP_K=3 (Specific Factual Question)**

**Objective**: Validate high precision with minimal chunks

**MCP Tool Call**:
```
Use mcp__dkm-knowledgebase__queryRAG with:
- question: "SOLID single responsibility"
- pdf_directory: "/home/fong/Projects/hub-thay-vinh-python-nang-cao-2025-09-29/python-cleancode-books"
- top_k: 3
```

**Expected Results**:
- ✅ 3 chunks retrieved
- ✅ High relevance (90%+)
- ✅ Minimal noise
- ✅ Fast retrieval (<0.1s)

**Quality Check**:
- [ ] Answer mentions "Single Responsibility Principle"
- [ ] Chunks are from Clean Code books
- [ ] No irrelevant information

---

### **TC-02: TOP_K=5 (Default - General QA)**

**Objective**: Validate default behavior

**MCP Tool Call**:
```
Use mcp__dkm-knowledgebase__queryRAG with:
- question: "SOLID principles Python examples"
- pdf_directory: "/home/fong/Projects/hub-thay-vinh-python-nang-cao-2025-09-29/python-cleancode-books"
- top_k: 5
```

**Expected Results**:
- ✅ 5 chunks retrieved
- ✅ Comprehensive coverage of all SOLID principles
- ✅ Low noise (~10%)
- ✅ Fast retrieval

**Quality Check**:
- [ ] Covers SRP, OCP, LSP, ISP, DIP
- [ ] Python code examples present
- [ ] Balanced detail vs breadth

---

### **TC-03: TOP_K=8 (Broad Topic)**

**Objective**: Test broader context retrieval

**MCP Tool Call**:
```
Use mcp__dkm-knowledgebase__queryRAG with:
- question: "Clean code principles best practices"
- pdf_directory: "/home/fong/Projects/hub-thay-vinh-python-nang-cao-2025-09-29/python-cleancode-books"
- top_k: 8
```

**Expected Results**:
- ✅ 8 chunks retrieved
- ✅ Moderate-high relevance (70-80%)
- ⚠️ Some redundancy acceptable (~20%)
- ✅ Fast retrieval

**Quality Check**:
- [ ] Multiple principles covered (KISS, DRY, YAGNI, etc.)
- [ ] Some overlapping information
- [ ] Broader context helpful

---

### **TC-04: TOP_K=10 (Research/Analysis)**

**Objective**: Test extensive retrieval for research

**MCP Tool Call**:
```
Use mcp__dkm-knowledgebase__queryRAG with:
- question: "Software architecture patterns comparison"
- pdf_directory: "/home/fong/Projects/hub-thay-vinh-python-nang-cao-2025-09-29/python-cleancode-books"
- top_k: 10
```

**Expected Results**:
- ✅ 10 chunks retrieved
- ⚠️ Moderate relevance (60-70%)
- ⚠️ Noticeable redundancy (~30%)
- ✅ Still fast (<0.2s)

**Quality Check**:
- [ ] Multiple architecture patterns mentioned
- [ ] Comparative information present
- [ ] Some chunks less relevant
- [ ] Useful for comprehensive research

---

### **TC-05: TOP_K=15 (Stress Test - Not Recommended)**

**Objective**: Validate degradation at high TOP_K

**MCP Tool Call**:
```
Use mcp__dkm-knowledgebase__queryRAG with:
- question: "Python coding standards"
- pdf_directory: "/home/fong/Projects/hub-thay-vinh-python-nang-cao-2025-09-29/python-cleancode-books"
- top_k: 15
```

**Expected Results**:
- ✅ 15 chunks retrieved
- ❌ Low relevance (50-60%)
- 🔴 High noise (~50%)
- ⚠️ Diminishing returns evident

**Quality Check**:
- [ ] Significant redundancy
- [ ] Many chunks marginally relevant
- [ ] Answer quality NOT improved vs TOP_K=8
- [ ] Confirms "avoid >10" recommendation

---

### **TC-06: TOP_K=5 (Multi-Concept - Different Collection)**

**Objective**: Test with different RAG collection

**MCP Tool Call**:
```
Use mcp__dkm-knowledgebase__queryRAG with:
- question: "code review best practices Google"
- pdf_directory: "/home/fong/Projects/RAGs/nasa-google-cleancode"
- top_k: 5
```

**Expected Results**:
- ✅ 5 chunks from Google style guide
- ✅ High relevance (85%+)
- ✅ Specific to Google practices
- ✅ Fast retrieval

**Quality Check**:
- [ ] Google-specific guidelines
- [ ] Code review process mentioned
- [ ] CL (Changelist) best practices

---

### **TC-07: TOP_K=8 (Comparative Query - Laravel)**

**Objective**: Test comparative query with moderate TOP_K

**MCP Tool Call**:
```
Use mcp__dkm-knowledgebase__queryRAG with:
- question: "Laravel routing vs Eloquent ORM"
- pdf_directory: "/home/fong/Projects/RAGs/laravel-books"
- top_k: 8
```

**Expected Results**:
- ✅ 8 chunks covering both concepts
- ✅ Moderate-high relevance (70-80%)
- ✅ Balanced coverage of routing + ORM
- ⚠️ Some redundancy acceptable

**Quality Check**:
- [ ] Both routing and Eloquent covered
- [ ] Comparative information present
- [ ] Code examples from Laravel docs

---

## 📊 Results Recording Template

After each test, record:

| TC ID | TOP_K | Load Time | Retrieval Time | Chunks | Relevance | Noise | Notes |
|-------|-------|-----------|----------------|--------|-----------|-------|-------|
| TC-01 | 3 | | | | | | |
| TC-02 | 5 | | | | | | |
| TC-03 | 8 | | | | | | |
| TC-04 | 10 | | | | | | |
| TC-05 | 15 | | | | | | |
| TC-06 | 5 | | | | | | |
| TC-07 | 8 | | | | | | |

**Relevance Rating**: 1-5 stars (5 = perfect, 1 = poor)
**Noise Level**: % of irrelevant chunks (subjective estimate)

---

## 🎯 Success Criteria

### **Pass Criteria**:
- ✅ All test cases retrieve correct number of chunks (= TOP_K)
- ✅ TC-01, TC-02: Relevance ≥ 4/5 stars
- ✅ TC-03: Relevance ≥ 3.5/5 stars
- ✅ TC-04: Relevance ≥ 3/5 stars
- ✅ TC-05: Demonstrates clear degradation vs TC-04
- ✅ Retrieval time < 0.5s for all cases

### **Validation Against Academic Research**:
- [ ] TOP_K=3-5 shows highest quality (confirms research)
- [ ] TOP_K=5-8 provides balanced coverage (confirms research)
- [ ] TOP_K=10 shows moderate quality (confirms research)
- [ ] TOP_K>10 shows diminishing returns (confirms research)

---

## 📝 Additional Tests (Optional)

### **Edge Cases**:

1. **TOP_K=1 (Minimum)**:
   ```
   question: "What is DRY principle?"
   top_k: 1
   ```
   Expected: Single most relevant chunk, very focused

2. **TOP_K=20 (Extreme)**:
   ```
   question: "Python best practices"
   top_k: 20
   ```
   Expected: Severe noise, NOT recommended

3. **Omit top_k (Default Behavior)**:
   ```
   question: "SOLID principles"
   (no top_k parameter)
   ```
   Expected: Default to 5 chunks

---

## 🔧 Troubleshooting

### **Issue**: "Collection not found"
- **Fix**: Verify pdf_directory path with `ls -la <path>`

### **Issue**: "Fewer chunks than TOP_K"
- **Cause**: Not enough documents in collection
- **Expected**: If collection has only 7 chunks total, TOP_K=10 returns 7

### **Issue**: "MCP tool not available"
- **Fix**: Run `/mcp` to check server status
- **Fallback**: Use local `./run.sh` with `--top-k` parameter

---

## 📚 References

- [Academic Research](https://perplexity.ai) - TOP_K=5 optimal (2020-2025)
- [Memory File](.fong/.memory/2025-10-26-top-k-parameter-implementation.md)
- [Documentation](.fong/instructions/instructions-fong-RAG.md)

---

## ✅ Post-Test Actions

After completing all tests:

1. [ ] Document results in `.fong/.memory/2025-10-26-topk-test-results.md`
2. [ ] Update mem0 with findings
3. [ ] Compare with academic research predictions
4. [ ] Update documentation if patterns differ from expectations
5. [ ] Git commit test results

---

**Last Updated**: 2025-10-26
**Test Plan Version**: 1.0.0
