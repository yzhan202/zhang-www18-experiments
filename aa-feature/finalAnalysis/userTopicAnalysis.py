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

recover_sober = 0
recover_alc = 0
relapse_sober = 0
relapse_alc = 0

topic_file = '/home/yue/Public/Java/testonPSL/data/recover_data/recover4/userTopic.txt'
data = open(topic_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    user = record[0]
    topic = int(record[1])

    truth = label_dict[user]
    if truth == 1:
        if topic == 1:
            recover_sober += 1
        elif topic == 0:
            recover_alc += 1
    else:
        if topic == 1:
            relapse_sober += 1
        elif topic == 0:
            relapse_alc += 1

print recover_sober, relapse_sober
print recover_alc, relapse_alc


