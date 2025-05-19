from nltk import download
from utils.api import retrieve_comments, retrieve_video_info, get_sentiment
from utils.text_cleaner import clean_text
import argparse
from spelling_correction.corpus import Corpus

# -------- Corpus from nltk --------
from nltk.corpus import brown
corpus = Corpus(" ".join(brown.words()))

# -------- language Model ------------
from spelling_correction.language_model import GoodTuringLanguageModel
language_model = GoodTuringLanguageModel(corpus)

# --------- Channel Model ------------
from spelling_correction.channel_model import ChannelModel
channel_model = ChannelModel(language_model.vocabulary, './data/common_errors.txt')

# -------- Spelling Correction -------
from spelling_correction.spelling_corrector import SpellingCorrector
spelling_corrector = SpellingCorrector(language_model, channel_model)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("youtube_url", help="URL of the YouTube video")

    args = parser.parse_args()

    youtube_url = args.youtube_url
    
    # info = retrieve_video_info(youtube_url)
    info = {
        "title": "Sample Video Title",
        "description": "Sample video description."
    }
    comments = retrieve_comments(youtube_url, 100)
    
    print("Video Title:", info['title'])
    print("Video Description:", info['description'])
    
    total_sentiment = 0
    
    # Spelling correction for each comment
    for comment in comments:
        author = comment['username']
        original_comment = comment['comment']
        cleaned_comment = clean_text(original_comment)
        # spelling correction so that the comment is parsed correctly from the machine learning model
        comment_for_model = spelling_corrector.correct(cleaned_comment)
        
        total_sentiment += get_sentiment(comment_for_model)
        
    if total_sentiment > 0:
        sentiment = "Positive"
    elif total_sentiment < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
            
    print(f"The video has a {sentiment} sentiment.")

if __name__ == "__main__":
    main()