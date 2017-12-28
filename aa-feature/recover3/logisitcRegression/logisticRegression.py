import numpy as np
import os
from os.path import isfile, join
from six.moves import cPickle as pickle
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import TweetTokenizer
from stop_words import get_stop_words
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string


sober_phrases = ['#recovery', 'sober', 'sobriety', 'recovery', '#sobriety']

alcoholic_phrases = ['drunk', 'beer', 'bar', 'wine', 'alcohol', 'wasted', 'hungover',
                     'hangover', 'turnt', 'vodka', 'liquor', 'whiskey', 'tequila',
                     'alcoholic', 'champagne']

def partition_dataset(feature_set, label_set, fold_num, step):
    step = step % fold_num
    train_length = len(label_set)
    batch_size = np.ceil(train_length / (fold_num * 1.0))
    # print train_length, fold_num, batch_size
    idx_start = int((step* batch_size))
    idx_end = int(np.min([((step+1)* batch_size), train_length]))

    # print(idx_start, idx_end)
    test_feature = feature_set[idx_start:idx_end, :]
    test_target = label_set[idx_start:idx_end]

    train_idx = list(set(range(train_length)) - set(range(idx_start, idx_end)))
    train_feature = feature_set[train_idx, :]
    train_target = label_set[train_idx]

    return train_feature, train_target, test_feature, test_target


def classify_tweets(doc_topic, target):

    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, precision_score, recall_score
    from sklearn.metrics import roc_auc_score
    from sklearn import metrics


    num_folds = 5
    prediction_probabilities = np.array([])
    metrics = np.zeros([5,6])
    for i in range(num_folds):
        train_feature, train_target, test_feature, test_target = partition_dataset(doc_topic, target, num_folds, i)

        logreg = LogisticRegression(penalty='l1')
        logreg.fit(train_feature, train_target)

        # print(train_feature.shape, test_feature.shape)
        # print(train_target.shape, test_target.shape)

        y_pred = logreg.predict(test_feature)
        y_proba = np.array(logreg.predict_proba(test_feature))

        print('%d' % i)
        # print(test_target.shape)
        accuracy = accuracy_score(test_target, y_pred)
        precision = precision_score(test_target, y_pred)
        recall = recall_score(test_target, y_pred)
        auc = roc_auc_score(test_target, y_pred)

        from sklearn.metrics import precision_recall_curve
        from sklearn.metrics import average_precision_score

        # AUPRC = average_precision_score(test_target, y_pred, average="micro")

        # average_precision = [0,0]
        # for negtive class
        neg_target = [int(x) for x in (test_target == 0)]
        auprc_negative = average_precision_score(neg_target, y_proba[:,0])
        # for positive class
        post_target = [int(x) for x in (test_target == 1)]
        auprc_positive = average_precision_score(post_target, y_proba[:, 1])

        print("Accuracy: " + str(accuracy))
        print("Precision: " + str(precision))
        print("Recall: " + str(recall))

        print("auprc negative: "+ str(auprc_negative))
        print("auprc positive: " + str(auprc_positive))
        print("AUC: " + str(auc))
        print('\n')
        prediction_probabilities = np.concatenate((prediction_probabilities, y_proba[:,1]), axis=0)

        metrics[i,:] = np.array([accuracy, precision, recall, auc,
                           auprc_negative, auprc_positive])

    return prediction_probabilities, metrics

