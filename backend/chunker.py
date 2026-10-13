from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text_into_chunks(pages, chunk_size=300, overlap=50):
    chunks = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    for page_data in pages:
        page_number = page_data["page"]
        text = page_data["text"].strip()

        if not text:
            continue

        split_chunks = splitter.split_text(text)

        for chunk_text in split_chunks:
            if len(chunk_text.strip()) >= 100:
                chunks.append({
                    "text": chunk_text.strip(),
                    "page": page_number
                })

    return chunks