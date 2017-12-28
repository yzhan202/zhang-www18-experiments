import os
import numpy as np
from os.path import join, isfile
from six.moves import cPickle as pickle

pickle_file = './features/metaData.pickle'
with open(pickle_file, 'rb') as h:
    save = pickle.load(h)
    retweet_dict = save['retweet_dict']
    replies_dict = save['replies_dict']
    sober_dict = save['sober_dict']
    alc_dict = save['alc_dict']
    userList = save['userList']
    friend_dict = save['friend_dict']
    timeStamp_dict = save['timeStamp_dict']

label_dict = {}
recover_file = '/home/yue/Public/Java/testonPSL/data/recover_data/recover3/recovers.txt'
data = open(recover_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    user = record[0]
    value = int(record[1])
    label_dict[user] = value

output = './features/recovers.txt'
out = open(output, 'w+')
for user in userList:
    out.write('%s,%d\n' % (user, label_dict[user]))
out.close()
