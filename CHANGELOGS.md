# CHANGELOGS - Mini-RAG

**Phiên bản**: 0.3
**Tác giả**: Lâm Thanh Phong - Trường Đại Học Ngân Hàng Tp. Hồ Chí Minh
**Ngày cập nhật**: 20/11/2025

## Phiên bản 0.3 (20/11/2025)

### 🚀 Performance Optimization - Shared Memory Cache

#### /dev/shm/ Cache Implementation
- **Apply to multi-query system**: Tích hợp SharedMemoryCache vào `standalone_loader.py`
- **Reuse existing modules**: DRY principle - dùng `shm_cache.py` từ minirag package
- **Smart invalidation**: Manifest hash tracking để auto-invalidate khi PDFs thay đổi
- **Zero architecture change**: Transparent caching, không cần sửa `run-multiquery.sh`

#### Performance Gains
- **Cold start**: 7.29s (load from disk + cache to /dev/shm/)
- **Warm hit**: 2.88s (load from /dev/shm/) → **2.5x faster**
- **Cache size**: ~90MB per source, persistent across process restarts
- **Memory footprint**: Fixed cache trong RAM, không tăng theo số queries

#### Code Quality
- **Clean Code maintained**: 149 LOC < 150 LOC limit (CLAUDE.md standard)
- **SSOT principle**: Config managed centrally trong `config.py`
- **SRP compliance**: Cache separated into 3 modules (cache, validator, cleanup)
- **Backward compatible**: Existing code works unchanged

#### Technical Details
- **Cache location**: `/dev/shm/minirag_faiss_<hash>.pkl`
- **Cache key**: MD5(path + manifest_hash)[:16]
- **Metadata tracking**: `.meta` file với manifest_hash, save_time, pdf_dir
- **Error handling**: Graceful fallback khi cache corrupted hoặc /dev/shm/ full

---

## Phiên bản 0.2 (23/10/2025)

### 🔄 Refactoring (23/10/2025 - Update)

#### API Simplification - Remove max_sources
- **Removed unused parameter**: `max_sources` không được sử dụng trong implementation
- **Filtering via source_hashes**: User đã tự control số lượng qua hash selection
- **Cleaner API**: Simplified NewRAGQuerySchema (2 params instead of 3)
- **Code cleanup**: Removed dead code từ types.ts, handler, tool definition

#### New Tool: listNewRAGSources
- **MCP discovery tool**: List all hundreds of books với filename + hash qua MCP
- **Replace Bash workflow**: Không cần run bash script trực tiếp
- **Consistent UX**: Follow pattern của listRAGCollections
- **30s timeout**: Fast listing với error handling

#### Workflow Enhancement
- **MANDATORY step**: Call listNewRAGSources() FIRST before queryNewRAG
- **Updated documentation**: Clear 3-step workflow trong tool description
- **Better discoverability**: User discover PDFs qua MCP tool, không qua docs
- **Example-driven**: Workflow example ngay trong tool description

### 🚀 Tính năng mới

#### NewRAG MCP Tool - Cross-Project Knowledge Search
- **MCP server integration**: Thêm `queryNewRAG` tool vào DKM Knowledge Base MCP
- **Multi-query support**: 1-3 parallel queries với source filtering
- **Hash-based filtering**: Select specific books qua 32-char MD5 hash
- **Cross-project service**: Gọi từ BẤT KỲ project nào không cần CD
- **Discovery commands**: `--list-pdfs`, `--list-sources`, `--help` với absolute paths

#### Workflow UX Improvement
- **Absolute path workflow**: Không cần CD sang mini-rag directory
- **From ANY project**: `~/Projects/mini-rag/multi-query/run-multiquery.sh --list-pdfs`
- **Simplified steps**: Từ 5 steps → 4 steps (remove CD requirement)
- **Cross-project compatibility**: Perfect cho AI searching từ project khác

### 🔧 Cải thiện kỹ thuật

#### MCP Server Architecture
- **TypeScript handler**: `newrag-handler.ts` với execa subprocess
- **Config centralization**: `NEWRAG_CONFIG` trong `config.ts`
- **Auto working directory**: `cwd` tự động set trong execa call
- **Timeout management**: 300s timeout cho large queries
- **Error handling**: Graceful timeout và exit code handling

#### Code Quality
- **Tool definition refactor**: Documentation phản ánh đúng cross-project usage
- **Consistent with implementation**: Workflow match với actual code behavior
- **User-centric design**: Không assume user đang ở project nào

### 📚 Documentation

#### MCP Tool Description
- **Discovery commands**: Clear instructions với absolute paths
- **Workflow guide**: Step-by-step từ listing PDFs đến query
- **Critical rules**: Max sources, hash format, performance warnings
- **Examples**: Practical query patterns với source filtering

