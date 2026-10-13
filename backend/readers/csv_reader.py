import pandas as pd


def extract_text_from_csv(file_path):

    df = pd.read_csv(file_path)

    chunks = []

    for index, row in df.iterrows():

        row_text = ", ".join(
            f"{column}: {row[column]}"
            for column in df.columns
        )

        chunks.append({
            "page": index + 1,
            "text": row_text
        })

    return chunks