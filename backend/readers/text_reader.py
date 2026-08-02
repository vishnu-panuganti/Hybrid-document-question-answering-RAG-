def extract_text_from_txt(file_path):
    """
    Extract text from a TXT file and return it in the same
    structure used by the PDF reader.

    TXT files do not have pages, so the entire file is
    currently treated as page 1.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        # Remove unnecessary whitespace
        text = text.strip()

        if not text:
            return []

        return [
            {
                "page": 1,
                "text": text
            }
        ]

    except UnicodeDecodeError:
        # Fallback for text files that are not UTF-8 encoded
        with open(file_path, "r", encoding="latin-1") as file:
            text = file.read().strip()

        if not text:
            return []

        return [
            {
                "page": 1,
                "text": text
            }
        ]

    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return []