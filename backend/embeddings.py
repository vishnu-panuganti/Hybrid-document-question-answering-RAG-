import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


def generate_answer(context, question):
    prompt = f"""
    You are a helpful document assistant.

    Context:
    {context}

    Question:
    {question}

    Instructions:
    - Answer only using the provided context.
    - If the answer is not present in the context, say:
      "I could not find the answer in the uploaded document."
    - Explain the answer in simple and clear language.
    """

    response = client.models.generate_content(
       model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text