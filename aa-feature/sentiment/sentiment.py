import numpy as np

import time
import datetime
import sys, glob, os
from os import listdir
from os.path import isfile, join
import dill
from six.moves import cPickle as pickle

import string

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer

from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

import dill
from nltk.corpus import sentiwordnet as swn
import spacy


tokenizer = RegexpTokenizer(r'\w+')  # r'[a-zA-Z]+'
tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
# create English stop words list
en_stop = get_stop_words('en')
stop_word = stopwords.words('english')
# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()


pickle_file = '../topic/tweetMetaData.pickle'
with open(pickle_file, 'rb') as h:
    save = pickle.load(h)
    friendTweet_dict = save['friendTweet_dict']

pos_sentiment_score = []
neg_sentiment_score = []
for (key, clean_tweet) in friendTweet_dict.items():
    friend = key[0]
    seq = key[1]

    clean_tweet = str(clean_tweet)

    # print clean_tweet

    text = clean_tweet.split(' ')
    if 'RT' in text[0] or 'rt' in text[0]:
        continue

    pos_scores = []
    neg_scores = []
    for word in text:
        tweet_synsets = list(swn.senti_synsets(word))
        for s in tweet_synsets:
            neutral_score = s.obj_score()
            if neutral_score >= 0.3:
                continue
            pos = s.pos_score()
            neg = s.neg_score()
            # score = 1.0 if pos > neg else 0.0
            pos_scores.append(pos)
            neg_scores.append(neg)
    if len(pos_scores) != 0:
        pos_avg = np.average(pos_scores)
        if not (np.isnan(pos_avg)):
            pos_sentiment_score.append((friend, seq, pos_avg, clean_tweet))
    if len(neg_scores) != 0:
        neg_avg = np.average(neg_scores)
        if not (np.isnan(neg_avg)):
            neg_sentiment_score.append((friend, seq, neg_avg, clean_tweet))

output = './pos_sentiment.txt'
out = open(output, 'w+')
for i in range(len(pos_sentiment_score)):
    user = pos_sentiment_score[i][0]
    seq_num = pos_sentiment_score[i][1]
    pos_avg = pos_sentiment_score[i][2]
    text = pos_sentiment_score[i][3]

    out.write('%s,%d,%f,%s\n' % (user, seq_num, pos_avg, text))
out.close()

output = './neg_sentiment.txt'
out = open(output, 'w+')
for i in range(len(neg_sentiment_score)):
    user = neg_sentiment_score[i][0]
    seq_num = neg_sentiment_score[i][1]
    neg_avg = neg_sentiment_score[i][2]

    out.write('%s,%d,%f\n' % (user, seq_num, neg_avg))
out.close()