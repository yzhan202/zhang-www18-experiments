import numpy as np

import time
import datetime
import sys, glob, os
from os import listdir
from os.path import isfile, join
import dill
from six.moves import cPickle as pickle

import string


topic_file = '../topic/friendTweetTopic.txt'

target_file = '/home/yue/Public/Java/testonPSL/data/recover_data/recover4/recovers.txt'

label_dict = {}
data = open(target_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    user = record[0]
    truth = int(record[1])
    label_dict[user] = truth

friendTopic_dict = {}
data = open(topic_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    friend = record[0]
    seq = int(record[1])
    topic = int(record[2])
    if (topic == 0) or (topic == 1):
        if friend not in friendTopic_dict:
            friendTopic_dict[friend] = [(seq, topic)]
        else:
            friendTopic_dict[friend].append((seq, topic))

pickle_file = '../recover3/features/metaData.pickle'
with open(pickle_file, 'rb') as h:
    save = pickle.load(h)
    userList = save['userList']
    friend_dict = save['friend_dict']
    # timeStamp_dict = save['timeStamp_dict']

recoverAlcTopic = 0
relapseAlcTopic = 0

recoverSoberTopic = 0
relapseSoberTopic = 0

for user in userList:

    truth = label_dict[user]
    try:
        friendList = friend_dict[user]
    except:
        continue

    for friend in friendList:
        if friend in friendTopic_dict:
            topics = friendTopic_dict[friend]
            for t in topics:
                seq = t[0]
                topic = t[1]
                if topic == 0:
                    if truth == 1:
                        recoverAlcTopic += 1
                    else:
                        relapseAlcTopic += 1
                elif topic == 1:
                    if truth == 1:
                        recoverSoberTopic += 1
                    else:
                        relapseSoberTopic += 1

print recoverAlcTopic, relapseAlcTopic
print recoverSoberTopic, relapseSoberTopic



