import time
import datetime
import sys, glob, os
from os import listdir
from os.path import isfile, join
import dill
from six.moves import cPickle as pickle

import string


pickle_file = '../recover3/features/metaData.pickle'
with open(pickle_file, 'rb') as h:
    save = pickle.load(h)
    userList = save['userList']
    friend_dict = save['friend_dict']
    newUserList = save['newUserList']
    sober_dict = save['sober_dict']
    alc_dict = save['alc_dict']

psl_dir = '/home/yue/Public/Java/testonPSL/data/recover_data/recover4/'

target_file = join(psl_dir, 'recovers.txt')
label_dict = {}
data = open(target_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    user = record[0]
    truth = int(record[1])
    label_dict[user] = truth

sentiment_dict = {}
sentiment_file = join(psl_dir, 'pos_sentiment.txt')
data = open(sentiment_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    friend = record[0]
    value = float(record[2])
    if friend in sentiment_dict:
        sentiment_dict[friend].append(value)
    else:
        sentiment_dict[friend] = [value]

sober_user = []
alc_user = []
for user in userList:
    try:
        friendList = friend_dict[user]
    except:
        continue

    truth = label_dict[user]

    for friend in friendList:
        try:
            values = sentiment_dict[friend]
        except:
            continue

        if truth == 1:
            sober_user += values
        else:
            alc_user += values

import numpy as np

sober_mean = np.mean(sober_user)
alc_mean = np.mean(alc_user)

print sober_mean, alc_mean