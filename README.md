# AskPDF

A Hybrid Retrieval-Augmented Generation (RAG) application for document question answering. Upload PDF, TXT, DOCX, or CSV files and ask natural language questions. The system retrieves relevant document context using hybrid search and generates grounded responses with Google Gemini.

## Features

- Multi-format document support (PDF, TXT, DOCX, CSV)
- Hybrid retrieval using ChromaDB + BM25 + Reciprocal Rank Fusion (RRF)
- Google Gemini for answer generation
- Configurable text chunking (1500 characters, 300 overlap)
- Metadata-aware indexing (Document ID, Chunk ID, Filename, Page Number)
- Page-level source attribution
- SHA-256 duplicate document detection
- Multi-document storage
- FastAPI backend
- React + Vite frontend

## Architecture
## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the complete system architecture and retrieval workflow.
# System Architecture

## Document Processing Pipeline


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




## Retrieval Workflow

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





## Tech Stack

### Backend

- Python
- FastAPI
- Google Gemini API
- ChromaDB
- rank-bm25
- Sentence Transformers
- python-docx
- pandas

### Frontend

- React
- Vite
- CSS

## Project Structure

document-qa
├── backend
│   ├── main.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── bm25_search.py
│   ├── hybrid_search.py
│   ├── reranker.py
│   ├── duplicate_checker.py
│   ├── chunker.py
│   └── readers
├── frontend
│   ├── src
│   └── public
└── README.md


## Installation

### Clone the repository

git clone https://github.com/<your-username>/AskPDF.git
cd AskPDF


### Backend Setup

cd backend

python -m venv venv


**Windows**

venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` folder.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Start the backend

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will run at:

```
http://localhost:5173
```

## Evaluation

The retrieval pipeline is evaluated using RAGAS with metrics including:

- Recall@5
- Precision@5
- Mean Reciprocal Rank (MRR)
- Faithfulness

## Future Improvements

- Conversation memory
- Document-specific retrieval
- PPTX support
- XLSX support
- Markdown support
- OCR for scanned documents
- Authentication
- Streaming responses
- Docker deployment

## License

This project is licensed under the MIT License.