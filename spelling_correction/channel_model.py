from spelling_correction.vocabulary import Vocabulary
import re

INSERT = "insert"
DELETE = "delete"
SUBSTITUTE = "substitute"
TRANSPOSE = "transpose"

class ChannelModel:
    
    def __init__(self, vocabulary: Vocabulary, common_errors_file: str):
        """
        Initializes the ChannelModel with a vocabulary.
        :param vocabulary: The vocabulary to be used for correction.
        """
        self.vocabulary = vocabulary
        self.common_errors = {}
        self._load_common_errors(common_errors_file)
        
    def _load_common_errors(self, common_errors_file: str):
        """
        Loads common errors from a file. 
        The file must contain lines in the format "word:misspelling".
        :param common_errors_file: The file containing common errors.
        """
        with open(common_errors_file, 'r') as f:
            for line in f:
                word, misspelling = line.split(':')
                self.common_errors[word] = misspelling
        
    def similar_words(self, word: str) -> list[(str, str)]:
        """
        Generate candidates for a given word based on edit distance.
        :param word: The word to be corrected.
        :return: A list of tuples containing the edit operation and the candidate word.
        """
        candidates = []
        for i in range(len(word)):
            # Deletion
            candidates.append((DELETE, word[:i] + word[i+1:], i))
            # Insertion
            for c in "abcdefghijklmnopqrstuvwxyz":
                candidates.append((INSERT, word[:i] + c + word[i:], i))
            # Substitution
            for c in "abcdefghijklmnopqrstuvwxyz":
                candidates.append((SUBSTITUTE, word[:i] + c + word[i+1:], i))
            # Transposition
            if i < len(word) - 1:
                candidates.append((TRANSPOSE, word[:i] + word[i+1] + word[i] + word[i+2:], i))
        # Filter candidates to only include valid words in the vocabulary
        candidates = [(op, w, i) for op, w, i in candidates if w in self.vocabulary]
        # Remove duplicates
        candidates = list(set(candidates))
        return candidates
    
    def probability(self, misspelled_word: str, correct_word: str, operation:str, index:int) -> float:
        """
        Calculate the probability of a misspelled word given a correct word.
        :param misspelled_word: The misspelled word.
        :param correct_word: The correct word.
        :param operation: The edit operation used to generate the misspelled word.
        :param index: The index of the character in the original word.
        :return: The probability of the misspelled word given the correct word.
        """
        if operation == DELETE:
            return self._probability_delete(misspelled_word, correct_word, index)
        elif operation == INSERT:
            return self._probability_insert(misspelled_word, correct_word, index)
        elif operation == SUBSTITUTE:
            return self._probaility_substitute(misspelled_word, correct_word, index)
        elif operation == TRANSPOSE:
            return self._probability_transpose(misspelled_word, correct_word, index)
        
    def _probability_delete(self, misspelled_word: str, correct_word: str, i:int) -> float:
        """
        Calculate the probability of a misspelled word given a correct word obtained by deletion.
        
        Let:
            (misspelled_word) x := w_1 ... w_(i-1) w_(i+1) ... w_n
            (correct_word)    w := w_1 ... w_(i-1) w_i w_(i+1) ... w_n
        
        the two words are related by the deletion of w_i. (See method similar_words)
        
        The probability is:
            del[w_(i-1), w_i] / count(w_(i-1), w_i)
        Where:
            del[x, y] = count(xy typed as x)  where xy is checked in the keys of common errors and x is the corresponding part of the misspelled word
            count(x, y) = count(xy) among all corrected spelled words (keys of common_errors)

        :param misspelled_word: The misspelled word.
        :param correct_word: The correct word.
        :param i: The index of the character in the original word.
        :return: The probability of the misspelled word given the correct word.
        """
        if i >= len(correct_word):
            return 0
        x = correct_word[i-1]   # w_(i-1)
        y = correct_word[i]     # w_i
        xy = x + y              # w_(i-1)w_i
        count_x_y = 0           # count(w_(i-1), w_i)
        count_del_x_y = 0       # count(xy typed as x)
        for word_in_channel, misspell_in_channel in self.common_errors.items():
            if xy in word_in_channel:
                count_x_y += 1
            xy_indexes = ChannelModel.all_indexes_of_substring(word_in_channel, xy)
            for index in xy_indexes:
                if index + 1 < len(misspell_in_channel) and misspell_in_channel[index + 1] != x:
                    count_del_x_y += 1
        
        return count_del_x_y / count_x_y if count_x_y > 0 else 0
    
    def _probability_insert(self, misspelled_word: str, correct_word: str, i:int) -> float:
        """
        Calculate the probability of a misspelled word given a correct word obtained by insertion.
        
        Let:
            (misspelled_word) x := w_1 ... w_(i-1) x_i w_(i+1) ... w_n
            (correct_word)    w := w_1 ... w_(i-1) w_(i+1) ... w_n 
            
        the two words are related by the deletion of w_i. (See method similar_words)
        
        The probability is:
            ins[w_(i-1), x_i] / count(w_(i-1))
        Where:
            ins[x, y] = count(x typed as xy)  where x is checked in the keys of common errors and xy is the corresponding part of the misspelled word
            count(x) = count(x) among all corrected spelled words (keys of common_errors)


        :param misspelled_word: The misspelled word.
        :param correct_word: The correct word.
        :param i: The index of the character in the original word.
        :return: The probability of the misspelled word given the correct word.
        """
        x = correct_word[i-1]      # w_(i-1)
        y = misspelled_word[i]     # x_i
        count_x = 0                # count(w_(i-1))
        count_ins_x_y = 0          # count(x typed as xy)
        for word_in_channel, misspell_in_channel in self.common_errors.items():
            if x in word_in_channel:
                count_x += 1
            x_indexes = ChannelModel.all_indexes_of_substring(word_in_channel, x)
            for index in x_indexes:
                # x is a single character, so we need to check if the next character is y
                if index + 1 < len(misspell_in_channel) and misspell_in_channel[index + 1] == y:
                    count_ins_x_y += 1
        
        return count_ins_x_y / count_x if count_x > 0 else 0
    
    def _probaility_substitute(self, misspelled_word: str, correct_word: str, i:int) -> float:
        """
        Calculate the probability of a misspelled word given a correct word obtained by substitution.
        
        Let:
            (misspelled_word) x := w_1 ... w_(i-1) x_i w_(i+1) ... w_n
            (correct_word)    w := w_1 ... w_(i-1) w_i w_(i+1) ... w_n 
            
        the two words are related by the substitution of w_i with x_i. (See method similar_words)
        
        The probability is:
            sub[w_i, x_i] / count(w_i)
        Where:
            sub[x, y] = count(x typed as y)  where x is checked in the keys of common errors and y is the corresponding part of the misspelled word
            count(x) = count(x) among all corrected spelled words (keys of common_errors)


        :param misspelled_word: The misspelled word.
        :param correct_word: The correct word.
        :param i: The index of the character in the original word.
        :return: The probability of the misspelled word given the correct word.
        """
        x = correct_word[i]        # w_i
        y = misspelled_word[i]     # x_i
        count_x = 0                # count(w_i)
        count_sub_x_y = 0          # count(x typed y)
        for word_in_channel, misspell_in_channel in self.common_errors.items():
            if x in word_in_channel:
                count_x += 1
            x_indexes = ChannelModel.all_indexes_of_substring(word_in_channel, x)
            for index in x_indexes:
                # x is a single character, so we need to check if in the misspelled word the character is y
                if index < len(misspell_in_channel) and misspell_in_channel[index] == y:
                    count_sub_x_y += 1
        
        return count_sub_x_y / count_x if count_x > 0 else 0
    
    def _probability_transpose(self, misspelled_word: str, correct_word: str, i:int) -> float:
        """
        Calculate the probability of a misspelled word given a correct word obtained by transposition.
        
        Let:
            (misspelled_word) x := w_1 ... w_(i+1) w_i ... w_n
            (correct_word)    w := w_1 ... w_i w_(i+1) ... w_n 
            
        the two words are related by the transposition of w_i and w_(i+1). (See method similar_words)
        
        The probability is:
            trans[w_i, x_i] / count(w_i, w_(i+1))
        Where:
            trans[x, y] = count(xy typed as yx)  where xy is checked in the keys of common errors and yx is the corresponding part of the misspelled word
            count(x, y) = count(xy) among all corrected spelled words (keys of common_errors)
            
        :param misspelled_word: The misspelled word.
        :param correct_word: The correct word.
        :param i: The index of the character in the original word.
        :return: The probability of the misspelled word given the correct word.
        """
        x = correct_word[i]         # w_i
        y = correct_word[i + 1]     # w_(i+1)
        xy = x + y                  # w_i w_(i+1)
        yx = y + x                  # w_(i+1) w_i
        count_x_y = 0               # count(w_i, w_(i+1))
        count_trans_x_y = 0         # count(xy typed as yx)
        for word_in_channel, misspell_in_channel in self.common_errors.items():
            if xy in word_in_channel:
                count_x_y += 1
            xy_indexes = ChannelModel.all_indexes_of_substring(word_in_channel, xy)
            for index in xy_indexes:
                # xy is a substring of length 2, so we need to check if in the misspelled word the substring is yx
                if misspell_in_channel[index:index+2] == yx:
                    count_trans_x_y += 1
        
        return count_trans_x_y / count_x_y if count_x_y > 0 else 0

    @staticmethod
    def all_indexes_of_substring(string: str, substring: str) -> list[int]:
        """
        Returns all indexes of substring in string.
        :param string: The string to search in.
        :param substring: The substring to search for.
        :return: A list of indexes where the substring is found.
        """
        return [m.start() for m in re.finditer(re.escape(substring), string)]