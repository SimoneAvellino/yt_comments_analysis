import re
import unicodedata
import nltk
from nltk.tokenize import word_tokenize

try:
    from youtube_comment_downloader import YoutubeCommentDownloader
except ModuleNotFoundError:
    print("❌ ERROR: 'youtube_comment_downloader' is not installed.")
    print("➡️  Install it using pip:")
    print("    pip install youtube-comment-downloader")
    raise

# Ensure NLTK tokenizer is available
nltk.download('punkt')

def retrieve_comments(url, number_of_comments):
    """
    Fetches, cleans, and tokenizes YouTube comments from a given video URL.

    Args:
        url (str): YouTube video URL.
        number_of_comments (int): Number of top-level comments to retrieve.

    Returns:
        list of dict: Each dict contains 'username', 'comment', and 'tokens'.
    """
    def clean_text(text):
        text = text.lower()
        text = re.sub(r'@\w+', '', text)  # remove mentions
        text = re.sub(r"http\S+|www\.\S+", "", text)  # remove URLs
        text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8", "ignore")  # remove emojis
        text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
        text = re.sub(r"\s+", " ", text).strip()
        return text

    downloader = YoutubeCommentDownloader()
    generator = downloader.get_comments_from_url(url)

    result = []
    for i, comment in enumerate(generator):
        if i >= number_of_comments:
            break
        raw_text = comment.get("text", "")
        cleaned = clean_text(raw_text)
        tokens = word_tokenize(cleaned)
        result.append({
            "username": comment.get("author", "unknown"),
            "comment": cleaned,
            "tokens": tokens
        })

    return result
