from fastapi import HTTPException
from google.genai.errors import ClientError
import chromadb
import pandas as pd


def handle_exception(exception: Exception):

    # -------------------------
    # Gemini API Errors
    # -------------------------
    if isinstance(exception, ClientError):

        message = str(exception)

        if "RESOURCE_EXHAUSTED" in message:
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please try again later."
            )

        if "API_KEY_INVALID" in message:
            raise HTTPException(
                status_code=401,
                detail="Invalid Gemini API key."
            )

        raise HTTPException(
            status_code=502,
            detail="Failed to communicate with Gemini API."
        )

    # -------------------------
    # CSV Parsing Errors
    # -------------------------
    if isinstance(exception, pd.errors.ParserError):
        raise HTTPException(
            status_code=400,
            detail="Invalid CSV format."
        )

    # -------------------------
    # ChromaDB Errors
    # -------------------------
    if isinstance(exception, chromadb.errors.ChromaError):
        raise HTTPException(
            status_code=500,
            detail="Vector database operation failed."
        )

    # -------------------------
    # File Errors
    # -------------------------
    if isinstance(exception, FileNotFoundError):
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    # -------------------------
    # Value Errors
    # -------------------------
    if isinstance(exception, ValueError):
        raise HTTPException(
            status_code=400,
            detail=str(exception)
        )

    # -------------------------
    # Unexpected Errors
    # -------------------------
    print("Unexpected error:", exception)

    raise HTTPException(
        status_code=500,
        detail="An unexpected server error occurred."
    )