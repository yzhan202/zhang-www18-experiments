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

        print("auprc positive: "+ str(auprc_negative))
        print("auprc negative: " + str(auprc_positive))
        print("AUC: " + str(auc))
        print('\n')
        prediction_probabilities = np.concatenate((prediction_probabilities, y_proba[:,1]), axis=0)

        metrics[i,:] = np.array([accuracy, precision, recall, auc,
                           auprc_negative, auprc_positive])

    return prediction_probabilities, metrics


def main():
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

        clean_tweets = "".join(
            [" " + i if ((not i.startswith("'")) and (i not in string.punctuation))
             else i for i in stemmed_tokens]).strip()

        # clean_tweets = []
        # for i in stemmed_tokens:
        #     if ((not i.startswith("'")) and (i not in string.punctuation)):
        #         clean_tweets.append(i)
        # clean_tweets = "".join([" " + i for i in clean_tweets])
        documents.append(clean_tweets)

    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation

    stopwords_set = set(stopwords.words('english')) | set(['sober', 'sobriety', 'drunk'])

    no_features = 2000
    # tf_vectorizer = CountVectorizer(stop_words=stopwords_set, ngram_range=(1, 1), encoding='utf-8', lowercase=True)
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
    tf = tf_vectorizer.fit_transform(documents)
    tf_feature_names = tf_vectorizer.get_feature_names()

    label_file = '/home/yue/Public/Java/testonPSL/data/recover_data/recover3/recovers.txt'
    label_data = open(label_file, 'r').readlines()
    label_dict = {}
    for line in label_data:
        record = line.strip().split(',')
        user = record[0]
        value = int(record[1])
        # print user, value
        label_dict[user] = value

    labels = []
    for user in userList:
        value = label_dict[user]
        labels.append(value)

    target = np.array(labels)
    dense_tf = tf.toarray()

    prediction_probabilities, metrics = classify_tweets(dense_tf, target)

    output = './features/localRecovers.txt'
    out = open(output, 'w+')
    idx = 0
    for user in userList:
        predict_value = prediction_probabilities[idx]
        out.write('%s,%f\n' % (user, predict_value))
        idx += 1
    out.close()

if __name__ == "__main__":
    main()
