import sys
import string
import numpy as np
import json

from sklearn import datasets
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV

from nltk.tokenize import RegexpTokenizer
from nltk.tag import pos_tag

# load train set
cc_train = datasets.load_files("data/tran_set")
print "Training courses count:",len(cc_train.data)

# nltk tokenizer
def tokenize(text):
  lowers = text.lower()
  tokens = RegexpTokenizer(r'\w+').tokenize(lowers)
  tags = pos_tag(tokens)
  return [w for w, p in tags if p=="NN" or p=="NP"]

with open('data/keepcourses_data.json') as json_data:
  raw_course = json.load(json_data)

docs_test = raw_course[1023:1028]
print docs_test
# trainning pipeline
# text_clf = Pipeline([('vect', CountVectorizer(tokenizer=tokenize, stop_words='english')),
text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 2))),
                      ('tfidf', TfidfTransformer(use_idf=True)),
                      ('clf', SGDClassifier(loss='hinge', penalty='l2',
                      alpha=1e-3, n_iter=5, random_state=42)),
                    ])
text_clf = text_clf.fit(cc_train.data, cc_train.target)

# tuning parameters
# parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
#               'tfidf__use_idf': (True, False),
#               'clf__alpha': (1e-2, 1e-5),
#               'clf__n_iter': (2, 8),
#              }
# gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
# gs_clf = gs_clf.fit(cc_train.data, cc_train.target)
# best_parameters, score, _ = max(gs_clf.grid_scores_, key=lambda x: x[1])
# for param_name in sorted(parameters.keys()):
#   print("%s: %r" % (param_name, best_parameters[param_name]))
# print score

# test with test set
cc_test = datasets.load_files("data/test_set")
print "Testing courses count:",len(cc_test.data)
docs_test = cc_test.data
predicted = text_clf.predict(docs_test)
print np.mean(predicted == cc_test.target)
print(metrics.classification_report(cc_test.target, predicted, target_names=cc_test.target_names))

# print "confusion matrix:\n",metrics.confusion_matrix(cc_test.target, predicted)
