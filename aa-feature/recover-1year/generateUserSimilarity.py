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


def remove_non_ascii_characters(string_in):
    stripped = [c for c in string_in if 0 < ord(c) < 127]
    return ''.join(stripped)


def getUserTweets():

    pickle_file = './features/metaData.pickle'
    with open(pickle_file, 'rb') as h:
        save = pickle.load(h)
        userList = save['userList']
        newUserList = save['newUserList']
        timeStamp_dict = save['timeStamp_dict']

    data_dir = '/home/yue/Public/aa-dataset'
    new_data_dir = '/home/yue/Public/Python/twitter_work/extract_tweets/dataset'
    last_data_dir = '/home/yue/Public/Python/twitter_work/newExtractTweets/dataset/userTweets'

    afterTweet_dir1 = join(data_dir, 'after')
    afterTweet_dir2 = join(data_dir, 'test_after')
    afterTweet_dir3 = last_data_dir   #join(new_data_dir, 'after')

    beforeTweet_dir1 = join(data_dir, 'before')
    beforeTweet_dir2 = join(data_dir, 'test_before')
    beforeTweet_dir3 = join(new_data_dir, 'before')

    userTweet_dict = {}
    for user in userList:
        # after data
        if user not in newUserList:
            if os.path.isfile(join(afterTweet_dir1, user)):
                fname = join(afterTweet_dir1, user)
            elif os.path.isfile(join(afterTweet_dir2, user)):
                fname = join(afterTweet_dir2, user)
        else:
            fname = join(afterTweet_dir3, user)

        data = open(fname, 'r').readlines()
        firstAA = data[-1].strip().split('\t')

        if len(firstAA) == 3:
            timeStamp_idx = 1
            tw_idx = 2
            tw_length = 3
        else:
            timeStamp_idx = 2
            tw_idx = 3
            tw_length = 4

        timeStamp = timeStamp_dict[user]
        firstAA = timeStamp[0]
        start = timeStamp[1]
        end = timeStamp[2]

        clean_tweets = []
        for line in data:
            tw = line.strip().split('\t')
            if len(tw) < tw_length:
                continue
            try:
                time_stamp = int(tw[timeStamp_idx])
            except:
                continue
            if (time_stamp > end) or (time_stamp < firstAA):
                continue

            text = remove_non_ascii_characters(tw[tw_idx])
            if ('RT @' in text) or ('rt @' in text):
                    continue
            if (text == 'RT') or (text == 'rt'):
                continue
            clean_tweets.append(text)

        # before data
        if user not in newUserList:
            if os.path.isfile(join(beforeTweet_dir1, user)):
                fname = join(beforeTweet_dir1, user)
            elif os.path.isfile(join(beforeTweet_dir2, user)):
                fname = join(beforeTweet_dir2, user)
        else:
            fname = join(beforeTweet_dir3, user)

        beforedata = open(fname, 'r').readlines()

        for line in beforedata:
            tw = line.strip().split('\t')
            if len(tw) < tw_length:
                continue
            try:
                time_stamp = int(tw[timeStamp_idx])
            except:
                continue
            if (time_stamp > firstAA) or (time_stamp < start):
                continue

            text = remove_non_ascii_characters(tw[tw_idx])
            if ('RT @' in text) or ('rt @' in text):
                continue
            if (text == 'RT') or (text == 'rt'):
                continue
            clean_tweets.append(text)
        concat_tweets = string.whitespace.join(clean_tweets)
        userTweet_dict[user] = concat_tweets

    pickle_file = './features/clearUserTweets.pickle'
    try:
        f = open(pickle_file, 'wb')
        save = {
            'userTweet_dict': userTweet_dict,
            'userList': userList
        }
        pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
        f.close()
    except Exception as e:
        print('Unable to save data to', pickle_file, ':', e)
        raise
    stat_info = os.stat(pickle_file)
    print('Compressed pickle size:', stat_info.st_size)

def get_ngram_matrix(list_concatenated_text, n):
    vectorizer = CountVectorizer(stop_words='english', ngram_range=(1, n), encoding='utf-8', lowercase=True)
    sparse_ngram_matrix = vectorizer.fit_transform(list_concatenated_text)
    # sparse_ngram_matrix = total_count_normalize(sparse_ngram_matrix)
    return sparse_ngram_matrix


def compute_cosine_similarities(list_of_users, list_concatenated_text):
    cosine_sims = []
    sparse_feature_matrix = get_ngram_matrix(list_concatenated_text, 4)
    cosine_matrix = cosine_similarity(sparse_feature_matrix)

    for i in range(cosine_matrix.shape[0]):
        for j in range(cosine_matrix.shape[1]):
            if i < j:
                u1 = list_of_users[i]
                u2 = list_of_users[j]
                val = cosine_matrix[i][j]
                # val = np.power(val, 0.5)
                cosine_sims.append([u1, u2, val])
    return cosine_sims

def main():
    getUserTweets()

    pickle_file = './features/clearUserTweets.pickle'
    with open(pickle_file, 'rb') as h:
        save = pickle.load(h)
        userTweet_dict = save['userTweet_dict']
        userList = save['userList']

    tokenizer = RegexpTokenizer(r'\w+')  # r'[a-zA-Z]+'
    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
    # create English stop words list
    en_stop = get_stop_words('en')
    stop_word = stopwords.words('english')
    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()

    documents = []
    for user in userList:
        clean_tweets = userTweet_dict[user]
        # print clean_tweets
        tokens = tokenizer.tokenize(clean_tweets)
        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if (i not in en_stop) and (i not in stop_word)]
        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

        clean_tweets = []
        for i in stemmed_tokens:
            if ((not i.startswith("'")) and (i not in string.punctuation)):
                clean_tweets.append(i)
        clean_tweets = "".join([" " + i for i in clean_tweets])
        # print clean_tweets
        documents.append(clean_tweets)

    cosine_sims = compute_cosine_similarities(userList, documents)
    sim_df = pd.DataFrame(cosine_sims, columns=['u1', 'u2', 'cosinesim'])
    sim_df = sim_df[sim_df.cosinesim > 0.65]
    sim_df.to_csv('./features/similarity.txt', index=False)

if __name__ == "__main__":
    main()