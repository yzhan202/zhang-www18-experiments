import numpy as np

import time
import datetime
import sys, glob, os
from os import listdir
from os.path import isfile, join
import dill
from six.moves import cPickle as pickle

import string


category = ['Filename', 'Segment', 'WC', 'Analytic', 'Clout', 'Authentic',
            'Tone', 'WPS', 'Sixltr', 'Dic', 'affect', 'posemo', 'negemo', 'anx',
            'anger', 'sad', 'social', 'family', 'friend', 'female', 'male',
            'bio', 'body', 'health', 'sexual', 'ingest', 'drives',
            'affiliation', 'achieve', 'power', 'reward', 'risk']

affect_idx = category.index('affect')
posemo_idx = category.index('posemo')
negemo_idx = category.index('negemo')
anx_idx = category.index('anx')
anger_idx = category.index('anger')
sad_idx = category.index('sad')
social_idx = category.index('social')
family_idx = category.index('family')
friend_idx = category.index('friend')
female_idx = category.index('female')
male_idx = category.index('male')


label_dict = {}
target_file = '/home/yue/Public/Java/testonPSL/data/recover_data/recover4/recovers.txt'
data = open(target_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    user = record[0]
    truth = int(record[1])
    label_dict[user] = truth


recover_pos = []
relapse_pos = []
liwc_file = './userTopicsLIWC_Results.txt'
data = open(liwc_file, 'r').readlines()
for i in range(len(data)):
    if i == 0:
        continue
    record = data[i].strip().split('\t')
    user = record[0]
    idx = user.index('.txt')
    user = user[:idx]

    posemo = float(record[sad_idx])

    truth = label_dict[user]
    if truth == 1:
        recover_pos.append(posemo)
    else:
        relapse_pos.append(posemo)

# recover_arr = np.array(recover_pos)
# relapse_arr = np.array(relapse_pos)

max_value = np.max(recover_pos+relapse_pos)
print max_value

recover_mean = np.mean(recover_pos)
relapse_mean = np.mean(relapse_pos)
print recover_mean / max_value, relapse_mean / max_value


recover_median = np.median(recover_pos)
relapse_median = np.median(relapse_pos)
print recover_median, relapse_median



