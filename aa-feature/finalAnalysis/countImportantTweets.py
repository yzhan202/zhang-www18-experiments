import numpy as np

import time
import datetime
import sys, glob, os
from os import listdir
from os.path import isfile, join
import dill
from six.moves import cPickle as pickle

import string


PSLdata_dir = '/home/yue/Public/Java/testonPSL/data/recover_data/recover3'

dataset_dir = '/home/yue/Public/aa-dataset'
new_dataset_dir = '/home/yue/Public/Python/twitter_work/extract_tweets/dataset'

userTweet_dir = join(dataset_dir, 'after')
testuserTweet_dir = join(dataset_dir, 'test_after')
newuserTweet_dir = join(new_dataset_dir, 'after')

attendAA_file = join(PSLdata_dir, 'attendsAA.txt')


def remove_non_ascii_characters(string_in):
    stripped = [c for c in string_in if 0 < ord(c) < 127]
    return ''.join(stripped)

# wordSet = ['#anxiety', '#depression', '#sadness', 'anxiety', 'depression', 'sadness']
# wordSet = ['stressed', 'stress', '#stress']
# wordSet = ['love']
wordSet = ['guilt', 'guilty', 'regret', 'regrets', 'ashamed', 'shame']

def main():
    Count = 0
    userList = []
    userData = open(attendAA_file, 'r').readlines()
    for line in userData:
        user = line.strip()
        userList.append(user)

    print len(userList)

    for user in userList:
        userTweet_file1 = join(userTweet_dir, user)
        userTweet_file2 = join(testuserTweet_dir, user)
        userTweet_file3 = join(newuserTweet_dir, user)

        if isfile(userTweet_file1):
            data = open(userTweet_file1, 'r').readlines()
        elif isfile(userTweet_file2):
            data = open(userTweet_file2, 'r').readlines()
        elif isfile(userTweet_file3):
            data = open(userTweet_file3, 'r').readlines()
        else:
            # print('No user %s\n' % user)
            continue

        firstAA = data[-1].strip().split('\t')
        if len(firstAA) == 3:
            tweetLen = 3
            time_idx = 1
        elif len(firstAA) == 4:
            tweetLen = 4
            time_idx = 2
        else:
            continue

        for line in data:
            tw = line.strip().split('\t')
            try:
                text = remove_non_ascii_characters(tw[tweetLen - 1]).lower()
            except:
                continue
            phrases = text.split(' ')
            # if 'rt' == phrases[0]:
            #     continue
            for t in phrases:
                if t in wordSet:
                    print user, text
                    Count += 1
                    break

    print Count

if __name__ == "__main__":
    main()
