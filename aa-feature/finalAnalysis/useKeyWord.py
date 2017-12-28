import numpy as np

import time
import datetime
import sys, glob, os
from os import listdir
from os.path import isfile, join
import dill
from six.moves import cPickle as pickle

import string

target_file = '/home/yue/Public/Java/testonPSL/data/recover_data/recover4/recovers.txt'

label_dict = {}
data = open(target_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    user = record[0]
    truth = int(record[1])
    label_dict[user] = truth

pickle_file = '../recover3/features/metaData.pickle'
with open(pickle_file, 'rb') as h:
    save = pickle.load(h)
    userList = save['userList']
    friend_dict = save['friend_dict']
    # timeStamp_dict = save['timeStamp_dict']

sober_file = '../recover3/features/friendUsesSoberWord.txt'
alcohol_file = '../recover3/features/friendUsesAlcoholWord.txt'

sober_dict = {}
alcohol_dict = {}

data = open(sober_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    user = record[0]
    if user not in sober_dict:
        sober_dict[user] = 1
    else:
        sober_dict[user] += 1

data = open(alcohol_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    user = record[0]
    if user not in alcohol_dict:
        alcohol_dict[user] = 1
    else:
        alcohol_dict[user] += 1

recoverSober = 0
relapseSober = 0

recoverAlcohol = 0
relapseAlcohol = 0

recoverAlcoholFriend = 0
recoverSoberFriend = 0

relapseAlcoholFriend = 0
relapseSoberFriend = 0

for user in userList:

    try:
        friendList = friend_dict[user]
    except:
        continue

    truth = label_dict[user]

    for friend in friendList:
        if friend in sober_dict:
            count = sober_dict[friend]
            if truth == 0:
                relapseSoberFriend += 1
                relapseSober += count
            else:
                recoverSoberFriend += 1
                recoverSober += count

        if friend in alcohol_dict:
            count = alcohol_dict[friend]
            if truth == 0:
                relapseAlcoholFriend += 1
                relapseAlcohol += count
            else:
                recoverAlcoholFriend += 1
                recoverAlcohol += count


print recoverSober, relapseSober

print recoverAlcohol, relapseAlcohol

print recoverAlcoholFriend, relapseAlcoholFriend

print recoverSoberFriend, relapseSoberFriend










