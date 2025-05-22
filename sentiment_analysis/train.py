from sklearn.model_selection import train_test_split
from spelling_correction.spelling_corrector import SpellingCorrector
from utils.text_cleaner import clean_text
from sentiment_analysis.naive_bayes import NaiveBayes

from nltk import download
from nltk.corpus import brown
from spelling_correction.corpus import Corpus
from spelling_correction.language_model import GoodTuringLanguageModel
from spelling_correction.channel_model import ChannelModel
from spelling_correction.spelling_corrector import SpellingCorrector

import pandas as pd

def train_model():
    print("Loading dataset...")
    dataset_path = './dataset/YoutubeCommentsDataSet.csv'
    dataset = pd.read_csv(dataset_path)
    
    print("Preprocessing dataset...")
    dataset = dataset.dropna()
    dataset = dataset.drop_duplicates()
    dataset = dataset.reset_index(drop=True)
    print("Cleaning text...")
    dataset['Comment'] = dataset['Comment'].apply(clean_text)
    print("Correcting spelling...")
    corpus = Corpus(" ".join(brown.words()))
    language_model = GoodTuringLanguageModel(corpus)
    channel_model = ChannelModel(language_model.vocabulary, './data/common_errors.txt')
    spelling_corrector = SpellingCorrector(language_model, channel_model)
    dataset['Comment'] = dataset['Comment'].apply(spelling_corrector.correct)
    
    print("Splitting dataset...")
    train_df, test_df = train_test_split(dataset, test_size=0.2, random_state=42)
    
    print("Training model...")
    model = NaiveBayes()
    model.train(train_df)
    print("Training complete.")
    
    print("Testing model...")
    predictions = model.test(test_df)
    accuracy = (predictions == test_df['Sentiment']).mean()
    print(f"Accuracy: {accuracy:.2f}")
    
    print("Saving model...")
    model.saveModel('naive_bayes_model.pkl')
    
if __name__ == "__main__":
    train_model()