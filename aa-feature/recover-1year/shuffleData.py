import numpy as np

import time
import datetime
import sys, glob, os
from os import listdir
from os.path import isfile, join
import dill
from six.moves import cPickle as pickle

import string

# recover_1year_file = '/home/yue/Public/aa-dataset/recovers_1year.txt'
# data = open(recover_1year_file, 'r').readlines()
#
# recover1year_dict = {}
# for line in data:
#     record = line.strip().split(',')
#     user = record[0]
#     truth = int(record[1])
#     recover1year_dict[user] = truth


# print rand_idx

# output = './features/recovers_1year.txt'
# out = open(output, 'w+')
# for (user, truth) in recover1year_dict.items():
#     out.write('%s,%d\n' % (user, truth))
# out.close()

recover_file = './features/recovers_1year.txt'
output  = ''
num = len(data)
rand_idx = np.arange(num)
np.random.shuffle(rand_idx)
for i in range(len(data)):
    idx = rand_idx[i]
    line = data[idx].strip()
    out.write('%s\n' % line)
out.close()



