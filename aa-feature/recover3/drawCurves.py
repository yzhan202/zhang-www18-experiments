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
    pickle_file = './features/metaData.pickle'
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

    recovery_dict = {}
    recover_file = '/home/yue/Public/Java/testonPSL/data/recover_data/recover4/recovers.txt'
    data = open(recover_file, 'r').readlines()
    for line in data:
        record = line.strip().split(',')
        user = record[0]
        truth = int(record[1])
        recovery_dict[user] = truth

    userPattern_dict = {}
    friendPattern_dict = {}
    for (key, value) in alc_dict.items():
        user = key[0]
        seq = key[1]
        words = value

        userTweet_file1 = join(userTweet_dir, user)
        userTweet_file2 = join(testuserTweet_dir, user)
        userTweet_file3 = join(newuserTweet_dir, user)

        if user in newUserList:
            data = open(userTweet_file3, 'r').readlines()
        elif user in userList:
            if isfile(userTweet_file1):
                data = open(userTweet_file1, 'r').readlines()
            else:
                data = open(userTweet_file2, 'r').readlines()
        else:
            continue

        tw = data[seq].strip().split('\t')
        if len(tw) == 3:
            time_idx = 1
        elif len(tw) == 4:
            time_idx = 2
        timeStamp = int(tw[time_idx])

        if user in userList:
            for w in words:
                if user in userPattern_dict:
                    userPattern_dict[user].append((timeStamp, w))
                else:
                    userPattern_dict[user] = [(timeStamp, w)]

    for (key, value) in sober_dict.items():
        user = key[0]
        seq = key[1]
        words = value

        userTweet_file1 = join(userTweet_dir, user)
        userTweet_file2 = join(testuserTweet_dir, user)
        userTweet_file3 = join(newuserTweet_dir, user)

        if user in newUserList:
            data = open(userTweet_file3, 'r').readlines()
        elif user in userList:
            if isfile(userTweet_file1):
                data = open(userTweet_file1, 'r').readlines()
            else:
                data = open(userTweet_file2, 'r').readlines()
        else:
            continue

        tw = data[seq].strip().split('\t')
        if len(tw) == 3:
            time_idx = 1
        elif len(tw) == 4:
            time_idx = 2
        timeStamp = int(tw[time_idx])

        if user in userList:
            for w in words:
                if user in userPattern_dict:
                    userPattern_dict[user].append((timeStamp, w))
                else:
                    userPattern_dict[user] = [(timeStamp, w)]


    groupedFriendPattern_dict = {}
    for user in userList:
        if user in userPattern_dict:
            userPattern_dict[user] = sorted(userPattern_dict[user], key=lambda data: data[0], reverse=False)

        # groupedFriendPattern_dict[user] = []
        # try:
        #     friendList = friend_dict[user]
        #     for friend in friendList:
        #         if friend in friendPattern_dict:
        #             value = friendPattern_dict[friend]
        #             groupedFriendPattern_dict[user] += value
        # except:
        #     continue
        # groupedFriendPattern_dict[user] = sorted(groupedFriendPattern_dict[user], key=lambda data: data[0], reverse=False)
        if user in friend_dict:
            friendList = friend_dict[user]

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

                    if (time_stamp > int(end)) or (time_stamp < firstAA_timeStamp):
                        continue

                    reply_list = []
                    RT_flag = False
                    text = remove_non_ascii_characters(tw[2])
                    phrases = text.lower().split(' ')
                    for w in phrases:
                        if w in sober_phrases:
                            if user not in groupedFriendPattern_dict:
                                groupedFriendPattern_dict[user] = [(time_stamp, w)]
                            else:
                                groupedFriendPattern_dict[user].append((time_stamp, w))
                        elif w in alcoholic_phrases:
                            if user not in groupedFriendPattern_dict:
                                groupedFriendPattern_dict[user] = [(time_stamp, w)]
                            else:
                                groupedFriendPattern_dict[user].append((time_stamp, w))
        # else:
        #     groupedFriendPattern_dict[user] = []

    import matplotlib.pyplot as plt

    # Get current size
    fig_size = plt.rcParams["figure.figsize"]
    print "Current size:", fig_size
    # Set figure width to 12 and height to 9
    fig_size[0] = 15
    fig_size[1] = 9
    plt.rcParams["figure.figsize"] = fig_size

    recover_dir1 = './curve/eps/recovery'
    relapse_dir1 = './curve/eps/relapse'
    recover_dir2 = './curve/pdf/recovery'
    relapse_dir2 = './curve/pdf/relapse'

    for user in userList:
        time_Stamp = timeStamp_dict[user]
        # print time_Stamp
        firstAA = time_Stamp[0]
        end = time_Stamp[2]

        user_x_point = []
        user_y_point = []
        friend_x_point = []
        friend_y_point = []

        try:
            keyWord_tweets = userPattern_dict[user]
        except:
            keyWord_tweets = []


        for i in range(len(keyWord_tweets)):
            tweet = keyWord_tweets[i]
            time_stamp = tweet[0]
            start_date_time = datetime.datetime.fromtimestamp(firstAA)
            date_time = datetime.datetime.fromtimestamp(time_stamp)
            diff = date_time - start_date_time
            user_x_point.append(int(diff.days))

            if int(diff.days) > 90:
                print('%s, [%d, %d, %d]' % (user, firstAA, end, time_stamp))

            phase = tweet[1]
            if phase in sober_phrases:
                user_y_point.append(1)
            else:
                user_y_point.append(0)
        try:
            friend_tweets = groupedFriendPattern_dict[user]
        except:
            friend_tweets = []
        for i in range(len(friend_tweets)):
            tweet = friend_tweets[i]
            time_stamp = tweet[0]
            date_time = datetime.datetime.fromtimestamp(time_stamp)
            diff = date_time - start_date_time
            friend_x_point.append(diff.days)

            phase = tweet[1]
            if phase in sober_phrases:
                friend_y_point.append(1)
            else:
                friend_y_point.append(0)

        user_output = join('./curve_data/user', user)
        friend_output = join('./curve_data/friend', user)
        user_out = open(user_output, 'w+')
        friend_out = open(friend_output, 'w+')

        for i in range(len(user_x_point)):
            x = user_x_point[i]
            y = user_y_point[i]
            user_out.write('%d,%d\n' % (x, y))
        user_out.close()
        for i in range(len(friend_x_point)):
            x = friend_x_point[i]
            y = friend_y_point[i]
            friend_out.write('%d,%d\n' % (x, y))
        friend_out.close()

        figure_list = []
        name_list = []
        if len(user_x_point) != 0:
            user_figure, = plt.plot(user_x_point, user_y_point, 'ro-')
            figure_list.append(user_figure)
            name_list.append('User')

        if len(friend_x_point) != 0:
            friend_figure, = plt.plot(friend_x_point, friend_y_point, 'b^')
            figure_list.append(friend_figure)
            name_list.append('Friends')

        plt.legend(figure_list, name_list)

        axes = plt.gca()
        axes.set_xlim([0, 90])
        axes.set_ylim([-0.5, 1.5])

        for tick in axes.xaxis.get_major_ticks():
            tick.label.set_fontsize(24)
        for tick in axes.yaxis.get_major_ticks():
            tick.label.set_fontsize(24)

        plt.xlabel('Days', fontsize=28)
        plt.ylabel('Alcohol=0, Sober=1', fontsize=28)

        truth_value = recovery_dict[user]
        if truth_value == 1:
            file_name1 = join(recover_dir1, user + '.eps')
            plt.savefig(file_name1, format='eps')

            file_name2 = join(recover_dir2, user + '.pdf')
            plt.savefig(file_name2, format='pdf')
        else:
            file_name1 = join(relapse_dir1, user + '.eps')
            plt.savefig(file_name1, format='eps')

            file_name2 = join(relapse_dir2, user + '.pdf')
            plt.savefig(file_name2, format='pdf')

        plt.close()



if __name__ == "__main__":
    main()



