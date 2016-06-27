from sklearn import datasets
from sklearn.pipeline import Pipeline
from sklearn import metrics
import numpy as np
import sys

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV

# load train set
cc_train = datasets.load_files("data/tran_set")
print "courses count:",len(cc_train.data)

# use SVM and train
# sys.exit(1)
text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                           alpha=1e-3, n_iter=5, random_state=42)),
                     ])
text_clf = text_clf.fit(cc_train.data, cc_train.target)

# test with test set
cc_test = datasets.load_files("data/test_set")
docs_test = cc_test.data
predicted = text_clf.predict(docs_test)
print np.mean(predicted == cc_test.target)
print(metrics.classification_report(cc_test.target, predicted, target_names=cc_test.target_names))
# print "confusion matrix:\n",metrics.confusion_matrix(cc_test.target, predicted)
