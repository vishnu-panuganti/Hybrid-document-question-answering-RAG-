from embeddings import get_embedding

text = "Deadlock occurs when two or more processes wait for each other."

embedding = get_embedding(text)

print(type(embedding))
print(len(embedding))
print(embedding[:10])