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

recovery_dir = './recovers'

prefix = join(recovery_dir, 'recovers_')


def get_name(text):
    start = len('RECOVERS(')
    user = text[start:-1]
    return user

sober_user = []
alc_user = []
for i in range(4):
    file = prefix + str(i)

    data = open(file, 'r').readlines()
    for line in data:
        record = line.strip().split('\t')
        user = get_name(record[0])
        predict = float(record[1])

        truth = label_dict[user]
        if truth == 1:
            sober_user.append(predict)
        else:
            alc_user.append(predict)

import numpy as np

sober_mean = np.mean(sober_user)
alc_mean = np.mean(alc_user)

print sober_mean, alc_mean

