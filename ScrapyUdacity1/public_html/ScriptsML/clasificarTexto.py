text = open('D:\Nube\Dropbox\TESIS DATA LEARNING\DatosCSV\postMess.txt','rU').read()
#text = open('C:\Users\Maria Leon\Dropbox\TESIS DATA LEARNING\DatosCSV\postMess.txt','rU').read()
import nltk.tokenize
from nltk.corpus import movie_reviews
documents = [(list(movie_reviews.words(fileid)), category)
      for category in movie_reviews.categories()
      for fileid in movie_reviews.fileids(category)]

tokens = nltk.word_tokenize(text)
stopWordsText= open('D:\Nube\Dropbox\TESIS DATA LEARNING\DatosCSV\stopWords.txt','rU').read()
stopWords = nltk.word_tokenize(stopWordsText)
tokens= [w.lower() for w in tokens]
tokens= [w.lower() for w in tokens if w.isalpha()]
tokens= [word for word in tokens if word not in stopWords]
all_words = nltk.FreqDist(w.lower() for w in tokens)
word_features = all_words.keys()[:2000]
def document_features(document):
    document_words = set(document)
    features = {} 
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features
featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)
classifier.show_most_informative_features(20)

import collections

from nltk import metrics

def precision_recall(classifier, testfeats):
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
    for i, (feats, label) in enumerate(testfeats):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)
        precisions = {}
        recalls = {}
        for label in classifier.labels():
            precisions[label] = metrics.precision(refsets[label], testsets[label])
            recalls[label] = metrics.recall(refsets[label], testsets[label])
    return precisions, recalls


nb_precisions, nb_recalls = precision_recall(classifier, featuresets)
nb_precisions['pos']
nb_precisions['neg']
nb_recalls['pos']
nb_recalls['neg']