#### Memory Records
- **Implementation record**: `2025-10-23-newrag-mcp-implementation.md`
- **WBS plan**: `2025-10-23-newrag-mcp-wbs-plan.md`
- **Workflow refactor**: `2025-10-23-queryNewRAG-workflow-refactor.md`

### 🏗️ Files Added/Modified

```
ts-mcp/
├── src/
│   ├── newrag-handler.ts      # NEW: NewRAG MCP handler
│   ├── config.ts              # MODIFIED: Add NEWRAG_CONFIG
│   ├── index.ts               # MODIFIED: Add queryNewRAG route
│   ├── tool-definitions.ts    # MODIFIED: Add queryNewRAG tool
│   └── types.ts               # MODIFIED: Add NewRAGQueryParams

.fong/.memory/short-term/
├── 2025-10-23-newrag-mcp-implementation.md
├── 2025-10-23-newrag-mcp-wbs-plan.md
└── 2025-10-23-queryNewRAG-workflow-refactor.md
```

### 🎯 Use Cases

#### AI Knowledge Search from Any Project
```bash
# Đang ở /home/fong/Projects/laravel-app
# Search knowledge qua NewRAG MCP
/home/fong/Projects/mini-rag/multi-query/run-multiquery.sh --list-pdfs | jq ...
```

#### MCP Tool Integration
```typescript
// From ANY Claude Code session
mcp__dkm-knowledgebase__queryNewRAG({
  queries: ["SOLID principles", "clean code"],
  source_hashes: "838cc6ac8cb0d8ddb98fdb1ae0c8a443,41d80961ba66da6a1294aa9624cea15d",
  max_sources: 9
})
```

### 🔬 Technical Specifications

#### MCP Handler Details
```typescript
// Auto working directory setup
await execa(NEWRAG_CONFIG.runnerPath, args, {
  timeout: NEWRAG_CONFIG.timeout,
  cwd: NEWRAG_CONFIG.workDir,  // Auto CD
});
```

#### Performance
- **Timeout**: 300s (5 minutes) cho large queries
- **Max sources**: 9 books (cognitive load limit)
- **Max queries**: 3 parallel queries per request
- **Output**: Structured JSON với results và timing

### 🐛 Bug Fixes

#### Documentation UX Issues
- **Fixed**: Workflow yêu cầu CD sang mini-rag directory
- **Root cause**: Documentation copy từ local development docs
- **Solution**: Refactor sang absolute path workflow
- **Impact**: Users có thể query từ ANY project

### 🎉 Kết quả đạt được

✅ **Cross-project service**: MCP tool hoạt động từ bất kỳ project nào
✅ **UX improvement**: Không cần CD, dùng absolute paths
✅ **Consistent design**: Documentation match implementation
✅ **Memory alignment**: Full documentation trong .memory/
✅ **Git workflow**: Clean feature branch → main merge

### 🔄 Migration Guide

#### Từ old workflow:
```bash
cd /home/fong/Projects/mini-rag/multi-query
./run-multiquery.sh --list-pdfs
```

#### Sang new workflow:
```bash
# Từ BẤT KỲ đâu
/home/fong/Projects/mini-rag/multi-query/run-multiquery.sh --list-pdfs
```

---

**Commits**:
- 43da860: refactor(mcp): Remove max_sources param and add listNewRAGSources tool
- c802c8c: feat(mcp): Add NewRAG multi-query tool to MCP server
- 7827fee: refactor: Update queryNewRAG workflow to use absolute paths

---

## Phiên bản 0.1 (11/09/2025)

### 🚀 Tính năng mới

#### Pure Retrieval System  
- **Loại bỏ hoàn toàn OpenAI/LLM generation**: Chuyển từ RAG sang pure retrieval system
- **AI-to-AI pipeline integration**: Tối ưu cho việc feed context vào AI systems khác
- **Structured output format**: `[document.pdf] content...` với separator `---`
- **Source attribution**: Mỗi chunk đều có tên file nguồn để truy vết

#### Smart Caching System
- **Manifest-based tracking**: Sử dụng MD5 hash để detect thay đổi PDF files
- **Intelligent rebuild**: Chỉ rebuild khi files thực sự thay đổi
- **Performance boost**: Từ 45s rebuild → 0.17s cache load (265x faster)
- **Folder structure**: Vector store trong `.mini_rag_index/`, manifest.json ở root level

#### Results Management
- **Automated saving**: Mỗi query tự động save vào `/results/` folder
- **Timestamped files**: Format `{timestamp}-{uuid}.md` 
- **Structured markdown**: Bao gồm query, PDF directory, context chunks, metadata
- **Source tracking**: Ghi rõ file nguồn và nội dung cho từng chunk

