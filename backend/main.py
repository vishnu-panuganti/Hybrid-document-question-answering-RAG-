from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pdf_reader import extract_text_from_pdf
from chunker import split_text_into_chunks
from embeddings import get_embedding, generate_answer
from vector_store import store_chunks, search_chunks
from bm25_search import build_bm25_index, search_bm25
from hybrid_search import reciprocal_rank_fusion
from reranker import rerank_chunks
import time
from text_reader import extract_text_from_txt
from duplicate_checker import (
    calculate_file_hash,
    is_duplicate,
    register_document,
    get_existing_document,
    load_hashes
)
 

import uuid
import os
import shutil


app = FastAPI()


# =====================================
# CORS Configuration
# =====================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


# =====================================
# Home
# =====================================
@app.get("/")
def home():
    return {"message": "Document QA Backend Running"}


# =====================================
# Upload Document
# =====================================
@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    # Unique ID for this document
    document_id = str(uuid.uuid4())

    # Get file type
    file_extension = os.path.splitext(file.filename)[1].lower()
    file_type = file_extension.replace(".", "")

    file_path = f"uploads/{file.filename}"

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    file_hash = calculate_file_hash(file_path)
    print("Current Hash:", file_hash)
    print("Hashes:", load_hashes())
    print("Duplicate:", is_duplicate(file_hash))

    if is_duplicate(file_hash):

        existing = get_existing_document(file_hash)

        return {
            "message": "Document already uploaded.",
            "duplicate": True,
            "document_id": existing["document_id"],
            "filename": existing["filename"]
        }    

    if if file_type == "pdf":
    extracted_text = extract_text_from_pdf(file_path)

elif file_type == "txt":
    extracted_text = extract_text_from_txt(file_path)



else:
    return {
        "error": f"Unsupported file type: {file_type}"
    }

    # Split extracted text into chunks
    chunks = split_text_into_chunks(extracted_text)

    # Build BM25 index
    build_bm25_index(
        chunks,
        document_id,
        file.filename,
        file_type
    )

    # Generate embeddings
    embeddings = []

    for chunk in chunks:
        embedding = get_embedding(chunk["text"])
        embeddings.append(embedding)

    # Store chunks + embeddings in ChromaDB
    store_chunks(
        chunks,
        embeddings,
        document_id,
        file.filename,
        file_type
    )
    register_document(
    file_hash,
    document_id,
    file.filename
)

    return {
        "message": "Document processed successfully",
        "document_id": document_id,
        "filename": file.filename,
        "file_type": file_type,
        "number_of_chunks": len(chunks)
    }


# =====================================
# Greetings
# =====================================
GREETINGS = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
    "thanks",
    "thank you",
    "bye"
}


# =====================================
# Ask Question
# =====================================
@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question
    user_question = question.strip().lower()

    # Handle greetings
    if user_question in GREETINGS:

        responses = {
            "hi": "Hello! Welcome back, how can I help you with your documents today?",
            "hello": "Hello! 👋 How can I help you with your documents today?",
            "hey": "Hey! 👋 What would you like to know about your documents?",
            "good morning": "Good morning! ☀️ How can I assist you today?",
            "good afternoon": "Good afternoon! 😊 How can I help?",
            "good evening": "Good evening! 🌙 How can I help?",
            "thanks": "You're welcome! 😊",
            "thank you": "You're welcome! 😊",
            "bye": "Goodbye! Have a great day! 👋"
        }

        return {
            "question": question,
            "answer": responses[user_question]
        }

    # =====================================
    # Dense Search
    # =====================================

    question_embedding = get_embedding(question)

    relevant_chunks = search_chunks(question_embedding)

    print("\nDENSE SEARCH CHUNKS:")

    for chunk in relevant_chunks:
        print(
            "Chunk:", chunk["chunk_id"],
            "File:", chunk["filename"],
            "| Page:", chunk["page"],
            "| Distance:", chunk["distance"]
        )

    # =====================================
    # BM25 Search
    # =====================================

    bm25_chunks = search_bm25(question)

    print("\nBM25 SEARCH RESULTS:")

    for chunk in bm25_chunks:
        print(
            "File:", chunk["filename"],
            "| Page:", chunk["page"],
            "| BM25 Score:", chunk["bm25_score"]
        )

    print("\nQuestion:")
    print(question)

    # =====================================
    # =====================================
    # Hybrid Search - RRF
    # =====================================

    hybrid_chunks = reciprocal_rank_fusion(
        relevant_chunks,
        bm25_chunks
    )

    print("\nHYBRID RRF RESULTS:")

    for chunk in hybrid_chunks:
        print(
            "File:", chunk["filename"],
            "| Page:", chunk["page"],
            "| RRF Score:", chunk["rrf_score"]
        )
        # =====================================
    # BGE Reranking
    # =====================================
# Send only strongest RRF candidates to BGE
    rerank_candidates = hybrid_chunks[:8]
    # Start timer BEFORE BGE
    start = time.perf_counter()
    final_chunks = rerank_chunks(
        question,
        rerank_candidates,
        top_k=5
    )
    elapsed = time.perf_counter() - start

    print(f"\nBGE RERANK TIME: {elapsed:.2f} seconds")

    print("\nBGE RERANKED RESULTS:")

    for chunk in final_chunks:
        print(
            "File:", chunk["filename"],
            "| Page:", chunk["page"],
            "| Rerank Score:", chunk["rerank_score"]
        )
    # =====================================
    # Generate Answer
    # =====================================

    # Still using dense results only for Gemini.
    # Hybrid fusion will be added next.
    context = "\n\n".join(
        chunk["text"] for chunk in final_chunks
    )

    answer = generate_answer(context, question)

    # =====================================
    # Sources
    # =====================================

    sources = []

    for chunk in final_chunks:

        source = {
            "filename": chunk["filename"],
            "page": chunk["page"]
        }

        if source not in sources:
            sources.append(source)

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }