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



def generateMetaData():

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
    afterTweet_dir3 = last_data_dir

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

        output = join('./userTopics', user+'.txt')
        out = open(output, 'w+')

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
            out.write('%s\n' % text)
        concat_tweets = string.whitespace.join(clean_tweets)
        # concat_tweets = "".join([" " + i for i in clean_tweets])
        userTweet_dict[user] = concat_tweets
        out.close()
    pickle_file = './features/clearAfterUserTweets.pickle'
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

def main():
    generateMetaData()

    pickle_file = './features/clearAfterUserTweets.pickle'
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

        # clean_tweets = "".join(
        #     [" " + i if not i.startswith("'") and i not in string.punctuation else i for i in stemmed_tokens]).strip()
        # clean_tweets = "".join(
        #     [" " + i if ((not i.startswith("'")) and (i not in string.punctuation))
        #      else i for i in stemmed_tokens]).strip()
        clean_tweets = []
        for i in stemmed_tokens:
            if ((not i.startswith("'")) and (i not in string.punctuation)):
                clean_tweets.append(i)
        clean_tweets = "".join([" " + i for i in clean_tweets])
        # print clean_tweets
        documents.append(clean_tweets)

        print user
    # out.close()

    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    # from nltk.corpus import stopwords

    stopwords_set = set(stopwords.words('english')) | set(['sober', 'sobriety', 'drunk'])

    no_features = 2000
    # tf_vectorizer = CountVectorizer(stop_words=stopwords_set, ngram_range=(1, 1), encoding='utf-8', lowercase=True)
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
    tf = tf_vectorizer.fit_transform(documents)
    tf_feature_names = tf_vectorizer.get_feature_names()

    out_dir = '/home/yue/Public/C_program/cl2_project/SeededLDA/data/aaUserData'
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


if __name__ == "__main__":
    main()
