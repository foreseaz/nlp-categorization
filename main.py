"""
======================================================
Classification of Scrawled Courses into Topics
======================================================

This is the source for a task on classify scrawled courses into pre-defined su-
bjects and topics by using a bag-of-words approach.

1. classify the languages

2. map courses to our topics

3. generate datasets

4. train and classify
"""

def retrain_classifer(language,json_path=""):
    # TODO: retrain the classifier, if json is not empty, inject it into dataset
    return ""

def classify_course(language,json_path,output_path):
    # TODO: get a json file containing courses
    return ""


OUTPUT_PATH = 'output/'
print(__doc__)

SUBJECT_ARR = ["Arts and Humanities",
               "Mathematics",
               "Biology and Life Sciences",
               "Physical Science",
               "Social Science",
               "Business",
               "Engineering",
               "Computer Science",
               "Data Science",
               "Education and Teaching",
               "Personal Development",
               "Language Learning"]

TOPICS_ARR = [
               ["History", "Anthropology", "Music and Visual Arts", "Philosophy and Ethics", "Design and Creativity", "Literature", "Religion and Culture", "Film and Theatre", "Digital Media and Video Games"],
               ["Statistics and Probability", "Foundations of Mathematics", "Calculus and Mathematical Analysis", "Algebra and Geometry"],
               ["Animals and Veterinary Science", "Bioinformatics", "Biology", "Medicine and Healthcare", "Nutrition", "Clinical Science"],
               ["Environmental Science and Sustainability", "Physics and Astronomy", "Research Methods", "Energy and Earth Sciences", "Chemistry"],
               ["Politics", "Governance and Society", "Law", "Psychology"],
               ["Management and Leadership ", "Economics and Finance", "Marketing", "Entrepreneurship", "Business Essentials", "Business Strategy"],
               ["Architecture", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Materials Science and Engineering"],
               ["Software Development", "Mobile and Web Development",  "Algorithms", "Computer Security and Networks", "Design and Product", "Artificial Intelligence"],
               ["Data Analysis", "Machine Learning", "Probability and Statistics"],
               ["K12", "STEM", "Higher Education", "Teacher Development", "Course Development", "Online Education", "Test Prep"],
               ["Communication", "Career Development", "Self Improvement"],
               ["Learning English", "Language and Culture"]
             ]

import json
import os
import sys
import difflib
import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

def calc_mapping(train_topics, target_topics) :
  mapping = {}
  sm = difflib.SequenceMatcher(None)
  # calculate term char similarity
  for traintpc in train_topics:
    ratio = 0
    sm.set_seq1(traintpc)
    for targettpc in target_topics:
      sm.set_seq2(targettpc)
      loop_ratio = sm.ratio()
      if loop_ratio > ratio:
        ratio = loop_ratio
        mapping[traintpc] = targettpc

  # tune mapping
  mapping.update({
    "Sociology": "Governance and Society",
    "Business Analytics and Intelligence": "Business Strategy",
    "Strategic Management": "Business Strategy",
    "Internet of Things": "Software Development",
    "Finance": "Economics and Finance",
    "Theoretical Computer Science": "Algorithms",
    "Web Development": "Mobile and Web Development",
    "Grammar & Writing": "Learning English",
    "Economics": "Economics and Finance",
    "Disease & Disorders": "Medicine and Healthcare",
    "Physics": "Physics and Astronomy",
    "Information Technology": "Computer Security and Networks",
    "Data Science and Big Data": "Data Analysis",
    "Industry Specific": "Business Essentials"
  })

  # print "\nMapping after tuned:"
  # for k,v in mapping.iteritems():
  #   print k + " : " + v
  return mapping

with open(os.path.join(OUTPUT_PATH, "en_classcentral_courses.json")) as json_data:
  data = json.load(json_data)
  json_data.close()

  # remove no topic courses
  courses = [c for (c) in data if c.get("topic_name") != c.get("subject_name")]
  train_topics = list(set(
                      c.get('topic_name')[0].encode('utf-8') for (c) in courses
                    ))
  print "%d topics in %d training courses" %(len(train_topics), len(courses))
  # print train_topics

  target_topics = []
  for i in TOPICS_ARR:
    for j in i:
      target_topics.append(j)
  print "%d topics in target set" %len(target_topics)
  # print target_topics

  # train_topics map to target_topics
  mapping = calc_mapping(train_topics, target_topics)
  label_mapping = { k: target_topics.index(v) for k, v in mapping.iteritems() }
  labels = list(set([v for k, v in label_mapping.iteritems()]))

  # add label to training courses
  [c.update({"label": label_mapping[c["topic_name"][0]]}) for (c) in courses]

  train_data = [c["description"] for c in courses[:2000]]
  train_target = [c["label"] for c in courses[:2000]]
  test_data = [c["description"] for c in courses[2001:]]
  test_target = [c["label"] for c in courses[2001:]]

  count_vect = CountVectorizer()
  X_train_counts = count_vect.fit_transform(train_data)
  tf_transformer = TfidfTransformer().fit(X_train_counts)
  X_train_tfidf = tf_transformer.transform(X_train_counts)
  # print X_train_tf.shape

  X_new_counts = count_vect.transform(test_data)
  print X_new_counts.shape
  print len(test_target)

  X_new_tfidf = tf_transformer.transform(X_new_counts)

  # clf = MultinomialNB().fit(X_train_tfidf, train_target)
  clf = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42).fit(X_train_tfidf, train_target)

  predicted = clf.predict(X_new_tfidf)

  accuracy = np.mean(predicted == test_target)
  print "Accuracy: %f" %accuracy

