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

social_idx = category.index('social')
affect_idx = category.index('affect')

file = 'userTopicsLIWC_Results.txt'   #'./LIWC2015Results1year.txt'
data = open(file, 'r').readlines()

social_output = './social.txt'
affect_output = './affect.txt'

social_dict = {}
affect_dict = {}
social_max = 0
affect_max = 0

for i in range(len(data)):
    line = data[i]
    if i == 0:
        continue
    record = line.strip().split('\t')
    user = record[0]
    idx = user.index('.txt')
    user = user[:idx]

    social = float(record[social_idx])
    social_dict[user] = social

    affect = float(record[affect_idx])
    affect_dict[user] = affect

    social_max = np.max([social_max, social])
    affect_max = np.max([affect_max, affect])

social_out = open(social_output, 'w+')
for (user, value) in social_dict.items():
    value = value*1.0 / social_max
    social_out.write('%s,%f\n' % (user,value))
social_out.close()

affect_out = open(affect_output, 'w+')
for (user, value) in affect_dict.items():
    value = value*1.0 / affect_max
    affect_out.write('%s,%f\n' % (user, value))
affect_out.close()



