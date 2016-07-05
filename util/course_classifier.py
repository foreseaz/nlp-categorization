from sklearn import datasets
from sklearn.pipeline import Pipeline
from sklearn import metrics
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV

from sklearn.externals import joblib
import os
import json


def load_clf(trainset, model_path, enforce_train=False,):
    print "trainset size:", len(trainset.data)

    # count_vect = CountVectorizer(ngram_range=(1, 1))
    # X_train_counts = count_vect.fit_transform(cc_train.data)
    # for w in count_vect.vocabulary_.keys():
    #     print w.encode('utf-8')

    if (not os.path.exists(model_path)) or (enforce_train == True):
        ## use SVM and train
        print "start training ...",
        count_vect = CountVectorizer(stop_words='english',ngram_range=(1, 2))
        tfidf_transformer = TfidfTransformer()
        svm_clf = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)

        ## pipeline
        text_clf = Pipeline([('vect', count_vect),
                             ('tfidf', tfidf_transformer),
                             ('clf', svm_clf),
                             ])
        text_clf = text_clf.fit(trainset.data, trainset.target)
        print "save model into file ...",
        joblib.dump(text_clf, model_path)
        print "done."

    text_clf = joblib.load(model_path)
    return text_clf

def parameter_tuning(trainset,clf):
    parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
                  'tfidf__use_idf': (True, False),
                  'clf__alpha': (1e-2, 1e-3),
                  }
    gs_clf = GridSearchCV(clf, parameters, n_jobs=-1)
    gs_clf = gs_clf.fit(trainset.data, trainset.target)
    best_parameters, score, _ = max(gs_clf.grid_scores_, key=lambda x: x[1])
    for param_name in sorted(parameters.keys()):
        print("%s: %r" % (param_name, best_parameters[param_name]))
    print score


if __name__ == '__main__':
    cc_train = datasets.load_files("../data/datasets/en/train", encoding="utf-8")
    keep_clf = load_clf(cc_train,"../models/svm_en.pkl",True)

    cc_test = datasets.load_files("../data/datasets/en/test", encoding="utf-8")
    docs_test = cc_test.data
    predicted = keep_clf.predict(docs_test)
    for doc, topic, origin in zip(docs_test, predicted, cc_test.target):
        output = json.loads(doc)['title']
        print('%s => %s / %s' % (output, cc_train.target_names[topic], cc_train.target_names[origin]))
    print np.mean(predicted == cc_test.target)
    print(metrics.classification_report(cc_test.target, predicted, target_names=cc_test.target_names))
    # print "confusion matrix:\n",metrics.confusion_matrix(cc_test.target, predicted)