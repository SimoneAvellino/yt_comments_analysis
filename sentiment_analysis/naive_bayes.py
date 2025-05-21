import sys
import getopt
import os
import math
import collections
import pickle

class Example:
    def __init__(self):
        self.klass = ''
        self.words = []
    
class NaiveBayes:
    def __init__(self):
        self.FILTER_STOP_WORDS = True
        self.stopList = set(self.readFile('./dataset/english.stop'))
        self.vocab = set([])
        self.countspos = collections.defaultdict(int)
        self.countsneutral = collections.defaultdict(int)
        self.countsneg = collections.defaultdict(int)
        self.prior = [0.0, 0.0, 0.0] 
  
    def classify(self, words):
        total = sum(self.prior)
        p_pos_prior = self.prior[0] / total
        p_neutral_prior = self.prior[1] / total
        p_neg_prior = self.prior[2] / total
        
        pos_tokens_count = sum(self.countspos.values())
        neutral_tokens_count = sum(self.countsneutral.values())
        neg_tokens_count = sum(self.countsneg.values())
        
        score_pos = math.log(p_pos_prior)
        score_neutral = math.log(p_neutral_prior)
        score_neg = math.log(p_neg_prior)
        
        for word in words:
            p_pov = (self.countspos[word] + 1)/(pos_tokens_count + len(self.vocab))
            score_pos += math.log(p_pov)
            
            p_neutral = (self.countsneutral[word] + 1)/(neutral_tokens_count + len(self.vocab))
            score_neutral += math.log(p_neutral)
            
            p_neg = (self.countsneg[word] + 1)/(neg_tokens_count + len(self.vocab))
            score_neg += math.log(p_neg)
    
        if score_pos > score_neutral and score_pos > score_neg:
            classification = 'positive'
        elif score_neutral > score_pos and score_neutral > score_neg:
            classification = 'neutral'
        else:
            classification = 'negative'
        return classification, [score_pos, score_neutral, score_neg]

    def addExample(self, klass, words):
        if klass=='positive':
            self.prior[0] += 1
        elif klass=='neutral':
            self.prior[1] += 1
        else:
            self.prior[2] += 1
        
        for word in words:
            if klass=='positive':
                self.countspos[word] += 1
            elif klass=='neutral':
                self.countsneutral[word] += 1
            else:
                self.countsneg[word] += 1
            self.vocab.add(word)
        
    def train(self, train_df):
        for _, row in train_df.iterrows():
            words = row['Comment'].split()
            words = [word.lower() for word in words]
            if self.FILTER_STOP_WORDS:
                words = self.filterStopWords(words)
            self.addExample(row['Sentiment'], words)

    def test(self, test_df):
        labels = []
        for _, row in test_df.iterrows():
            words = row['Comment'].split()
            words = [word.lower() for word in words]
            if self.FILTER_STOP_WORDS:
                words = self.filterStopWords(words)
            label, _ = self.classify(words)
            labels.append(label)
        return labels
  
    def predict(self, text):
        words = text.split()
        words = [word.lower() for word in words]
        if self.FILTER_STOP_WORDS:
            words = self.filterStopWords(words)
        label, _ = self.classify(words)
        return label
  
    def filterStopWords(self, words):
        filtered = []
        for word in words:
            if not word in self.stopList and word.strip() != '':
                filtered.append(word)
        return filtered

    def readFile(self, fileName):
        with open(fileName) as f:
            contents=f.readlines()
        return '\n'.join(contents).split()
    
    def saveModel(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)
            
    @staticmethod
    def loadModel(file_path):
        with open(file_path, 'rb') as f:
            model = pickle.load(f)
        return model