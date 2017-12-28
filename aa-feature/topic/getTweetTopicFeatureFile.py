import numpy as np

import time
import datetime
import sys, glob, os
from os import listdir
from os.path import isfile, join
import dill
from six.moves import cPickle as pickle

import string

pickle_file = './tweetMetaData.pickle'
with open(pickle_file, 'rb') as h:
    save = pickle.load(h)
    friendTweet_dict = save['friendTweet_dict']
    seq_record = save['seq_record']

print len(friendTweet_dict)
bestTopic_file = '/home/yue/Public/C_program/cl2_project/SeededLDA/data/aaTweetData/SeededLDA_bestTopic.txt'
data = open(bestTopic_file, 'r').readlines()

output = './friendTweetTopic.txt'
out = open(output, 'w+')

idx = 0
for key in seq_record:
    value = friendTweet_dict[key]
    friend = key[0]
    seq = key[1]
    topic = int(data[idx].strip())
    out.write('%s,%d,%d,%s\n' % (friend, seq, topic,value))
    idx += 1
out.close()

