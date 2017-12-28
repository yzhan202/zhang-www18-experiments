import numpy as np
import os
from os.path import isfile, join
from six.moves import cPickle as pickle

userTopic_file = '/home/yue/Public/C_program/cl2_project/SeededLDA/data/aaUserData/SeededLDA_bestTopic.txt'
userTopic_data = open(userTopic_file, 'r').readlines()

pickle_file = './features/metaData.pickle'
with open(pickle_file, 'rb') as h:
    save = pickle.load(h)
    userList = save['userList']
    friend_dict = save['friend_dict']
    timeStamp_dict = save['timeStamp_dict']

output = './features/userTopic.txt'
out = open(output, 'w+')
for i in range(len(userList)):
    user = userList[i]
    topic = int(userTopic_data[i].strip())
    out.write('%s,%d\n' % (user, topic))
out.close()

# tweetTopic_file = '/home/yue/Public/C_program/cl2_project/SeededLDA/data/afterTweetData/SeededLDA_bestTopic.txt'
# tweetTopic_data = open(tweetTopic_file, 'r').readlines()
# pickle_file2 = './features/tweetMetaData.pickle'
# with open(pickle_file2, 'rb') as h:
#     save = pickle.load(h)
#     clean_tweets_dict = save['clean_tweets_dict']
#
# output2 = './features/tweetTopic.txt'
# out2 = open(output2,'w+')
# idx = 0
# for (key, value) in clean_tweets_dict.items():
#     u1 = key[0]
#     u2 = key[1]
#     topic = int(tweetTopic_data[idx].strip())
#     idx += 1
#     out2.write('%s,%s,%d\n' % (u1, u2, topic))
# out2.close()
