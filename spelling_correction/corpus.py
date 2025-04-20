from collections import defaultdict
from vocabulary import Vocabulary

class Corpus:
    """
    A class to represent a text corpus for spelling correction.
    """

    def __init__(self, text: str):
        """
        Initialize the Corpus with a given text.

        :param text: The text to be used for spelling correction.
        """
        self.text = text
        self.word_count = defaultdict(lambda: 0)
        self.total_words = 0
        self.dictionary = Vocabulary(None) # Initialize an empty dictionary
        self._build_corpus()

    def _build_corpus(self):
        """
        Process the text to build the word count dictionary and total word count.
        """
        words = self.text.split()
        self.total_words = len(words)
        for word in words:
            word = word.lower()
            self.word_count[word] += 1
            # all word in the corpus should be in the dictionary
            self.dictionary.add_word(word)
            
    def get_word_count(self, word: str) -> int:
        """
        Get the count of a specific word in the corpus.

        :param word: The word to count.
        :return: The count of the word.
        """
        return self.word_count[word.lower()]
    
    def words_with_specific_count(self, count: int) -> int:
        """
        Get the number of words that have a specific count.

        :param count: The specific count to look for.
        :return: The number of words with the specified count.
        """
        return sum(1 for word_count in self.word_count.values() if word_count == count)