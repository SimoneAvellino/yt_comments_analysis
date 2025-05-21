import re
import unicodedata
import nltk
from youtube_comment_downloader import YoutubeCommentDownloader
from .text_cleaner import clean_text


# Ensure NLTK tokenizer is available
nltk.download('punkt')

def retrieve_comments(url, number_of_comments):
    """
    Fetches YouTube comments from a given video URL.

    Args:
        url (str): YouTube video URL.
        number_of_comments (int): Number of top-level comments to retrieve.

    Returns:
        list of dict: Each dict contains 'username', 'comment'.
    """
    

    downloader = YoutubeCommentDownloader()
    generator = downloader.get_comments_from_url(url)

    result = []
    for i, comment in enumerate(generator):
        if i >= number_of_comments:
            break
        raw_text = comment.get("text", "")
        result.append({
            "username": comment.get("author", "unknown"),
            "comment": raw_text
        })

    return result

# Pytube is apparently broken right now, that seems to happens often. I added a new function using yt-dlp instead.
# yt-dlp is apparently much more stable then pytube, it's working for me.
# Downside is that it's technically a command-line tool, so we have to use subprocess or something like that, but it's not that complex.

import subprocess
import json

def get_video_metadata_with_ytdlp(url):
    result = subprocess.run(
        ["yt-dlp", "--dump-json", "--skip-download", url],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        print("❌ Error:", result.stderr)
        return None
    return json.loads(result.stdout)

# this function can then be called with this code:
meta = get_video_metadata_with_ytdlp(url)
print(meta["title"], meta["description"])
    
def get_sentiment(comment):
    """
    Function to get sentiment of a comment.
    
    Args:
        comment (str): The comment text.

    Returns:
        int: 1 for positive, 0 for neutral, -1 for negative.
    """
    pass
