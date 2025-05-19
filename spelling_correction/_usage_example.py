from corpus import Corpus
from nltk import download

# -------- Corpus from nltk --------
from nltk.corpus import brown
corpus = Corpus(" ".join(brown.words()))

# -------- language Model ------------
from language_model import GoodTuringLanguageModel
language_model = GoodTuringLanguageModel(corpus)

# --------- Channel Model ------------
from channel_model import ChannelModel
channel_model = ChannelModel(language_model.vocabulary, './data/common_errors.txt')

# -------- Spelling Correction -------
from spelling_corrector import SpellingCorrector
spelling_corrector = SpellingCorrector(language_model, channel_model)

# --------- Example Usage ---------

# example of correcting a sentence
sentence = "This is a smple sentnce with erors."
corrected_sentence = spelling_corrector.correct(sentence)
print(f"Original: {sentence}")
print(f"Corrected: {corrected_sentence}")

