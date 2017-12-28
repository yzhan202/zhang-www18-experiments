import numpy as np

import time
import datetime
import sys, glob, os
from os import listdir
from os.path import isfile, join
import dill
from six.moves import cPickle as pickle

import string

pickle_file = './features/UserMetaData.pickle'
with open(pickle_file, 'rb') as h:
    save = pickle.load(h)
    sober_dict = save['sober_dict']
    alc_dict = save['alc_dict']
    userList = save['userList']
    friend_dict = save['friend_dict']

soberFreq_dict = {}
for (key, value) in sober_dict.items():
    u1 = key[0]
    seq = key[1]
    if u1 not in soberFreq_dict:
        soberFreq_dict[u1] = 1
    else:
        soberFreq_dict[u1] += 1

alcFreq_dict = {}
for (key, value) in alc_dict.items():
    u1 = key[0]
    seq = key[1]
    if u1 not in alcFreq_dict:
        alcFreq_dict[u1] = 1
    else:
        alcFreq_dict[u1] += 1


alc_count = []
for (user, count) in alcFreq_dict.items():
    alc_count.append(count)

sober_count = []
for (user, count) in soberFreq_dict.items():
    sober_count.append(count)

alc_mean = np.mean(alc_count)
alc_max = np.max(alc_count)
alc_median = np.median(alc_count)

sober_mean = np.mean(sober_count)
sober_max = np.max(sober_count)
sober_median = np.median(sober_count)

print alc_mean, sober_mean
print alc_max, sober_max
print alc_median, sober_median

alc_output = './features/userFrequencyAlcoholWord.txt'
sober_output = './features/userFrequencySoberWord.txt'

alc_out = open(alc_output, 'w+')
sober_out = open(sober_output, 'w+')

alc_threshold = 5.0
sober_threshold = 5.0

for (user, count) in alcFreq_dict.items():
    freq_count = count*1.0 / alc_threshold
    if freq_count > 1.0:
        freq_count = 1.0
    alc_out.write('%s,%f\n' % (user, freq_count))
alc_out.close()

for (user, count) in soberFreq_dict.items():
    freq_count = count * 1.0 / sober_threshold
    if freq_count > 1.0:
        freq_count = 1.0
    sober_out.write('%s,%f\n' % (user, freq_count))
sober_out.close()