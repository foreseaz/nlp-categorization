from sklearn import datasets
from sklearn.pipeline import Pipeline
from sklearn import metrics
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV


## load train set
cc_train = datasets.load_files("data/classcentral_dataset_train")
print "courses count:",len(cc_train.data)

# ## use SVM and train
text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                           alpha=1e-3, n_iter=5, random_state=42)),
                     ])
text_clf = text_clf.fit(cc_train.data, cc_train.target)


## use naive-bayes
# text_clf = Pipeline([('vect', CountVectorizer()),
#                      ('tfidf', TfidfTransformer()),
#                      ('clf', MultinomialNB()),
#                     ])
# text_clf = text_clf.fit(cc_train.data, cc_train.target)

## parameter tuning using grid search
# parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
#               'tfidf__use_idf': (True, False),
#               'clf__alpha': (1e-2, 1e-3),
#               }
# gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
# gs_clf = gs_clf.fit(cc_train.data, cc_train.target)
# best_parameters, score, _ = max(gs_clf.grid_scores_, key=lambda x: x[1])
# for param_name in sorted(parameters.keys()):
#     print("%s: %r" % (param_name, best_parameters[param_name]))
# print score

## test with test set
cc_test = datasets.load_files("data/classcentral_dataset_test")
docs_test = cc_test.data
predicted = text_clf.predict(docs_test)
print np.mean(predicted == cc_test.target)
print(metrics.classification_report(cc_test.target, predicted, target_names=cc_test.target_names))
# print "confusion matrix:\n",metrics.confusion_matrix(cc_test.target, predicted)