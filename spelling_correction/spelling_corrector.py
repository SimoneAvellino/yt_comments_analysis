from spelling_correction.language_model import LanguageModel
from spelling_correction.channel_model import ChannelModel
import re

class SpellingCorrector:
    
    def __init__(self, language_model:LanguageModel, channel_model:ChannelModel):

        """
        Initializes the SpellingCorrector with a language model and a channel model.
        :param language_model: The language model to be used for correction.
        """
        self.language_model = language_model
        self.channel_model = channel_model
        
    def tokenize(self, sentence: str) -> list[str]:
        """
        Splits sentence into tokens, keeping punctuation as separate tokens.
        Example: "Hello, world!" → ['Hello', ',', 'world', '!']
        """
        return re.findall(r"\w+|[^\w\s]", sentence, re.UNICODE)

    def correct(self, sentence: str) -> str:
        """ If the word is not in the dictionary, generate candidates and choose the best one.

        :param sentence: The sentence to be corrected.
        :return: The corrected sentence.
        """

        tokens = self.tokenize(sentence)
        
        for i, token in enumerate(tokens):
            # Skip if the token is a punctuation mark
            if not token.isalpha():
                continue
            # Check if the token is in the language model
            if not token in self.language_model:
                # If not, generate candidates and choose the best one
                candidates = self.channel_model.similar_words(token)
                best_candidate = self.choose_best_candidate(candidates, token)
                if len(candidates) == 0:
                    continue
                sentence = sentence.replace(token, best_candidate)
                
        return sentence
    
    def choose_best_candidate(self, candidates: list[(str, str, int)], misspelled_word: str) -> str:
        """
        Choose the best candidate based on the language model.
        
        :param candidates: The list of candidates. Format: [(operation, word, i), ...] where operation is the edit operation, word is the candidate word and i is the index of the character in the original word.
        :param token: The original token.
        :return: The best candidate.
        """
        best_candidate = None
        best_probability = -1
        for op, w, i in candidates:
            # w := correct word (the i-th element of candidates)
            p_w = self.language_model.probability(w)
            p_misspelled_word_given_w = self.channel_model.probability(misspelled_word, w, op, i)
            
            # maximum likelihood estimation
            prob = p_w * p_misspelled_word_given_w
            if prob > best_probability:
                best_probability = prob
                best_candidate = w
                
        return best_candidate