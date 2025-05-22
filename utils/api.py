import re
import unicodedata
import nltk
from youtube_comment_downloader import YoutubeCommentDownloader
import subprocess
import json

nltk.download('punkt', quiet=True)

def retrieve_comments(url, number_of_comments=None):
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
        if number_of_comments  and i >= number_of_comments:
            break
        raw_text = comment.get("text", "")
        result.append({
            "username": comment.get("author", "unknown"),
            "comment": raw_text
        })

    return result

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
