from spelling_correction.corpus import Corpus
from abc import ABC, abstractmethod
from spelling_correction.vocabulary import Vocabulary

class LanguageModel(ABC):
    
    def __init__(self, corpus: Corpus):
        self.corpus = corpus
        self.vocabulary = Vocabulary(corpus.text)
        
    @abstractmethod
    def probability(self, word: str) -> float:
        """
        Calculate the probability of a word in the corpus.
        """
        pass
    
    def __contains__(self, word: str) -> bool:
        """
        Check if a word is in the vocabulary.
        """
        return word in self.vocabulary
    
class GoodTuringLanguageModel(LanguageModel):
    
    def __init__(self, corpus: Corpus):
        super().__init__(corpus)
        
    def probability(self, word: str) -> float:
        
        c = self.corpus.get_word_count(word)
        
        if c == 0:
            c_star = self.corpus.words_with_specific_count(1) / self.corpus.total_words
        else:
            c_star = (c + 1) * self.corpus.words_with_specific_count(c + 1) / self.corpus.words_with_specific_count(c)
        
        return c_star / self.corpus.total_words