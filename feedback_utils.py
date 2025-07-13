# utils/feedback_utils.py

import re
from collections import Counter
from textblob import TextBlob

def clean_feedback_text(text: str) -> str:
    """
    Clean raw feedback text by lowering case and removing special characters.
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_sentiment_scores(text: str) -> dict:
    """
    Get polarity and subjectivity sentiment scores using TextBlob.

    Returns:
        dict: {'polarity': float, 'subjectivity': float}
    """
    blob = TextBlob(text)
    return {'polarity': blob.sentiment.polarity, 'subjectivity': blob.sentiment.subjectivity}

def extract_top_keywords(text: str, top_n: int = 20) -> list:
    """
    Extract top N keywords by frequency from cleaned text.

    Returns:
        list of tuples: [(word, count), ...]
    """
    words = text.split()
    word_counts = Counter(words)
    return word_counts.most_common(top_n)
