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


PSLdata_dir = '/home/yue/Public/Java/testonPSL/data/recover_data/recover5'

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


sober_phrases = ['#recovery', 'sober', 'sobriety', 'recovery', '#sobriety']

alcoholic_phrases = ['drunk', 'beer', 'bar', 'wine', 'alcohol', 'wasted', 'hungover',
                     'hangover', 'turnt', 'vodka', 'liquor', 'whiskey', 'tequila',
                     'alcoholic', 'champagne']

def generateMetaData():
    from six.moves import cPickle as pickle
    pickle_file = './features/metaData.pickle'
    with open(pickle_file, 'rb') as h:
        save = pickle.load(h)
        userList = save['userList']
        newUserList = save['newUserList']
        friend_dict = save['friend_dict']
        timeStamp_dict = save['timeStamp_dict']

    alc_dict = {}
    sober_dict = {}
    retweet_dict = {}
    replies_dict = {}
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

                for w in phrases:
                    w = w.lower()
                    if w in sober_phrases:
                        if (friend, seq_num) not in sober_dict:
                            sober_dict[(friend, seq_num)] = [w]
                        else:
                            sober_dict[(friend, seq_num)].append(w)
                    elif w in alcoholic_phrases:
                        if (friend, seq_num) not in alc_dict:
                            alc_dict[(friend, seq_num)] = [w]
                        else:
                            alc_dict[(friend, seq_num)].append(w)

    from six.moves import cPickle as pickle
    import os

    pickle_file = './features/FriendMetaData.pickle'
    try:
        f = open(pickle_file, 'wb')
        save = {
            'retweet_dict': retweet_dict,
            'replies_dict': replies_dict,
            'sober_dict': sober_dict,
            'alc_dict': alc_dict,
            'userList': userList,
            'newUserList': newUserList,
            'friend_dict': friend_dict,
            'timeStamp_dict': timeStamp_dict
        }
        pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
        f.close()
    except Exception as e:
        print('Unable to save data to', pickle_file, ':', e)
        raise
    stat_info = os.stat(pickle_file)
    print('Compressed pickle size:', stat_info.st_size)


def main():
    generateMetaData()

    pickle_file = './features/FriendMetaData.pickle'
    with open(pickle_file, 'rb') as h:
        save = pickle.load(h)
        retweet_dict = save['retweet_dict']
        replies_dict = save['replies_dict']
        sober_dict = save['sober_dict']
        alc_dict = save['alc_dict']
        userList = save['userList']
        friend_dict = save['friend_dict']
        timeStamp_dict = save['timeStamp_dict']

    retweet_output = './features/friendRetweets.txt'
    retweet_out = open(retweet_output, 'w+')
    for (key, value) in retweet_dict.items():
        u1 = key[0]
        u2 = key[1]
        seq_nums = list(set(value))
        for s in seq_nums:
            retweet_out.write('%s,%s,%d\n' % (u1, u2, s))
    retweet_out.close()

    reply_output = './features/friendReplies.txt'
    reply_out = open(reply_output, 'w+')
    for (key, value) in replies_dict.items():
        u1 = key[0]
        u2 = key[1]
        seq_nums = list(set(value))
        for s in seq_nums:
            reply_out.write('%s,%s,%d\n' % (u1, u2, s))

    useAlc_dict = {}
    useSober_dict = {}

    containAlc_output = './features/friendContainsAlcoholWord.txt'
    containAlc_out = open(containAlc_output, 'w+')
    for (key, value) in alc_dict.items():
        user = key[0]
        seq_num = key[1]
        words = list(set(value))
        for word in words:
            containAlc_out.write('%s,%d,%s\n' % (user, seq_num, word))
            if (user, word) not in useAlc_dict:
                useAlc_dict[(user,word)] = 1
    containAlc_out.close()

    useAlc_output = './features/friendUsesAlcoholWord.txt'
    useAlc_out = open(useAlc_output, 'w+')
    for (key, value) in useAlc_dict.items():
        user = key[0]
        word = key[1]
        useAlc_out.write('%s,%s\n' % (user, word))
    useAlc_out.close()

    containSober_output = './features/friendContainsSoberWord.txt'
    containSober_out = open(containSober_output, 'w+')
    for (key, value) in sober_dict.items():
        user = key[0]
        seq_num = key[1]
        words = list(set(value))
        for word in words:
            containSober_out.write('%s,%d,%s\n' % (user, seq_num, word))
            if (user, word) not in useSober_dict:
                useSober_dict[(user, word)] = 1
    containSober_out.close()

    useSober_output = './features/friendUsesSoberWord.txt'
    useSober_out = open(useSober_output, 'w+')
    for (key, value) in useSober_dict.items():
        user = key[0]
        word = key[1]
        useSober_out.write('%s,%s\n' % (user, word))
    useSober_out.close()


if __name__ == "__main__":
    main()












