import numpy as np

import time
import datetime
import sys, glob, os
from os import listdir
from os.path import isfile, join
import dill
from six.moves import cPickle as pickle

import string


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


def remove_non_ascii_characters(string_in):
    stripped = [c for c in string_in if 0 < ord(c) < 127]
    return ''.join(stripped)


pickle_file = '../recover3/features/FriendMetaData.pickle'
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

num = 0
friendTweet_dict = {}
for (key, value) in retweet_dict.items():
    friend = key[0]
    user = key[1]
    seq_nums = value

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

    for seq in seq_nums:
        tw = data[seq].strip().split('\t')
        text = remove_non_ascii_characters(tw[2])
        friendTweet_dict[(friend, seq)] = text
        num += 1

for (key, value) in replies_dict.items():
    friend = key[0]
    user = key[1]
    seq_nums = value

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

    for seq in seq_nums:
        tw = data[seq].strip().split('\t')
        text = remove_non_ascii_characters(tw[2])
        friendTweet_dict[(friend, seq)] = text
        num += 1
print num

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer

from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

tokenizer = RegexpTokenizer(r'\w+')  # r'[a-zA-Z]+'
tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
# create English stop words list
en_stop = get_stop_words('en')
stop_word = stopwords.words('english')
# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

for (key, value) in friendTweet_dict.items():
    clean_tweets = value
    tokens = tknzr.tokenize(clean_tweets)
    stopped_tokens = [i for i in tokens if (i not in en_stop) and (i not in stop_word)]
    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    # clean_tweets = "".join(
    #     [" " + i if ((not i.startswith("'")) and (i not in string.punctuation))
    #      else i for i in stemmed_tokens]).strip()
    clean_tweets = []
    for i in stemmed_tokens:
        if ((not i.startswith("'")) and (i not in string.punctuation) and (i not in ['rt', 'RT'])):
            clean_tweets.append(i)

    if len(clean_tweets) <= 3:
        del friendTweet_dict[key]
        # friendTweet_dict.pop(key, None)
        # print key
    else:
        clean_tweets = "".join([" " + i for i in clean_tweets])
        # print clean_tweets
        friendTweet_dict[key] = clean_tweets

seq_record = []
for (key, value) in friendTweet_dict.items():
    seq_record.append(key)

pickle_file = 'tweetMetaData.pickle'
try:
    f = open(pickle_file, 'wb')
    save = {
        'friendTweet_dict': friendTweet_dict,
        'seq_record': seq_record
    }
    pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
    f.close()
except Exception as e:
    print('Unable to save data to', pickle_file, ':', e)
    raise
stat_info = os.stat(pickle_file)
print('Compressed pickle size:', stat_info.st_size)

documents = []
for key in seq_record:
    value = friendTweet_dict[key]
    documents.append(value)
    print key, value

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
# from nltk.corpus import stopwords

stopwords_set = set(stopwords.words('english')) | set(['sober', 'sobriety', 'drunk'])

no_features = 2000
# tf_vectorizer = CountVectorizer(stop_words=stopwords_set, ngram_range=(1, 1), encoding='utf-8', lowercase=True)
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
tf = tf_vectorizer.fit_transform(documents)
tf_feature_names = tf_vectorizer.get_feature_names()

out_dir = '/home/yue/Public/C_program/cl2_project/SeededLDA/data/aaTweetData'
docIdx_file = join(out_dir, 'docIdx.txt')
wordIdx_file = join(out_dir, 'wordIdx.txt')
srcWords_file = join(out_dir, 'srcWords.txt')
# seededWord_file = join(out_dir, 'seed.uniq.words')

docIdx_out = open(docIdx_file, 'w+')
wordIdx_out = open(wordIdx_file, 'w+')
srcWords_out = open(srcWords_file, 'w+')
# seededWord_out = open(seededWord_file, 'w+')

for i in range(len(tf_feature_names)):
    feature = str(tf_feature_names[i])
    srcWords_out.write('%s\n' % feature)
srcWords_out.close()

tf_dense = tf.toarray()
doc_num = tf_dense.shape[0]
print doc_num
for i in range(doc_num):
    doc_tf = tf_dense[i, :]
    nonzeroIdx = (np.nonzero(doc_tf))[0]
    frequency = doc_tf[nonzeroIdx]
    for j in range(len(nonzeroIdx)):
        idx = nonzeroIdx[j]
        freq = frequency[j]
        for t in range(freq):
            wordIdx_out.write('%d\n' % (idx + 1))
            docIdx_out.write('%d\n' % (i + 1))
wordIdx_out.close()
docIdx_out.close()

