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

###
Tutorial 1
	1. Computing with Language: Texts and Words 
	2. Texts as Lists of Words
	3.Computing with Language: Simple Statistics
	4. Back to Python: Making Decisions and Taking Control (Conditionals, loops)

Tutorial 2
	1. Accessing Text Corpora
	2. Conditional Frequency Distributions

Tutorial 3
	3.1   Accessing Text from the Web and from Disk
	3.2   Strings: Text Processing at the Lowest Level
	3.3   Text Processing with Unicode
	3.6   Normalising Text
	3.9   Formatting: From Lists to Strings

Tutorial 4
	1.1   Gender Identification
	1.2   Choosing The Right Features
	1.3   Document Classification
	3.1 The Test Set
	3.2 Accuracy
	3.3 Precision and Recall
	3.4 Confusion Matrices
	3.4 Cross Validation

Tutorial 5:
	1. Using a Tagger
	2. Tagged Corpora
	4. Automatic Tagging
	5. N-Gram Tagging
	6. Part of Speech Tagging
	7. Exploiting Context

--- 

### 🧠 General Aim

The goal of this project is to analyze YouTube comments to uncover insights into user engagement, sentiment, and behavioral patterns. By applying techniques from natural language processing (NLP).

-  (1) Basic Tokenization for the classifier:
    - Regex to clean the input (ex. remove mentions)
    - Tokenization for the point 4 and 5.
- (2, 3) Language modeling and spelling correction:
    - Detect and correct errors in youtube comments
- (4, 5) Sentiment analisys and text classification: build a classifier that choose the sentiment of a new comment. Use POS tagger, regex and so on to extract the features.
- (6) Information retrieval: extract new youtube comments from a link to text the classifier

---


### 📌 Work Division

To ensure an efficient and collaborative workflow, the project is divided into the following main areas:

- Simone: points 2 and 3

- Stefan: points 1 and 6

- Mostafa: points 4 and 5
