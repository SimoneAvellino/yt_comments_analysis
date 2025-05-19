import re
import unicodedata
import nltk
from youtube_comment_downloader import YoutubeCommentDownloader
from .text_cleaner import clean_text
from pytube import YouTube


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


def retrieve_video_info(url):
    """
    Fetches YouTube video information from a given video URL.

    Args:
        url (str): YouTube video URL.

    Returns:
        dict: Video information including title, description, and view count.
    """
    yt = YouTube(url)
    
    return {
        "title": yt.title,
        "description": yt.description
    }