def reciprocal_rank_fusion(dense_chunks, bm25_chunks, k=60):
    fused = {}

    # Dense ranking
    for rank, chunk in enumerate(dense_chunks, start=1):
        chunk_id = chunk["chunk_id"]

        if chunk_id not in fused:
            fused[chunk_id] = {
                **chunk,
                "rrf_score": 0.0
            }

        fused[chunk_id]["rrf_score"] += 1 / (k + rank)

    # BM25 ranking
    for rank, chunk in enumerate(bm25_chunks, start=1):
        chunk_id = chunk["chunk_id"]

        if chunk_id not in fused:
            fused[chunk_id] = {
                **chunk,
                "rrf_score": 0.0
            }

        fused[chunk_id]["rrf_score"] += 1 / (k + rank)

    # Convert dictionary to list
    fused_chunks = list(fused.values())

    # Highest RRF score first
    fused_chunks.sort(
        key=lambda chunk: chunk["rrf_score"],
        reverse=True
    )

    return fused_chunks