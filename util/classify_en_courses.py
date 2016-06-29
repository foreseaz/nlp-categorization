"""
======================================================
Classification of English courses
======================================================
"""

import json
import os
import sys
from optparse import OptionParser
from nltk.corpus import words
from nltk.tokenize import RegexpTokenizer

# parse commandline arguments
op = OptionParser()
(options, args) = op.parse_args()
print(__doc__)
if len(args) != 1:
  op.error("wrong number of arguments \n \
            should enter one filename in /data/ path")
filename = args[0]


DATA_PATH = '../data/'

def export_course(is_en, courses):
  if is_en:
    with open(os.path.join(DATA_PATH, 'en_'+filename), 'a') as f:
      f.write(json.dumps(courses))
      f.write('\n')
    print "DONE: Write English courses to en_%s" %filename
    # print "      Total course: %d" %len(courses)
  else:
    with open(os.path.join(DATA_PATH, 'nonen_'+filename), 'a') as f:
      f.write(json.dumps(courses))
      f.write('\n')
    print "DONE: Write Non-En courses to nonen_%s" %filename
    # print "      Total course: %d" %len(courses)

tokenizer = RegexpTokenizer(r'\w+')
def is_en_course(course):
  is_en = False
  print "processing: " + course['title']
  tokens = tokenizer.tokenize(course['title']+course['description'])
  if len(tokens) == 0:
    return is_en

  is_ens = [w in words.words() for w in tokens]
  if is_ens.count(True)/float(len(is_ens)) > 0.5:
    is_en = True
  return is_en

with open(os.path.join(DATA_PATH, filename)) as json_data:
  courses = json.load(json_data)
  json_data.close()
  # Next when only have subjects
  courses = [c for c in courses if c['topic_name'] and not c['subject_name'] == c['topic_name']]
  print len(courses)

  for course in courses:
    export_course(is_en_course(course), course)
