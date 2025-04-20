import nltk
from nltk.corpus import cess_esp

class Vocabulary:
    
    def __init__(self, text: str = None):
        """
        Initializes the Vocabulary with a set of words.
        
        :param text: Optional text to initialize the vocabulary. If None, an empty vocabulary is created.
        """
        self.words = set()
        if text is not None:
            self.words = set(word.lower() for word in text.split())
        
    def __contains__(self, word: str) -> bool:
        """
        Checks if a word is in the Vocabulary.
        
        :param word: The word to check.
        :return: True if the word is in the vocabulary, False otherwise.
        """
        return word.lower() in self.words
    
    def add_word(self, word: str):
        """
        Adds a word to the Vocabulary.
        
        :param word: The word to add.
        """
        self.words.add(word.lower())