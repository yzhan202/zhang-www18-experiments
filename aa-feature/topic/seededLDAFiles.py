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