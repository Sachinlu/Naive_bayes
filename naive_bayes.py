# -*- coding: utf-8 -*-
"""Naive_bayes(Question _5).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DQPngC-Uzh--IuwZydRJ6MXdwdbfqs6x
"""

# Importing the important libraries
import nltk

# Elemenating the stop word
nltk.download('punkt')
nltk.download('stopwords')

# Commented out IPython magic to ensure Python compatibility.
# Importing tokenizer
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
# %pylab inline

# making stopword stronger by adding punctutaion and more self defined Stopwords
punctuation = list(punctuation)
Stopwords = stopwords.words('english')
Stopwords += punctuation

# Using some own defined stopwords to make data more clean
Stopwords += ['subject:','from:', 'date:', 'newsgroups:', 'message-id:', 'lines:', 'path:', 'organization:', 
            'would', 'writes:', 'references:', 'article', 'sender:', 'nntp-posting-host:', 'people', 
            'university', 'think', 'xref:']

# Defining the train files paths from the dataset 2
HARDWARE_TRAIN_DATA_DIR = '/content/drive/MyDrive/Pattern Rec/dataset2/dataset2/train/comp.sys.ibm.pc.hardware' # give your path
ELECTRONICS_TRAIN_DATA_DIR = '/content/drive/MyDrive/Pattern Rec/dataset2/dataset2/train/sci.electronics' # give your path

# Defining the test files paths from the dataset 2
HARDWARE_TEST_DATA_DIR = '/content/drive/MyDrive/Pattern Rec/dataset2/dataset2/test/comp.sys.ibm.pc.hardware' # give your path
ELECTRONICS_TEST_DATA_DIR = '/content/drive/MyDrive/Pattern Rec/dataset2/dataset2/test/sci.electronics' # give your path

# defining a function which loads the train data
def load_data(dir):
  #loading data
  train_data = {}
  exce_count =  0
  for file in os.listdir(dir):
    try:
      train_data[file] = filter_data(os.path.join(dir, file))
    except Exception as e:
        exce_count += 1 
  print("Data loading successfull")
  print(f"No of exception occured: {exce_count}")
  return train_data

# This section focus on data preprocessing
def filter_data(file):
  with open(file) as fd:
    try:
      data = fd.readlines()
      return eliminate_signature(eliminate_header(data))
    except Exception as e:
      raise encodingexp('Invalid encoding')

# Preprocessing step removing signature
def eliminate_signature(data):
  return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', eliminate_header(data))

# Preprocessing step removing header
def eliminate_header(data):
  s_idx = 0
  for index, value in enumerate(data):
    if value == '\n':
      s_idx = index + 1
      break
  return ''.join(data[s_idx:])

# Loading training data
HARDWARE_TRAIN_DATA = load_data(HARDWARE_TRAIN_DATA_DIR)
ELECTRONICS_TRAIN_DATA = load_data(ELECTRONICS_TRAIN_DATA_DIR)

# Loading testing data
HARDWARE_TEST_DATA = load_data(HARDWARE_TEST_DATA_DIR)
ELECTRONICS_TEST_DATA = load_data(ELECTRONICS_TEST_DATA_DIR)

# Handling encoding Exception
class encodingexp(Exception):
  pass

# Tokenizer class
class tokenizer():
  @staticmethod
  def get_data(data):
    _word = []
    for word in word_tokenize(data):
      if word.lower() not in Stopwords:
        _word.append(word)

    return _word

# Defining model accuracy method
def accuracy(E, H, model):
  _acc_score = 0
  for message in E.values():
     pred = model.predict(message)
     if pred == "Class: Electronics":
       _acc_score += 1

  for message in H.values():
     pred = model.predict(message)
     if pred == "Class: Hardware":
       _acc_score += 1
  accuracy = (_acc_score / (len(E) + len(H))) 
  return accuracy * 100

# designing own Naive bayes classifier
class NB_classifier():

  def __init__(self):
    self._eletronics = 0
    self._hardware = 0
    self._prob_e = None
    self._prob_h = None
    # vocabulary and word frequency 
    self._vocab = {}
    self._word_freq = {}
    # no of class
    self._no_class = 2

  def fit(self, ele_data, hard_data):

    # Updating vocabulary for both classes
    self._add_vocabulary(hard_data)
    self._add_vocabulary(ele_data)
    
    # Updating word frequency
    self._add_word_freq(ele_data, hard_data)

    self._eletronics = len(ele_data.keys()) 
    self._hardware = len(hard_data.keys())

    # estimating priors
    self._prob_e = self._eletronics / (self._eletronics + self._hardware)
    self._prob_h = self._hardware / (self._eletronics + self._hardware)

  # word frequency updating function
  def _add_word_freq(self, ele_data, hard_data):
   for word in self._vocab.keys():
     doc_freq = [1,1]
     for file in ele_data.keys():
       if word in ele_data[file]:
         doc_freq[0] += 1
     for file in hard_data.keys():
       if word in hard_data[file]:
         doc_freq[1] += 1
     self._word_freq[word] = doc_freq
  
  # to make Prediction
  def predict(self, new_data):
    _new_prob_e = self._prob_e 
    _new_prob_h = self._prob_h
    _new_token =  tokenizer.get_data(new_data)

    for token in _new_token:
      if token in self._word_freq:
        _new_prob_e *= self._word_freq[token][0] / (self._no_class + self._eletronics + self._hardware )
        _new_prob_h *= self._word_freq[token][1] / (self._no_class + self._eletronics + self._hardware )

    # Comparing probabilities of two classes and classifying as one class with higher probability 
    if _new_prob_e > _new_prob_h:
      return "Class: Electronics"
    
    elif _new_prob_e < _new_prob_h:
      return "Class: Hardware"

    else:
      return " OOPS! 404 class not found........ "  
  # Updating vocabulary function
  def _add_vocabulary(self, collection):
    for data in collection.keys():
      tokens = tokenizer.get_data(collection[data])
      for token in tokens:
        if token not in self._vocab:
          self._vocab[token] = 1
        else:
          self._vocab[token] += 1

"""**REFERENCE**:- https://github.com/tanishq9/Text-Classification-20-Newsgroups/"""

# Creating object of our model class
clf = NB_classifier()

# Training the model using training data of datset2
clf.fit(ELECTRONICS_TRAIN_DATA, HARDWARE_TRAIN_DATA)

# predicting accuracy on test data of datset2 
print(f"Model accuracy is: {accuracy(ELECTRONICS_TEST_DATA, HARDWARE_TEST_DATA, clf)}")