def main():
    # Term Frequency
    pickle_file = '../features/clearAfterUserTweets.pickle'
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

        clean_tweets = "".join(
            [" " + i if not i.startswith("'") and i not in string.punctuation else i for i in stemmed_tokens]).strip()
        documents.append(clean_tweets)

    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation

    stopwords_set = set(stopwords.words('english')) | set(['sober', 'sobriety', 'drunk'])

    no_features = 2000
    # tf_vectorizer = CountVectorizer(stop_words=stopwords_set, ngram_range=(1, 1), encoding='utf-8', lowercase=True)
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
    tf = tf_vectorizer.fit_transform(documents)
    tf_feature_names = tf_vectorizer.get_feature_names()
    tf_dense = tf.toarray()

    # Uses Sober/Alcohol Word
    alcohol_file = '../features/userUsesAlcoholWord.txt'
    sober_file = '../features/userUsesSoberWord.txt'
    alcohol_data = open(alcohol_file, 'r').readlines()
    alcohol_dict = {}
    for line in alcohol_data:
        record = line.strip().split(',')
        user = record[0]
        word = record[1]
        if user in alcohol_dict:
            alcohol_dict[user].append(word)
        else:
            alcohol_dict[user] = [word]

    sober_data = open(sober_file, 'r').readlines()
    sober_dict = {}
    for line in sober_data:
        record = line.strip().split(',')
        user = record[0]
        word = record[1]
        if user in sober_dict:
            sober_dict[user].append(word)
        else:
            sober_dict[user] = [word]
    useSober_feature = []
    useAlcohol_feature = []
    for user in userList:
        sober_feature = [0] * len(sober_phrases)
        alcohol_feature = [0] * len(alcoholic_phrases)

        if user in sober_dict:
            sober_words = sober_dict[user]
            for w in sober_words:
                idx = sober_phrases.index(w)
                sober_feature[idx] = 1

        if user in alcohol_dict:
            alcohol_words = alcohol_dict[user]
            for w in alcohol_words:
                idx = alcoholic_phrases.index(w)
                alcohol_feature[idx] = 1

        useSober_feature.append(sober_feature)
        useAlcohol_feature.append(alcohol_feature)

    useSober_feature = np.array(useSober_feature)
    useAlcohol_feature = np.array(useAlcohol_feature)

    # Freqency
    soberFreq_file = '../features/userFrequencySoberWord.txt'
    alcoholFreq_file = '../features/userFrequencyAlcoholWord.txt'
    soberFreq_dict = {}
    alcFreq_dict = {}
    soberFreq_data = open(soberFreq_file, 'r').readlines()
    for line in soberFreq_data:
        record = line.strip().split(',')
        user = record[0]
        freq = float(record[1])
        soberFreq_dict[user] = freq
    alcFreq_data = open(alcoholFreq_file, 'r').readlines()
    for line in alcFreq_data:
        record = line.strip().split(',')
        user = record[0]
        freq = float(record[1])
        alcFreq_dict[user] = freq
    freq_feature = []
    for user in userList:
        freq = [0,0]
        if user in alcFreq_dict:
            freq[0] = alcFreq_dict[user]
        if user in soberFreq_dict:
            freq[1] = soberFreq_dict[user]
        freq_feature.append(freq)

    freq_feature = np.array(freq_feature)

    # Topic Distribution
    topicDist_file = '/home/yue/Public/C_program/cl2_project/SeededLDA/data/aaUserData/SeededLDA_docTopicDist.txt'
    topicDist_data = open(topicDist_file, 'r').readlines()
    topicDist_feature = []
    topic_dict = {}
    for line in topicDist_data:
        record = line.strip().split(',')
        dist = [0,0]
        dist[0] = float(record[0])
        dist[1] = float(record[1])
        topicDist_feature.append(dist)
    topicDist_feature = np.array(topicDist_feature)

    # Social
    social_file = '../../LIWC/social.txt'
    social_dict = {}
    data = open(social_file, 'r').readlines()
    for line in data:
        record = line.strip().split(',')
        user = record[0]
        value = float(record[1])
        social_dict[user] = value

    # Affect
    affct_file = '../../LIWC/affect.txt'
    affect_dict = {}
    data = open(affct_file, 'r').readlines()
    for line in data:
        record = line.strip().split(',')
        user = record[0]
        value = float(record[1])
        affect_dict[user] = value


    social_feature = []
    for user in userList:
        social_value = social_dict[user]
        affect_value = affect_dict[user]
        social_feature.append([social_value, affect_value])
    social_feature = np.array(social_feature)

    # Labels
    recover_file = '/home/yue/Public/Java/testonPSL/data/recover_data/recover4/recovers.txt'
    recover_dict = {}
    data = open(recover_file, 'r').readlines()
    for line in data:
        record = line.strip().split(',')
        user = record[0]
        label = int(record[1])
        recover_dict[user] = label

    target = []
    for user in userList:
        target.append(recover_dict[user])
    target = np.array(target)

    print tf_dense.shape
    print topicDist_feature.shape
    print freq_feature.shape
    print useAlcohol_feature.shape
    print useSober_feature.shape
    print social_feature.shape

    features = np.concatenate((tf_dense, topicDist_feature, freq_feature,
                               useAlcohol_feature, useSober_feature, social_feature), axis=1)
    # features = tf_dense
    # features = np.concatenate((tf_dense, topicDist_feature), axis=1)

    prediction_probabilities, metrics = classify_tweets(features, target)

    accu_hat = np.mean(metrics[:, 0])
    prec_hat = np.mean(metrics[:, 1])
    recall_hat = np.mean(metrics[:, 2])
    auc_hat = np.mean(metrics[:, 3])

    prc_negative_hat = np.mean(metrics[:, 4])
    prc_positive_hat = np.mean(metrics[:, 5])

    print prc_positive_hat, prc_negative_hat, auc_hat


if __name__ == "__main__":
    main()





