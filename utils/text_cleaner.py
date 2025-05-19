import re
import unicodedata

def clean_text(text):
    text = text.lower()
    text = re.sub(r'@\w+', '', text)  # remove mentions
    text = re.sub(r"http\S+|www\.\S+", "", text)  # remove URLs
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8", "ignore")  # remove emojis
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()
    return text