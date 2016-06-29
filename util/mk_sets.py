"""
======================================================
Make training set and testing set
======================================================
"""
import json
import os
import re
import sys
import shutil
from optparse import OptionParser

# parse commandline arguments
op = OptionParser()
(options, args) = op.parse_args()
print(__doc__)
if len(args) != 1:
  op.error("wrong number of arguments \n \
            should enter one filename in /data/ path")
filename = args[0]

topic = {}

DATA_PATH = '../data/'

if os.path.exists(DATA_PATH+"tran_set"):
  print "tran_set removed"
  shutil.rmtree(DATA_PATH+"tran_set")

os.mkdir(DATA_PATH+"tran_set")

if os.path.exists(DATA_PATH+"test_set"):
  print "test_set removed"
  shutil.rmtree(DATA_PATH+"test_set")

os.mkdir(DATA_PATH+"test_set")

def extract_data(course):
  d = re.sub("([\n]|\s{2,})", "", course["description"]) +' '\
                                     + course["title"] + ' '\
                                     + course["topic_name"][0]
  return d.encode('utf-8')


# with open(os.path.join(DATA_PATH, filename)) as json_data:
#   courses = json.load(json_data)
#   json_data.close()
#
#   for course in courses:

file = open(os.path.join(DATA_PATH, filename))
line = file.readline()
while(line):
  # udemy
  line = line[:len(line)-2]
  course = json.loads(line)

  if len(course["subject_name"]) < 1:
    line = file.readline()
    continue

  topic_status = topic.get(course['subject_name'][0])
  if topic_status == None:
    topic[course['subject_name'][0]] = 0
    os.mkdir(DATA_PATH+"tran_set/" + course['subject_name'][0])
    os.mkdir(DATA_PATH+"test_set/" + course['subject_name'][0])
    topic_status = 0

  # print course["title"]
  if topic_status == 0:
    outfile = open(DATA_PATH+"test_set/" + course['subject_name'][0] + "/" + re.sub("[\\/:*?\"<>\|\n]", " ", course['title']) + ".json", "wb")
    outline = json.dumps(course, ensure_ascii=False).encode('utf8')
    # outline = extract_data(course)
    outfile.write(outline)
    outfile.close()
    topic[course['subject_name'][0]] = (topic[course['subject_name'][0]] + 1) % 5
  else:
    outfile = open(DATA_PATH+"tran_set/" + course['subject_name'][0] + "/" + re.sub("[\\/:*?\"<>\|\n]", " ", course['title']) + ".json", "wb")
    outline = json.dumps(course, ensure_ascii=False).encode('utf8')
    # outline = extract_data(course)
    outfile.write(outline)
    outfile.close()
    topic[course['subject_name'][0]] = (topic[course['subject_name'][0]] + 1) % 5

  line = file.readline()
file.close()