#### Example Structure Reorganization
- **code-examples/**: Chứa demo scripts và AI integration examples
- **pdf-documents/**: Chứa sample PDFs với manifest tracking
- **Automation script**: `run.sh` với absolute paths, tự động activate venv

### 🔧 Cải thiện kỹ thuật

#### Configuration Updates
- **Pure HuggingFace**: Loại bỏ tất cả OpenAI dependencies  
- **Fallback embeddings**: DummyHashEmbeddings khi không có sentence-transformers
- **Environment variables**: Simplified config chỉ với HF embeddings
- **Error handling**: Graceful fallback cho offline operation

#### Performance Optimizations  
- **Lazy loading**: PDF loading/splitting chỉ khi cần rebuild vector store
- **Cached retrieval**: Skip hoàn toàn PDF processing khi có cache
- **Memory efficiency**: Optimized document loading và chunking
- **Fast startup**: 0.17s vs 45s cho subsequent runs

#### Code Quality
- **Modular architecture**: Tách biệt concerns theo pipeline pattern
- **Type hints**: Full type annotations với `from __future__ import annotations`
- **Error handling**: Comprehensive exception handling và logging
- **Rich console**: Beautiful console output với progress indicators

### 📚 Documentation

#### AI-Focused README
- **AI-to-AI integration patterns**: Shell, Python, API service examples
- **Query strategies**: Natural language, keyword/phrase, structured queries
- **Pipeline integration**: Comprehensive examples cho downstream AI systems
- **Performance metrics**: Detailed caching và retrieval benchmarks

#### Vietnamese Documentation  
- **CHANGELOGS.md**: Chi tiết thay đổi phiên bản bằng tiếng Việt
- **Code comments**: Vietnamese comments cho core functions
- **Error messages**: Vietnamese error output cho user experience

### 🏗️ Cấu trúc dự án

```
mini-rag/
├── src/minirag/           # Core modules
│   ├── config.py         # Settings với HF embeddings only
│   ├── embedder.py       # HF embeddings với fallback  
│   ├── pipeline.py       # Pure retrieval pipeline
│   ├── vectorstore.py    # FAISS với smart caching
│   ├── loader.py         # PDF document loading
│   ├── splitter.py       # Text chunking
│   └── utils.py          # Timing và utilities
├── example/
│   ├── code-examples/    # Demo scripts
│   └── pdf-documents/    # Sample PDFs với manifest  
├── results/              # Auto-saved query results
├── logs/                 # Application logs
├── run.sh               # Automation script
├── main-minirag.py      # Entry point
└── requirements.txt     # Dependencies
```

### 🎯 Use Cases

#### AI System Preprocessing
- Extract structured context từ PDF collections
- Feed vào downstream AI models
- Document-based RAG system backends  
- Automated research analysis workflows

#### Query Examples
```bash
# Natural language (comprehensive context)
./run.sh "What research methodologies are discussed?" /path/to/pdfs

# Keywords (specific term extraction)  
./run.sh "machine learning algorithms neural networks" /path/to/pdfs

# Structured (systematic analysis)
./run.sh "List: 1) methodologies 2) datasets 3) metrics" /path/to/pdfs
```

### 🔬 Technical Specifications

#### Dependencies
- **LangChain**: Document processing và retrieval
- **FAISS**: Vector similarity search  
- **Rich**: Console UI và progress indicators
- **Optional**: sentence-transformers (fallback to DummyHashEmbeddings)

#### Performance
- **First run**: ~45s (build vector index cho 7 research papers)
- **Cached runs**: ~0.17s (265x faster)
- **Memory**: Efficient với streaming file hashing
- **Storage**: Smart caching với MD5 tracking

#### Environment Variables
```bash
export HF_EMBEDDINGS_MODEL_NAME="sentence-transformers/all-MiniLM-L6-v2"
export CHUNK_SIZE=1200
export CHUNK_OVERLAP=150  
export TOP_K=4
```

### 🚧 Breaking Changes

#### Removed OpenAI Integration
- **KHÔNG còn**: `OPENAI_API_KEY`, `OPENAI_MODEL_NAME`
- **KHÔNG còn**: LLM generation trong pipeline
- **KHÔNG còn**: OpenAI embeddings option

#### API Changes
- `answer_question()` → returns pure context (không phải generated answer)
- `get_context()` → new primary function cho retrieval
- `build_or_load_vectorstore()` → không cần docs parameter

### 🎉 Kết quả đạt được

✅ **Cache Performance**: 265x speedup (45s → 0.17s)  
✅ **Pure Retrieval**: 100% context extraction, 0% generation  
✅ **AI Integration**: Complete examples cho 3 integration patterns  
✅ **Documentation**: Comprehensive Vietnamese docs  
✅ **Results Management**: Auto-save với structured markdown  
✅ **Offline Capable**: Hoạt động 100% offline với fallback embeddings  

---

**Lưu ý**: Đây là phiên bản đầu tiên focus vào pure retrieval cho AI-to-AI integration. Không còn support OpenAI LLM generation.