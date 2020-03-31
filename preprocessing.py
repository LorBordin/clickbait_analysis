#####


# ---- MODULES -------------------------

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.stem.wordnet import WordNetLemmatizer
from pandas import DataFrame, Series, read_csv
from scipy.sparse import coo_matrix, hstack
from contractions import contractions_dict
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords
from collections import Counter
from nltk import word_tokenize
from nltk.tag import pos_tag
import contractions
import numpy as np
import string


_lem = WordNetLemmatizer()
contractions_set = set(contr.lower() for contr in contractions_dict)



# ---- FUNCTIONS -------------------------

def remove_contractions(string):
    '''
    Expand and count the most common contractions.
    Returns the expandend string and the number of contractions
    E.g.: "I've gone wild" --> "I have gone wild"
    '''
    string = string.lower()
    contr_num = sum(1 for contr in contractions_set if contr in string)
    parsed_string = ' '.join(contractions.fix(word) for word in string.split())
    return parsed_string, contr_num


def lemmatise_sentence(sentence):
    '''
    Parse sentence. Implements lower-casing, removes punctuations and lemmatizes.
    Returns a string.
    '''
    # remove contarctions and convert to lower case
    sentence, contr_num = remove_contractions(sentence.lower())
    # remove punctuation
    sentence = sentence.translate(str.maketrans('', '', string.punctuation+'’‘'))
    # lemmatize words
    lemm_str = ""
    for word, tag in pos_tag(word_tokenize(sentence.lower())):
        if tag.startswith('NN'):
            word_1 = word
            pos = 'n'
        elif tag.startswith('VB'):
            word_1 = word
            pos = 'v'
        elif tag.startswith('CD'):
            word_1 = 'NUM'
            pos = 'a'
        else:
            word_1 = word
            pos = 'a'
        lemm_str += ' '+_lem.lemmatize(word_1, pos)
    return lemm_str, contr_num
    
    
def load_vocabulary(length, txt_file, to_del=None):
    ''' Loads pre-saved bag of words'''
    file = open(txt_file, 'r')
    vocab = np.array([file.readline().rstrip().lower() for line in range(length)])
    file.close()
    print('Dictionary loaded.')
    return vocab



# ---- CLASSES -------------------------

class ParseString(BaseEstimator, TransformerMixin):
    def __init__(self):
        self = True
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X_prep, contr_list = [], []
        for string in X:
            lemm_str, contr_num = lemmatise_sentence(string)
            X_prep.append(lemm_str)
            contr_list.append(contr_num)
        return DataFrame({"headline": X_prep, "contr num":contr_list})
    
    
class PreProcess(BaseEstimator, TransformerMixin):
    def __init__(self, vocabulary):
        self.vocabulary = vocabulary
        self.vectorizer = CountVectorizer(vocabulary=self.vocabulary)
        self.stopwords_set = set(stopwords.words('english'))
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        # bag of words
        X_bag = self.vectorizer.transform(X.headline)
        # meta data
        meta_arr = []
        for i in range(len(X)):
            d = Counter(X.headline.iloc[i].split())
            num_flag = 1 if list(d)[0]=='NUM' else 0
            n_of_words = sum(d.values())
            contr_r = X['contr num'].iloc[i]/n_of_words
            stop_r = sum(d[key] for key in set(d.keys())&self.stopwords_set) / n_of_words
            meta_arr.append([num_flag, contr_r, stop_r, n_of_words])
        meta_arr = coo_matrix(meta_arr)
        return hstack([X_bag, meta_arr])

# ---- PIPELINES -------------------------

full_pipeline = Pipeline([
    ("parse text", ParseString()),
    ("gen features", PreProcess(vocabulary=load_vocabulary(200, 'vocabularies/lem_clckbt_words.txt')))
])
