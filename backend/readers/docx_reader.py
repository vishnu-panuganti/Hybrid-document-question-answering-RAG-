from docx import Document


def extract_text_from_docx(file_path):
    document = Document(file_path)

    pages = []

    text = ""

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"

    pages.append({
        "page": 1,
        "text": text
    })

    return pages