import numpy as np
from os.path import isfile, join
from six.moves import cPickle as pickle

import string
import pandas as pd

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer

from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

import os
import datetime
import time

dataset_dir = '/home/yue/Public/aa-dataset'
new_dataset_dir = '/home/yue/Public/Python/twitter_work/extract_tweets/dataset'

userTweet_dir = join(dataset_dir, 'after')
testuserTweet_dir = join(dataset_dir, 'test_after')
newuserTweet_dir = join(new_dataset_dir, 'after')

before_userTweet_dir = join(dataset_dir, 'before')
before_testuserTweet_dir = join(dataset_dir, 'test_before')
before_newuserTweet_dir = join(new_dataset_dir, 'before')


def remove_non_ascii_characters(string_in):
    stripped = [c for c in string_in if 0 < ord(c) < 127]
    return ''.join(stripped)


pickle_file = '../recover3/features/metaData.pickle'
with open(pickle_file, 'rb') as h:
    save = pickle.load(h)
    userList = save['userList']
    newUserList = save['newUserList']
    timeStamp_dict = save['timeStamp_dict']


tokenizer = RegexpTokenizer(r'\w+')  # r'[a-zA-Z]+'
tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
# create English stop words list
en_stop = get_stop_words('en')
stop_word = stopwords.words('english')
# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

userTweet_dict = {}
documents = []
keys = []
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

    # timeStamp_dict[user] = (firstAA_timeStamp, startTimeStamp, endTimeStamp)

    timeStamp = timeStamp_dict[user]
    firstAA_timeStamp = timeStamp[0]
    startTimeStamp = timeStamp[1]
    endTimeStamp = timeStamp[2]

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
    seq = -1
    for line in data:
        seq += 1
        tw = line.strip().split('\t')
        if len(tw) < tweetLen:
            continue
        try:
            time_stamp = int(tw[time_idx])
        except:
            continue

        if (time_stamp > endTimeStamp) or (time_stamp < firstAA_timeStamp):
            continue

        text = remove_non_ascii_characters(tw[tweetLen - 1])

        tokens = tokenizer.tokenize(text)
        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if (i not in en_stop) and (i not in stop_word)]
        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

        clean_tweets = []
        for i in stemmed_tokens:
            if ((not i.startswith("'")) and (i not in string.punctuation) and (i not in ['rt', 'RT'])):
                clean_tweets.append(i)
        clean_tweets = "".join([" " + i for i in clean_tweets])
        # userTweet_dict[(user, seq)] = clean_tweets
        if clean_tweets != '':
            # print clean_tweets
            documents.append(clean_tweets)
            keys.append((user, seq))
    print user


pickle_file = './userTweetTopic.pickle'
try:
    f = open(pickle_file, 'wb')
    save = {
        'documents': documents,
        'keys': keys
    }
    pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
    f.close()
except Exception as e:
    print('Unable to save data to', pickle_file, ':', e)
    raise
stat_info = os.stat(pickle_file)
print('Compressed pickle size:', stat_info.st_size)


from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
# from nltk.corpus import stopwords

# stopwords_set = set(stopwords.words('english')) | set(['sober', 'sobriety', 'drunk'])

no_features = 2000
# tf_vectorizer = CountVectorizer(stop_words=stopwords_set, ngram_range=(1, 1), encoding='utf-8', lowercase=True)
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
tf = tf_vectorizer.fit_transform(documents)
tf_feature_names = tf_vectorizer.get_feature_names()

out_dir = '/home/yue/Public/C_program/cl2_project/SeededLDA/data/aaUserTweetData'
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
    # print nonzeroIdx
    # print tf_feature_names[956]
    # break
    if len(nonzeroIdx0 == 0:
        print (i+1)
    frequency = doc_tf[nonzeroIdx]
    for j in range(len(nonzeroIdx)):
        idx = nonzeroIdx[j]
        freq = frequency[j]
        for t in range(freq):
            wordIdx_out.write('%d\n' % (idx + 1))
            docIdx_out.write('%d\n' % (i + 1))
wordIdx_out.close()
docIdx_out.close()


