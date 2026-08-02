from PyPDF2 import PdfReader


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text()

        if page_text:

            pages.append({
                "page": page_number,
                "text": page_text
            })

    return pages