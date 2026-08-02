import re
from rank_bm25 import BM25Okapi


bm25 = None
stored_chunks = []


def preprocess_text(text):
    return re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())


def build_bm25_index(chunks, document_id, filename, file_type):
    global bm25, stored_chunks

    # Remove an older copy of this document if present
    stored_chunks = [
        chunk for chunk in stored_chunks
        if chunk.get("document_id") != document_id
    ]

    # Add this document's chunks
    for i, chunk in enumerate(chunks):

        stored_chunks.append({
            "chunk_id": f"{document_id}_chunk_{i}",
            "document_id": document_id,
            "filename": filename,
            "file_type": file_type,
            "page": chunk.get("page", 0),
            "text": chunk["text"]
        })

    # Rebuild BM25 across ALL documents
    tokenized_chunks = [
        preprocess_text(chunk["text"])
        for chunk in stored_chunks
    ]

    bm25 = BM25Okapi(tokenized_chunks)

    print(
        f"BM25 index built: "
        f"{len(stored_chunks)} chunks across documents"
    )

def search_bm25(question, n_results=12):

    if bm25 is None or not stored_chunks:
        return []

    query_tokens = preprocess_text(question)

    if not query_tokens:
        return []

    scores = bm25.get_scores(query_tokens)

    ranked_indexes = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )

    results = []

    for index in ranked_indexes[:n_results]:

        # Skip chunks with no BM25 match
        if scores[index] <= 0:
            continue

        chunk = stored_chunks[index]

        results.append({
            "chunk_id": chunk["chunk_id"],
            "document_id": chunk["document_id"],
            "filename": chunk["filename"],
            "file_type": chunk["file_type"],
            "page": chunk.get("page", 0),
            "text": chunk["text"],
            "bm25_score": float(scores[index])
        })

    return results