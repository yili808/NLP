import re
import numpy as np
import pandas as pd
import nltk
# nltk.download()  # Download text data sets, including stop words
from nltk.tokenize import RegexpTokenizer
from gensim import corpora, models, similarities
from nltk.corpus import stopwords  # Import the stop word list
# print(stopwords.words("english"))

from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer


# tokenizer = RegexpTokenizer('\s+', gaps=True)
df = pd.read_csv("indeed.csv")
print(df.shape)
# sr_softengine = df.loc[df['job_title'] == "senior software engineer"]
sr_softengine = df.loc[df['job_title'].isin(["senior software engineer"])]
print(sr_softengine.shape)

my_additional_stop_words = ["years","time","required","including","new","looking","http","www","com"]
stop_words = text.ENGLISH_STOP_WORDS.union(my_additional_stop_words)

"""count vectorizer"""
vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0.2, max_df=0.8, stop_words=stop_words)
X = vectorizer.fit_transform(sr_softengine['job_description'])
# print(vectorizer.vocabulary_)
# print(vectorizer.vocabulary_.items())
freqs = [(word, X.getcol(idx).sum()) for word, idx in vectorizer.vocabulary_.items()]
print(sorted(freqs, key=lambda x: -x[1])[:100])



"""tf-idf vectorizer"""
# vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0.2, max_df=0.8, stop_words=stop_words)
# X = vectorizer.fit_transform(sr_softengine['job_description'])
# indices = np.argsort(vectorizer.idf_)[::-1]
# features = vectorizer.get_feature_names()
# top_n = 100
# top_features = [features[i] for i in indices[:top_n]]
# print(top_features)






    # texts = []
    # for line in f:
    #     # print(line)
    #     tokens = tokenizer.tokenize(line)
    #     stopped_tokens = [w for w in tokens if not w in stopwords.words("english")]
    #     # stemmed_tokens = [p_stenner.sten(w) for w in stopped_tokens]
    #     texts.append(stopped_tokens)
    # print(len(texts))


    # tfidf_matrix = tf.fit_transform(f)
    # # print(tfidf_matrix)
    # feature_names = tf.get_feature_names()
    # print(len(feature_names))
    # # print(feature_names[50:70])
    # dense = tfidf_matrix.todense()
    # # print(dense)
    # print(len(dense[10].tolist()[0]))
    #
    # episode = dense[10].tolist()[0]
    # phrase_scores = [pair for pair in zip(range(0, len(episode)), episode) if pair[1] > 0]
    # print(len(phrase_scores))
    # sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)
    # for phrase, score in [(feature_names[word_id], score) for (word_id, score) in sorted_phrase_scores][:20]:
    #     print('{0: <20} {1}'.format(phrase, score))




