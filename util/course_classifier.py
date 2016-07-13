# -*- coding: utf-8 -*-

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


def load_en_clf(trainset, model_path, enforce_train=False,):
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

def load_ch_clf(trainset, model_path, enforce_train=False,):
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

def classify_courses(trainset,clf,input_path,output_path):
    # get topic-subject mapping
    topic_subject = {}
    keep_topics_path = "../data/provider_topics/keep_topics.json"
    keep_topics_file = open(keep_topics_path,'r')
    keep_topics = json.loads(keep_topics_file.read())
    for subject_index in keep_topics.keys():
        for topic_index in keep_topics[subject_index]['topics']:
            subject_name = keep_topics[subject_index]['subject_name']
            topic_name = keep_topics[subject_index]['topics'][topic_index]
            topic_subject[topic_name] = subject_name
    keep_topics_file.close()

    input_file = open(input_path)
    courses = json.loads(input_file.read())
    input_file.close()
    doc_courses = []
    for course in courses:
        doc_course = json.dumps(course,ensure_ascii=False)
        doc_courses.append(doc_course)
    predicted_topics = clf.predict(doc_courses)
    for course, predicted_topic in zip(courses,predicted_topics):
        predicted_topic_name = trainset.target_names[predicted_topic]
        predicted_subject_name = topic_subject[predicted_topic_name]
        course['subject_name'] = [predicted_subject_name]
        course['topic_name'] = [predicted_topic_name]
        # print('%s => %s' % (course['title'],predicted_topic_name))

    output_file = open(output_path,'w')
    output_file.write(json.dumps(courses,ensure_ascii=False,indent=2).encode('utf-8'))
    output_file.close()

def classify_en_courses(provider_list,enforce=True):
    ## use english trainsets and classifier
    print "loading classifier ...",
    en_train = datasets.load_files("../data/datasets/en/train", encoding="utf-8")
    keep_clf = load_en_clf(en_train, "../models/svm_en.pkl",enforce_train=enforce)
    print "done."

    for provider_name in provider_list:
        print "classify", provider_name, "...",
        if provider_name in ['coursera','udemy']:
            classify_courses(en_train, keep_clf,
                             "../output/unmap_courses/en/unmap_"+provider_name+".json",
                             "../output/classified_courses/en/classified_"+provider_name+".json")
        else:
            classify_courses(en_train, keep_clf,
                             "../data/raw_courses/en/"+provider_name+"_courses.json",
                             "../output/classified_courses/en/classified_"+provider_name+".json")
        print "done."

def collect_all_courses(classified_dir):
    if not os.path.isdir(classified_dir):
        print "ERROR: %s is not a directory!" % classified_dir
        exit(1)
    classified_courses = []
    course_urls = set()
    dump_num = 0
    for sub_dir_name in os.listdir(classified_dir):
        sub_dir_path = os.path.join(classified_dir,sub_dir_name)
        if not os.path.isdir(sub_dir_path):
            continue
        else:
            print sub_dir_name
            for file_name in os.listdir(sub_dir_path):
                if file_name.find('classcentral') > -1:
                    continue
                file_path = os.path.join(sub_dir_path,file_name)
                # classified_courses += json.loads(open(file_path).read())
                for clf_course in json.loads(open(file_path).read()):
                    if not clf_course['course_url'].strip() in course_urls:
                        course_urls.add(clf_course['course_url'].strip())
                        classified_courses.append(clf_course)
                    else:
                        dump_num += 1
                print "\t"+file_name
    print "all classified courses count:",len(classified_courses),"dump:",dump_num
    output_file = open(classified_dir+"/all_classified_courses.json","w")
    output_courses = json.dumps(classified_courses, ensure_ascii=False, indent=2)
    output_file.write(output_courses.encode("utf-8"))
    output_file.close()

if __name__ == '__main__':
    provider_list = [
        'canvas',
        # 'classcentral',
        'coursera',
        'edx',
        'ewant',
        'futurelearn',
        'keepedx',
        'keepmoodle',
        'udacity',
        'udemy',
        'xuetang'
    ]
    classify_en_courses(provider_list,False)

    collect_all_courses('../output/classified_courses')

    print "done."

    # cc_test = datasets.load_files("../data/datasets/en/test", encoding="utf-8")
    # docs_test = cc_test.data
    # predicted = keep_clf.predict(docs_test)
    # for doc, topic, origin in zip(docs_test, predicted, cc_test.target):
    #     output = json.loads(doc)['title']
    #     print('%s => %s / %s' % (output, cc_train.target_names[topic], cc_train.target_names[origin]))
    # print np.mean(predicted == cc_test.target)
    # print(metrics.classification_report(cc_test.target, predicted, target_names=cc_test.target_names))
    # print "confusion matrix:\n",metrics.confusion_matrix(cc_test.target, predicted)