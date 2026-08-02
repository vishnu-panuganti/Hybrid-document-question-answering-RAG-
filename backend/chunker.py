def split_text_into_chunks(pages, chunk_size=1500, overlap=300):
    chunks = []

    for page_data in pages:
        page_number = page_data["page"]
        text = page_data["text"].strip()

        # Skip empty pages
        if not text:
            continue

        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            chunk_text = text[start:end].strip()

            # Avoid storing tiny useless chunks
            if len(chunk_text) >= 100:
                chunks.append({
                    "text": chunk_text,
                    "page": page_number
                })

            # Reached the end of the page
            if end == len(text):
                break

            # Move forward but preserve overlap
            start = end - overlap

    return chunks