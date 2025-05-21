from nltk import download
from utils.api import retrieve_comments, get_video_metadata_with_ytdlp, get_sentiment
from utils.text_cleaner import clean_text
import argparse
from spelling_correction.corpus import Corpus
import textwrap
from tqdm import tqdm

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

from sentiment_analysis.naive_bayes import NaiveBayes
# Load the model
model = NaiveBayes()
model = model.loadModel('naive_bayes_model.pkl')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("youtube_url", help="URL of the YouTube video")
    parser.add_argument(
        "--number_of_comments",
        type=int,
        default=None,
        help="Number of comments to retrieve (default: All comments)",
    )

    args = parser.parse_args()

    youtube_url = args.youtube_url
    
    info = get_video_metadata_with_ytdlp(youtube_url)
    # print(info.keys())
    
    comments = retrieve_comments(youtube_url, args.number_of_comments)
    
    print("\033[91mVideo Title:\033[0m\n    ", info['title'])
    print("\033[91mVideo Description:\033[0m", )
    for line in textwrap.wrap(info['description'], width=50):
        print("    ", line)
    print("\033[91mStats on comments:\033[0m")
    print("    ", f"Number of comments retrieved {'(all)' if not args.number_of_comments else ''}:", len(comments))
    print("    ", "Number of likes:", info['like_count'])
    print("    ", "Number of views:", info['view_count'])
    
    sentiment = {
        "positive": 0,
        "negative": 0,
        "neutral": 0
    }
    
    # # Spelling correction for each comment
    for comment in tqdm(comments, desc="Evaluating comments", unit="comment"):
        author = comment['username']
        original_comment = comment['comment']
        cleaned_comment = clean_text(original_comment)
        # spelling correction so that the comment is parsed correctly from the machine learning model
        comment_for_model = spelling_corrector.correct(cleaned_comment)
        classification, (prob_pos, prob_neu, prob_neg) = model.predict(comment_for_model)
        sentiment[classification] += 1
    
    print("\033[91mSentiment Analysis:\033[0m")
    print("    ", "Positive:", sentiment["positive"]/len(comments) * 100, "%")
    print("    ", "Negative:", sentiment["negative"]/len(comments) * 100, "%")
    print("    ", "Neutral:", sentiment["neutral"]/len(comments) * 100, "%")


if __name__ == "__main__":
    main()