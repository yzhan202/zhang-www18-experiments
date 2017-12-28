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


target_file = '/home/yue/Public/Java/testonPSL/data/recover_data/recover4/recovers.txt'
label_dict = {}
data = open(target_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    user = record[0]
    truth = int(record[1])
    label_dict[user] = truth

recover_sober = 0
recover_alc = 0
relapse_alc = 0
relapse_sober = 0
for (key, words) in sober_dict.items():
    user = key[0]
    if user in label_dict:
        truth = label_dict[user]
        if truth == 1:
            recover_sober += len(words)
        else:
            relapse_sober += len(words)

for (key, words) in alc_dict.items():
    user = key[0]
    if user in label_dict:
        truth = label_dict[user]
        if truth == 1:
            recover_alc += len(words)
        else:
            relapse_alc += len(words)


print recover_sober, relapse_sober
print recover_alc, relapse_alc
