import os
import re
from collections import Counter

import pandas as pd

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "headlines.csv")
OUTPUT_DIR = "/opt/airflow/working_data"
OUTPUT_FILE = "top_keywords.xlsx"
TOP_N = 10

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "for", "with",
    "at", "by", "from", "as", "is", "are", "was", "were", "be", "after", "over",
    "new", "into", "its", "it", "this", "that", "how", "why", "what", "amid",
    "says", "will", "than", "more", "up", "out", "about",
}


def load_headlines():
    """Reads the headlines CSV and returns the headlines as a list of strings."""
    df = pd.read_csv(DATA_PATH)
    if "headline" not in df.columns:
        raise ValueError("headlines.csv must have a 'headline' column")
    headlines = df["headline"].dropna().astype(str).tolist()
    if not headlines:
        raise ValueError("headlines.csv has no headlines")
    print(f"Loaded {len(headlines)} headlines")
    return headlines


def clean_headlines(headlines):
    """Lowercases each headline, removes punctuation and numbers, and drops filler words."""
    words = []
    for headline in headlines:
        text = re.sub(r"[^a-z\s]", " ", headline.lower())
        for word in text.split():
            if len(word) > 2 and word not in STOPWORDS:
                words.append(word)
    print(f"Kept {len(words)} keywords after cleaning")
    return words


def count_keywords(words):
    """Counts each keyword and returns the most common ones as [keyword, count] pairs."""
    top = Counter(words).most_common(TOP_N)
    for word, count in top:
        print(f"{word}: {count}")
    return [[word, count] for word, count in top]


def save_to_excel(top_keywords):
    """Saves the top keywords to an Excel file in working_data and returns its path."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    df = pd.DataFrame(top_keywords, columns=["keyword", "count"])
    df.to_excel(output_path, index=False)
    print(f"Saved top keywords to {output_path}")
    return output_path
