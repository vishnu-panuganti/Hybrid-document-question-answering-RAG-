import pandas as pd


def extract_text_from_csv(file_path):
    df = pd.read_csv(file_path)

    rows = []

    for _, row in df.iterrows():
        rows.append(
            ", ".join(f"{col}: {row[col]}" for col in df.columns)
        )

    text = "\n".join(rows)

    return [
        {
            "page": 1,
            "text": text
        }
    ] 