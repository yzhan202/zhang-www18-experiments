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

before_userTweet_dir = join(dataset_dir, 'before')
before_testuserTweet_dir = join(dataset_dir, 'test_before')
before_newuserTweet_dir = join(new_dataset_dir, 'before')

friendList_dir = join(dataset_dir, 'friendList')
testfriendList_dir = join(dataset_dir, 'chiaaFriends')
newfriendList_dir = join(new_dataset_dir, 'friendList')

lastfriendTweet_dir = '/home/yue/Public/Python/twitter_work/newExtractTweets/dataset/mergedFriendTweet'
friendTweet_dir = lastfriendTweet_dir #join(dataset_dir, 'friendjusttweets')
testfriendTweet_dir = lastfriendTweet_dir #join(dataset_dir, 'chiaaFriends/friendtweetsExtracted')
newfriendTweet_dir = join(new_dataset_dir, 'friendTweets')

attendAA_file = join(PSLdata_dir, 'attendsAA.txt')
friends_file = join(PSLdata_dir, 'friends.txt')


sober_phrases = ['#recovery', 'sober', 'sobriety', 'recovery', '#sobriety']

alcoholic_phrases = ['drunk', 'beer', 'bar', 'wine', 'alcohol', 'wasted', 'hungover',
                     'hangover', 'turnt', 'vodka', 'liquor', 'whiskey', 'tequila',
                     'alcoholic', 'champagne']


def main():
    pickle_file = '../features/metaData.pickle'
    with open(pickle_file, 'rb') as h:
        save = pickle.load(h)
        retweet_dict = save['retweet_dict']
        replies_dict = save['replies_dict']
        sober_dict = save['sober_dict']
        alc_dict = save['alc_dict']
        userList = save['userList']
        newUserList = save['newUserList']
        friend_dict = save['friend_dict']
        timeStamp_dict = save['timeStamp_dict']

    userBefore = 0
    userAfter = 0
    for user in userList:
        userTweet_file1 = join(userTweet_dir, user)
        userTweet_file2 = join(testuserTweet_dir, user)
        userTweet_file3 = join(newuserTweet_dir, user)

        if user in newUserList:
            if isfile(userTweet_file3):
                data = open(userTweet_file3, 'r').readlines()
            else:
                continue
        else:
            if isfile(userTweet_file1):
                data = open(userTweet_file1, 'r').readlines()
            elif isfile(userTweet_file2):
                data = open(userTweet_file2, 'r').readlines()
            else:
                continue

        firstAA = data[-1].strip().split('\t')

        if len(firstAA) == 3:
            tweetLen = 3
            time_idx = 1
        elif len(firstAA) == 4:
            tweetLen = 4
            time_idx = 2
        else:
            # print('error\n')
            continue

        timeStamp = timeStamp_dict[user]
        firstAA_timeStamp = timeStamp[0]
        start_TimeStamp = timeStamp[1]
        end_TimeStamp = timeStamp[2]

        seq_num = -1
        for line in data:
            seq_num += 1
            tw = line.strip().split('\t')
            if len(tw) < tweetLen:
                continue
            try:
                time_stamp = int(tw[time_idx])
            except:
                continue

            # if (time_stamp > endTimeStamp) or (time_stamp < firstAA_timeStamp):
            #     continue

            if (time_stamp >= firstAA_timeStamp) and (time_stamp <= end_TimeStamp):
                userAfter += 1

        # before data
        if user not in newUserList:
            if os.path.isfile(join(before_userTweet_dir, user)):
                fname = join(before_userTweet_dir, user)
            elif os.path.isfile(join(before_testuserTweet_dir, user)):
                fname = join(before_testuserTweet_dir, user)
        else:
            fname = join(before_newuserTweet_dir, user)

        beforedata = open(fname, 'r').readlines()

        seq_num = -1
        for line in beforedata:
            seq_num += 1
            tw = line.strip().split('\t')
            if len(tw) < tweetLen:
                continue
            try:
                time_stamp = int(tw[time_idx])
            except:
                continue

            # if (time_stamp > endTimeStamp) or (time_stamp < firstAA_timeStamp):
            #     continue
            if (time_stamp >= start_TimeStamp) and (time_stamp <= firstAA_timeStamp):
                userBefore += 1

    friendBefore = 0
    friendAfter = 0
    for user in userList:
        try:
            friendList = friend_dict[user]
        except:
            # print('user %s no friends\n' % user)
            continue

        timeStamps = timeStamp_dict[user]
        firstAA_timeStamp = timeStamps[0]
        start = timeStamps[1]
        end = timeStamps[2]

        for friend in friendList:
            friendTweet_file1 = join(friendTweet_dir, friend)
            friendTweet_file2 = join(testfriendTweet_dir, friend)
            friendTweet_file3 = join(newfriendTweet_dir, friend)

            if user in newUserList:
                if isfile(friendTweet_file3):
                    data = open(friendTweet_file3, 'r').readlines()
                else:
                    data = []
            else:
                if isfile(friendTweet_file1):
                    data = open(friendTweet_file1, 'r').readlines()
                elif isfile(friendTweet_file2):
                    data = open(friendTweet_file2, 'r').readlines()
                else:
                    data = []

            seq_num = -1
            for line in data:
                seq_num += 1

                tw = line.strip().split('\t')

                if len(tw) < 3:
                    continue
                try:
                    time_stamp = int(tw[1])
                except:
                    continue

                if (time_stamp < firstAA_timeStamp) and (time_stamp >= start):
                    friendBefore += 1
                elif (time_stamp >= firstAA_timeStamp) and (time_stamp <= end):
                    friendAfter += 1

    print userBefore, userAfter
    print friendBefore, friendAfter

    friend_num = 76183.0
    print userBefore / 302.0, userAfter / 302.0
    print friendBefore / friend_num, friendAfter / friend_num

if __name__ == "__main__":
    main()






