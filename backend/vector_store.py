import chromadb
# import uuid

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="document_chunks"
)


def store_chunks(chunks, embeddings, document_id, filename, file_type):

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        chunk_id = f"{document_id}_chunk_{i}"

        ids.append(chunk_id)
        documents.append(chunk["text"])

        metadatas.append({
            "chunk_id": chunk_id,
            "document_id": document_id,
            "filename": filename,
            "file_type": file_type,
            "page": chunk.get("page", 0)
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

def search_chunks(question_embedding):

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=12,
        include=["documents", "metadatas", "distances"]
    )

    relevant_chunks = []

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):

        relevant_chunks.append({
            "chunk_id": metadata["chunk_id"],
            "document_id": metadata["document_id"],
            "filename": metadata["filename"],
            "file_type": metadata["file_type"],
            "page": metadata.get("page", 0),
            "text": document,
            "distance": distance
        })

    return relevant_chunks