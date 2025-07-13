# utils/text_utils.py

import re
from typing import List

def clean_text(text: str) -> str:
    """
    Basic text cleaning: lowercase, remove special characters except spaces.
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def split_text_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split long text into overlapping chunks for easier processing in NLP tasks.

    Args:
        text (str): The input text to split.
        chunk_size (int): Number of characters per chunk.
        overlap (int): Number of overlapping characters between chunks.

    Returns:
        List[str]: List of text chunks.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap  # move start with overlap

    return chunks
