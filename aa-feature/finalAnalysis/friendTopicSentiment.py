import numpy as np

import time
import datetime
import sys, glob, os
from os import listdir
from os.path import isfile, join
import dill
from six.moves import cPickle as pickle

import string

psl_dir = '/home/yue/Public/Java/testonPSL/data/recover_data/recover4'

friendTweetTopic_file = join(psl_dir, 'friendTweetTopic.txt')
pos_sentiment_file = join(psl_dir, 'pos_sentiment.txt')


topic_dict = {}
sentiment_dict = {}

data = open(friendTweetTopic_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    friend = record[0]
    seq_num = int(record[1])
    topic = int(record[2])

    if (topic == 0) or (topic == 1):
        topic_dict[(friend, seq_num)] = topic

data = open(pos_sentiment_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    friend = record[0]
    seq_num  = int(record[1])
    score = float(record[2])

    sentiment_dict[(friend, seq_num)] = score

output = 'topicSentimentScore.txt'
out = open(output, 'w+')
for (key, topic) in topic_dict.items():
    if key in sentiment_dict:
        score = sentiment_dict[key]
        friend = key[0]
        seq_num = key[1]
        out.write('%s,%d,[%d,%f]\n' % (friend, seq_num, topic, score))
out.close()

