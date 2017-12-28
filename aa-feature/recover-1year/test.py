import numpy as np

import time
import datetime
import sys, glob, os
from os import listdir
from os.path import isfile, join
import dill
from six.moves import cPickle as pickle

import string

recover_90day_file = '/home/yue/Public/Java/testonPSL/data/recover_data/recover4/recovers.txt'
recover_1year_file = '/home/yue/Public/Java/testonPSL/data/recover_data/recover5/recovers.txt'
relapse_count = 0
recover_count = 0
recover90day_dict = {}
data = open(recover_90day_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    user = record[0]
    truth = int(record[1])
    recover90day_dict[user] = truth

    if truth == 0:
        relapse_count += 1
    elif truth == 1:
        recover_count += 1
    else:
        print('error')

recover1year_dict = {}


data = open(recover_1year_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    user = record[0]
    truth = int(record[1])
    recover1year_dict[user] = truth

    # if truth == 0:
    #     relapse_count += 1
    # elif truth == 1:
    #     recover_count += 1
    # else:
    #     print('error')

output = './recover2relapseUsers.txt'
out = open(output, 'w')
num = 0
for (user, truth) in recover1year_dict.items():
    old_truth = recover90day_dict[user]
    if old_truth == 1 and (truth == 0):
        out.write("%s\n" % user)
        num += 1

print num

print relapse_count, recover_count


output = './features/attendsAA.txt'
out = open(output, 'w+')
for (user, truth) in recover1year_dict.items():
    out.write('%s\n' % user)
out.close()