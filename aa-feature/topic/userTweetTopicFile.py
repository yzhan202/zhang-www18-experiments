import numpy as np
from os.path import isfile, join
from six.moves import cPickle as pickle

import string
import pandas as pd

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer

from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

import os
import datetime
import time


pickle_file = './userTweetTopic.pickle'
with open(pickle_file, 'rb') as h:
    save = pickle.load(h)
    keys = save['keys']
    documents = save['documents']

bestTopic_file = '/home/yue/Public/C_program/cl2_project/SeededLDA/data/aaUserTweetData/SeededLDA_bestTopic.txt'
data = open(bestTopic_file, 'r').readlines()

output = './userTweetTopic.txt'
out = open(output, 'w+')

idx = 0
for key in keys:
    user =  key[0]
    seq = key[1]
    topic = int(data[idx].strip())
    text = documents[idx]
    out.write('%s,%d,%d\n' % (user, seq, topic))
    idx += 1
out.close()

