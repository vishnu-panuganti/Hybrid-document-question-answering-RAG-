import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_NAME = "BAAI/bge-reranker-v2-m3"

# Load once when backend starts
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME
)

model.eval()


def rerank_chunks(question, chunks, top_k=5):

    if not chunks:
        return []

    pairs = [
        [question, chunk["text"]]
        for chunk in chunks
    ]

    # Tokenize query + passage together
    inputs = tokenizer(
        pairs,
        padding=True,
        truncation=True,
        max_length=256,
        return_tensors="pt"
    )

    # No gradients needed for inference
    with torch.no_grad():
        logits = model(**inputs).logits.view(-1)

        # Convert raw relevance scores to 0-1
        scores = torch.sigmoid(logits).tolist()

    reranked_chunks = []

    for chunk, score in zip(chunks, scores):
        reranked_chunks.append({
            **chunk,
            "rerank_score": float(score)
        })

    reranked_chunks.sort(
        key=lambda chunk: chunk["rerank_score"],
        reverse=True
    )

    return reranked_chunks[:top_k]