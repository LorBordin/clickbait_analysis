#####


# MODULES
import numpy as np
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize
from nltk.tag import pos_tag
import contractions
import string
from collections import Counter
from nltk.corpus import stopwords
from sklearn.base import BaseEstimator, TransformerMixin
from contractions import contractions_dict


# FUNCTIONS
def remove_contractions(string):
    '''
    Identify and expand the most common contractions.
    returmns a string with the uncontracted sentence
    E.g.: "I've gone wild" --> "I have gone wild"
    '''
    str_words = [contractions.fix(word) for word in string.lower().split()]
    return ' '.join(str_words)

def lemmatise_sentence(sentence):
    '''
    Parse sentence. Lower-case words and remove punctuations.
    Return the list of lemmatised words.
    '''
    sentence = remove_contractions(sentence.lower())
    sentence = sentence.translate(str.maketrans('', '', string.punctuation+'’‘'))
    lemmatiser = WordNetLemmatizer()
    lemmatised_sentence = []
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
        lemmatised_sentence.append(lemmatiser.lemmatize(word_1, pos))
    return lemmatised_sentence
    

def lemmatise_verbs(sentence):
    '''
    Return the list of lemmatised verbs in a sentence.
    '''
    sentence = sentence.lower()
    sentence = sentence.translate(str.maketrans('', '', string.punctuation+'’‘'))
    lemmatiser = WordNetLemmatizer()
    lemmatised_verbs = []
    for word, tag in pos_tag(word_tokenize(sentence.lower())):
        if tag.startswith('VB'):
            word_1 = word
            pos = 'v'
            lemmatised_verbs.append(lemmatiser.lemmatize(word_1, pos))
    return lemmatised_verbs



def make_dict(titles_set, collect_verbs=False, rm_stopwords=False, rm_words=False, to_del=None):
    dictionary = Counter()
    tot_str = ' '
    for title in titles_set:
        tot_str+=title+' '
        if collect_verbs:
            dictionary = Counter(lemmatise_verbs(tot_str))
        else:
            dictionary = Counter(lemmatise_sentence(tot_str))
    # Remove english stopwords
    if rm_stopwords:
        stop_words = stopwords.words('english')
        for word in stop_words:
            del dictionary[word]
    # Remove some words
    if rm_words:
        for word in to_del:
            del dictionary[word]
    return dictionary


def most_common_words(n_words, txt_file, collect_verbs=False, rm_stopwords=False, rm_words=False, to_del=None, words_set=None):
    '''
    Loads the vocabulary and returns the list with the most common n_words from it.
    NOTICE: the exception is not intendend to run.
    '''
    # try to load the dictionary from the .txt file.
    try:
        words_count = []
        file = open(txt_file, 'r')
        for line in range(n_words):
            words_count.append(file.readline().rstrip())
        file.close()
        words_count = np.array(words_count)
        print('Dictionary loaded.')
    # make_dict if the .txt doesn't exists
    except FileNotFoundError:
        print("There's no dictionary. Creating a new one.")
        words_count = make_dict(words_set, collect_verbs, rm_stopwords=rm_stopwords, rm_words=rm_words, to_del=to_del)
        words_count = words_count.most_common(n_words)
        file = open(txt_file, 'w+')
        for key, freq in words_count:
            file.write(str(key)+'\n')
        file.close()
        words_count = most_common_words(n_words, txt_file, collect_verbs, rm_stopwords, rm_words, to_del, words_set)
    return words_count
    
    


def contractions_count(string):
    '''
    Returns the ratio between the number of common contracions and the total number of words in the sentence.
    '''
    words = string.split()
    counter = 0
    for word in words:
        if word in list(contractions_dict.keys()):
            counter += 1
    return counter/len(words)


def vectorize(title, dictionary, n_words, options=[True]*4 ):
    '''
    Generate the features vector.
    Default features: word frequencies
    Option features (in order):
    - check if sentence starts with a cardinal number
    - compute the contractions ratio
    - compute the stop words ratio
    - compute the total number of words
    '''
    freq_vec = np.zeros(n_words+sum(options))
    title_words = make_dict([title], rm_stopwords=False)
    
    # options consist in num_first, n_contractions, stopword_ratio, #_tot_words
    options_arr = np.zeros(len(options))
    stop_words = np.array(stopwords.words('english'))
    
    for index, key in list(enumerate(dictionary[:n_words])):
        freq_vec[index] = title_words[key]
    
    for key in title_words.keys():
        options_arr[3] += title_words[key]
        if key in stop_words:
            options_arr[2] += title_words[key]
   
    if options_arr[3]==0:
        options_arr = np.zeros(4)
    else:
        options_arr[0] = 1 if 'NUM' == list(title_words.keys())[0] else 0
        options_arr[1] = contractions_count(title)
        options_arr[2] = options_arr[2]/options_arr[3]
    
    if sum(options)>1:
        freq_vec[n_words:] = options_arr[options]
    
    return freq_vec


# CLASS DigitalizeTitle
class DigitalizeTitle(BaseEstimator, TransformerMixin):
    
    def __init__(self, clckbt_dict, options=[True]*4):
        self.clckbt_dict = clckbt_dict
        self.options = options
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        clckbt_words_vec = np.zeros((len(X), 200+sum(self.options)))
        
        for index, title in enumerate(X):
            clckbt_words_vec[index] = vectorize(title, self.clckbt_dict, 200, self.options)
            #clckbt_words_vec[index, 200:] = count_words(title)
            
        return clckbt_words_vec
