import numpy as np

import time
import datetime
import sys, glob, os
from os import listdir
from os.path import isfile, join
import dill
from six.moves import cPickle as pickle

import string


def remove_non_ascii_characters(string_in):
    stripped = [c for c in string_in if 0 < ord(c) < 127]
    return ''.join(stripped)


PSLdata_dir = '/home/yue/Public/Java/testonPSL/data/recover_data/recover4'

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

newfriendTweet_dir = join(new_dataset_dir, 'friendTweets')
lastfriendTweet_dir = '/home/yue/Public/Python/twitter_work/newExtractTweets/dataset/mergedFriendTweet'
friendTweet_dir = lastfriendTweet_dir #join(dataset_dir, 'friendjusttweets')
testfriendTweet_dir = lastfriendTweet_dir #join(dataset_dir, 'chiaaFriends/friendtweetsExtracted')

attendAA_file = join(PSLdata_dir, 'attendsAA.txt')
friends_file = join(PSLdata_dir, 'friends.txt')
recover_file = join(PSLdata_dir, 'recovers.txt')

sober_phrases = ['#recovery', 'sober', 'sobriety', 'recovery', '#sobriety']

alcoholic_phrases = ['drunk', 'beer', 'bar', 'wine', 'alcohol', 'wasted', 'hungover',
                     'hangover', 'turnt', 'vodka', 'liquor', 'whiskey', 'tequila',
                     'alcoholic', 'champagne']

def generateMetaData():
    from six.moves import cPickle as pickle
    pickle_file = '../recover3/features/metaData.pickle'
    with open(pickle_file, 'rb') as h:
        save = pickle.load(h)
        userList = save['userList']
        newUserList = save['newUserList']
        friend_dict = save['friend_dict']
        timeStamp_dict = save['timeStamp_dict']

    label_dict = {}
    data = open(recover_file, 'r').readlines()
    for line in data:
        record = line.strip().split(',')
        user = record[0]
        truth = int(record[1])
        label_dict[user] = truth

    alc_dict = {}
    sober_dict = {}
    retweet_dict = {}
    replies_dict = {}

    recoverAlcCount = {}
    relapseAlcCount = {}

    recoverSoberCount = {}
    relapseSoberCount = {}

    for user in userList:

        truth = label_dict[user]
        if truth == 1:
            recoverAlcCount[user] = 0
            recoverSoberCount[user] = 0
        else:
            relapseAlcCount[user] = 0
            relapseSoberCount[user] = 0
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

                if (time_stamp > end) or (time_stamp < firstAA_timeStamp):
                    continue

                reply_list = []
                RT_flag = False
                text = remove_non_ascii_characters(tw[2])
                phrases = text.split(' ')
                if (phrases[0] == 'RT') or (phrases[0] == 'rt'):
                    try:
                        if ('@' in phrases[1]):
                            ii = phrases[1].index('@')
                            reply = phrases[1][(ii + 1):]
                            if (reply[-1] == ':') or (reply[-1] == ','):
                                reply = reply[0:(len(reply) - 1)]

                            if reply == user:
                                RT_flag = True
                                reply_list.append(reply)
                    except:
                        RT_flag = False
                        # print phrases
                else:
                    for t in phrases:
                        if '@' in t:
                            ii = t.index('@')
                            reply = t[(ii + 1):]
                            # print reply
                            if reply != '':
                                if (reply[-1] == ':') or (reply[-1] == ','):
                                    reply = reply[0:(len(reply) - 1)]
                                if reply == user:
                                    reply_list.append(reply)
                interationFLAG = 1
                if RT_flag == True:
                    if (friend, reply) in retweet_dict:
                        retweet_dict[(friend, reply)].append(seq_num)
                    else:
                        retweet_dict[(friend, reply)] = [seq_num]
                elif len(reply_list) > 0:
                    for reply in reply_list:
                        if (friend, reply) in replies_dict:
                            replies_dict[(friend, reply)].append(seq_num)
                        else:
                            replies_dict[(friend, reply)] = [seq_num]
                else:
                    interationFLAG = 0

                if interationFLAG == 1:
                    for w in phrases:
                        w = w.lower()
                        if w in sober_phrases:
                            if truth == 1:
                                recoverSoberCount[user] += 1
                                print('Recover User, Sober Tweet: [%s--%s, %d, %s]' % (user, friend, seq_num, text))
                            else:
                                relapseSoberCount[user] += 1
                                print('Relapse User, Sober Tweet: [%s--%s, %d, %s]' % (user, friend, seq_num, text))
                            # print recoverSoberCount, relapseSoberCount
                        elif w in alcoholic_phrases:
                            if truth == 1:
                                recoverAlcCount[user] += 1
                                print('Recover User, Alc Tweet: [%s--%s, %d, %s]' % (user, friend, seq_num, text))
                            else:
                                relapseAlcCount[user] += 1
                                print('Relapse User, Alc Tweet: [%s--%s, %d, %s]' % (user, friend, seq_num, text))
                            # print recoverAlcCount, relapseAlcCount
    return recoverSoberCount, relapseSoberCount, recoverAlcCount, relapseAlcCount

def main():
    recoverSoberCount, relapseSoberCount, recoverAlcCount, relapseAlcCount = generateMetaData()

    total_recoverSoberCount = 0
    total_relapseSoberCount = 0
    total_recoverAlcCount = 0
    total_relapseAlcCount = 0

    for (user, count) in recoverSoberCount.items():
        total_recoverSoberCount += count

    for (user, count) in relapseSoberCount.items():
        total_relapseSoberCount += count

    for (user, count) in recoverAlcCount.items():
        total_recoverAlcCount += count

    for (user, count) in relapseAlcCount.items():
        total_relapseAlcCount += count

    print total_recoverSoberCount, total_relapseSoberCount
    print total_recoverAlcCount, total_relapseAlcCount

    from six.moves import cPickle as pickle
    import os

    pickle_file = './friendData.pickle'
    try:
        f = open(pickle_file, 'wb')
        save = {
            'recoverSoberCount': recoverSoberCount,
            'relapseSoberCount': relapseSoberCount,
            'recoverAlcCount': recoverAlcCount,
            'relapseAlcCount': relapseAlcCount
        }
        pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
        f.close()
    except Exception as e:
        print('Unable to save data to', pickle_file, ':', e)
        raise
    stat_info = os.stat(pickle_file)
    print('Compressed pickle size:', stat_info.st_size)

if __name__ == "__main__":
    main()












