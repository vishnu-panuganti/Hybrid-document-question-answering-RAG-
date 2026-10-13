import re
from rank_bm25 import BM25Okapi


# =====================================
# Global BM25 State
# =====================================

bm25 = None
stored_chunks = []


# =====================================
# Text Preprocessing
# =====================================

def preprocess_text(text):

    return re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )


# =====================================
# Build BM25 Index
# =====================================

def build_bm25_index(
    chunks,
    document_id,
    filename,
    file_type
):

    global bm25
    global stored_chunks

    # Remove older copy of this document
    stored_chunks = [
        chunk
        for chunk in stored_chunks
        if chunk.get("document_id") != document_id
    ]

    # Add new document chunks
    for i, chunk in enumerate(chunks):

        stored_chunks.append({

            "chunk_id":
                f"{document_id}_chunk_{i}",

            "document_id":
                document_id,

            "filename":
                filename,

            "file_type":
                file_type,

            "page":
                chunk.get("page", 0),

            "text":
                chunk["text"]

        })

    # =====================================
    # Rebuild BM25
    # =====================================

    tokenized_chunks = [

        preprocess_text(
            chunk["text"]
        )

        for chunk in stored_chunks

    ]

    if not tokenized_chunks:

        bm25 = None

        print(
            "BM25 index is empty."
        )

        return

    bm25 = BM25Okapi(
        tokenized_chunks
    )

    print(
        "BM25 index built:",
        len(stored_chunks),
        "chunks across documents"
    )


# =====================================
# Rebuild BM25 Directly
# =====================================

def rebuild_bm25_index(chunks):

    global bm25
    global stored_chunks

    # Clear existing in-memory index
    stored_chunks = []

    # Copy all chunks
    for chunk in chunks:

        stored_chunks.append({

            "chunk_id":
                chunk["chunk_id"],

            "document_id":
                chunk["document_id"],

            "filename":
                chunk["filename"],

            "file_type":
                chunk["file_type"],

            "page":
                chunk.get("page", 0),

            "text":
                chunk["text"]

        })

    # =====================================
    # Nothing to index
    # =====================================

    if not stored_chunks:

        bm25 = None

        print(
            "BM25 index is empty."
        )

        return

    # =====================================
    # Tokenize chunks
    # =====================================

    tokenized_chunks = [

        preprocess_text(
            chunk["text"]
        )

        for chunk in stored_chunks

    ]

    # =====================================
    # Create BM25 index
    # =====================================

    bm25 = BM25Okapi(
        tokenized_chunks
    )

    print(
        "BM25 index rebuilt:",
        len(stored_chunks),
        "chunks"
    )


# =====================================
# BM25 Search
# =====================================

def search_bm25(
    question,
    n_results=12
):

    # =====================================
    # Check index
    # =====================================

    if (
        bm25 is None
        or not stored_chunks
    ):

        print(
            "BM25 index is empty during search."
        )

        return []

    # =====================================
    # Tokenize question
    # =====================================

    query_tokens = preprocess_text(
        question
    )

    if not query_tokens:

        print(
            "BM25 query contains no tokens."
        )

        return []

    # =====================================
    # Debug information
    # =====================================

    print(
        "BM25 query tokens:",
        query_tokens
    )

    print(
        "BM25 stored chunks:",
        len(stored_chunks)
    )

    # =====================================
    # Calculate BM25 scores
    # =====================================

    scores = bm25.get_scores(
        query_tokens
    )

    print(
        "BM25 scores:",
        scores
    )

    # =====================================
    # Sort by score
    # =====================================

    ranked_indexes = sorted(

        range(len(scores)),

        key=lambda i: scores[i],

        reverse=True

    )

    # =====================================
    # Build results
    # =====================================

    results = []

    for index in ranked_indexes[:n_results]:

        chunk = stored_chunks[index]

        results.append({

            "chunk_id":
                chunk["chunk_id"],

            "document_id":
                chunk["document_id"],

            "filename":
                chunk["filename"],

            "file_type":
                chunk["file_type"],

            "page":
                chunk.get("page", 0),

            "text":
                chunk["text"],

            "bm25_score":
                float(scores[index])

        })

    # =====================================
    # Debug result count
    # =====================================

    print(
        "BM25 matched results:",
        len(results)
    )

    return results