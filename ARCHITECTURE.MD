# System Architecture

## Document Processing Pipeline

```text
                        Upload Document
                               │
                ┌──────────────┴──────────────┐
                │                             │
        PDF / TXT / DOCX / CSV         SHA-256 Duplicate Check
                │                             │
                └──────────────┬──────────────┘
                               │
                       Text Extraction
                               │
                          Text Chunking
                    (1500 chars, 300 overlap)
                               │
                     Gemini Embedding Model
                               │
              ┌────────────────┴────────────────┐
              │                                 │
      ChromaDB Vector Store             BM25 Index
      (Semantic Retrieval)          (Keyword Retrieval)
              │                                 │
              └────────────────┬────────────────┘
                               │
                  Reciprocal Rank Fusion (RRF)
                               │
                      BGE Cross-Encoder Reranker
                               │
                      Top-K Relevant Context
                               │
                     Google Gemini Generation
                               │
                Grounded Answer + Source Pages
```

---

## Retrieval Workflow

```text
User Question
      │
      ▼
Generate Query Embedding
      │
      ├────────► ChromaDB Search
      │
      └────────► BM25 Search
                  │
                  ▼
        Reciprocal Rank Fusion
                  │
                  ▼
         BGE Cross-Encoder Reranker
                  │
                  ▼
         Top-5 Relevant Chunks
                  │
                  ▼
         Google Gemini LLM
                  │
                  ▼
      Final Answer + Source Pages
```

---

## Current Pipeline

1. Upload document
2. SHA-256 duplicate detection
3. Text extraction
4. Chunk generation
5. Gemini embedding generation
6. Store embeddings in ChromaDB
7. Build BM25 index
8. Hybrid retrieval using RRF
9. BGE reranking
10. Generate grounded answer using Gemini
11. Return answer with page-level sources