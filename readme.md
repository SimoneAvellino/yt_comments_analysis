# YouTube Comments Analysis

**Kaggle Dataset**: [YouTube Comments Dataset](https://www.kaggle.com/datasets/atifaliak/youtube-comments-dataset)

The dataset is made up with two columns:
- Comment: text describing the comment
- Sentiment: the sentiment of the comment (Positive, Neutral, Negative)

**Team Members**:
- Stefan Schobesberger  
- Mostafa Nafie
- Simone Avellino  

---

### Points that should be covered

We will use NLP technique seen in the course:

1. Basic Text Processing
    - Regex
    - Tokenization
    - POS

2. Language Modeling
    - Uniform Language Model
    - Unigram Language Model
    - Stupid Backoff Language Model
    - Laplace Unigram LanguageModel
    - Laplace Bigram Language Model
    - Kneser Ney Language Model

3. Spelling correction
    - Minimum edit distance
    - Noisy channel

4. Text Classification
    - For example: Spam detection
    - For example: Language Identification
    - Naïve Bayes
    - Bag of words

5. Sentiment Analysis
    - Positive or negative review
    - Holder (source) of attitude
    - Target (aspect) of attitude
    - Three stages: 
        - Simplest task: Is the attitude of this text positive or negative?
        - More complex: Rank the attitude of this text from 1 to 5
        - Advanced: Detect the target, source, or complex attitude types
    - Baseline Algorithm
        - Tokenization
        - Feature extraction
        - Classification:

6. Information retrieval
    - Precision, Recall
    - Term-document Incidence Matrix
    - Inverted index
    - Ranked retrieval
    - Jaccard coefficient
    - Term frequency (tf), log tf
    - Document frequency (df), inververse df
    - Vector space model
        - cosine similarity
    - ddd.qqq
    - Evaluating IR System
        - Precision-Recall curve
        - Mean average precision (MAP)

7. POS tagging
8. Parsing Phrase Structure Grammars
    - CYK
        - Normal CKY
        - Extended CKY
        - CYK for PCFGs

--- 

### 🧠 General Aim

The goal of this project is to analyze YouTube comments to uncover insights into user engagement, sentiment, and behavioral patterns. By applying techniques from natural language processing (NLP).

-  (1) Basic Tokenization for the classifier:
    - Regex to clean the input (ex. remove mentions)
    - Tokenization for the point 4 and 5.
- (2, 3) Language modeling and spelling correction:
    - Detect and correct errors in youtube comments
- (4, 5) Sentiment analisys and text classification: build a classifier that choose the sentiment of a new comment.
- (6) Information retrieval: extract new youtube comments from a link to text the classifier

---


### 📌 Work Division

To ensure an efficient and collaborative workflow, the project is divided into the following main areas:

- Simone: points 2 and 3

- Stefan: points 1 and 6

- Mostafa: points 4 and 5