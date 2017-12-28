import numpy as np
import os
from os.path import isfile, join

attendsAA_file = '/home/yue/Public/Java/testonPSL/data/recover_data/recover/attendsAA.txt'
data = open(attendsAA_file, 'r').readlines()
userList = []
for line in data:
    user = line.strip()
    userList.append(user)

recover1year_file = '/home/yue/Public/aa-dataset/1year.csv'
recover_dict = {}
data = open(recover1year_file, 'r').readlines()
for line in data:
    record = line.strip().split(',')
    user = record[0]
    try:
        truth = int(record[1])
    except:
        truth = -1
    recover_dict[user] = truth

output = './features/recovers_1year.txt'
out = open(output, 'w+')
for user in userList:
    try:
        truth = recover_dict[user]
        out.write('%s,%d\n' % (user, truth))
        if truth == -1:
            print user
    except:
        # print user
        out.write('%s\n' % user)
out.close()


