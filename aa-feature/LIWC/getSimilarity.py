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


category = ['Filename', 'Segment', 'WC', 'Analytic', 'Clout', 'Authentic',
            'Tone', 'WPS', 'Sixltr', 'Dic', 'affect', 'posemo', 'negemo', 'anx',
            'anger', 'sad', 'social', 'family', 'friend', 'female', 'male',
            'bio', 'body', 'health', 'sexual', 'ingest', 'drives',
            'affiliation', 'achieve', 'power', 'reward', 'risk']

affect_idx = category.index('affect')
posemo_idx = category.index('posemo')
negemo_idx = category.index('negemo')
anx_idx = category.index('anx')
anger_idx = category.index('anger')
sad_idx = category.index('sad')

social_idx = category.index('social')
family_idx = category.index('family')
friend_idx = category.index('friend')
female_idx = category.index('female')
male_idx = category.index('male')

liwc_file = './userTopicsLIWC_Results.txt'
data = open(liwc_file, 'r').readlines()

feature_list = []
userList = []
for i in range(len(data)):
    if i == 0:
        continue
    line = data[i].strip().split('\t')
    affect = float(line[affect_idx])
    posemo = float(line[posemo_idx])
    negemo = float(line[negemo_idx])
    anx = float(line[anx_idx])
    sad = float(line[sad_idx])

    social = float(line[social_idx])
    family = float(line[family_idx])
    friend = float(line[friend_idx])
    female = float(line[female_idx])
    male = float(line[male_idx])

    user = line[0]
    idx = user.index('.txt')
    user = user[:idx]
    userList.append(user)

    feature = [affect, posemo, negemo, anx, sad, social, family, friend, female, male]
    feature_list.append(feature)


cosine_matrix = cosine_similarity(feature_list)
cosine_sims = []
for i in range(cosine_matrix.shape[0]):
    for j in range(cosine_matrix.shape[1]):
        if i < j:
            u1 = userList[i]
            u2 = userList[j]
            val = cosine_matrix[i][j]
            # val = np.power(val, 0.5)
            cosine_sims.append([u1, u2, val])

sim_df = pd.DataFrame(cosine_sims, columns=['u1', 'u2', 'cosinesim'])
sim_df = sim_df[sim_df.cosinesim > 0.995]
sim_df.to_csv('./similarityLIWC.txt', index=False)