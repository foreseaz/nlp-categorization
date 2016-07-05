"""
======================================================
Classification of Chinses and English
======================================================
"""

import json
import os
import sys
from optparse import OptionParser

OUTPUT_PATH = '../output/'
DATA_PATH = '../data/'

# parse commandline arguments
op = OptionParser()
(options, args) = op.parse_args()
print(__doc__)
if len(args) != 1:
  op.error("wrong number of arguments \n \
            should enter one filename in /data/ path")
filename = args[0]

def export_course(is_ch, courses):
  if is_ch:
    with open(os.path.join(OUTPUT_PATH, 'ch_'+filename), 'w') as f:
      f.write(json.dumps(courses))
    print "DONE: Write Chinese courses to ch_%s" %filename
    print "      Total course: %d" %len(courses)
  else:
    with open(os.path.join(OUTPUT_PATH, 'en_'+filename), 'w') as f:
      f.write(json.dumps(courses))
    print "DONE: Write English courses to en_%s" %filename
    print "      Total course: %d" %len(courses)

def is_ch_course(course):
  is_ch = False
  content = course.get("content") or course.get("description")

  for char in content:
    try:
      # utf-8 chinese between u4e00 and u9fa0
      if char > u'\u4e00' and char < u'\u9fa0':
        is_ch = True
        break
    except Exception as e:
      print e
      continue
  return is_ch

with open(os.path.join(DATA_PATH, filename)) as json_data:
  courses = json.load(json_data)
  json_data.close()

  ch_courses = [c for (c) in courses if is_ch_course(c)]
  en_courses = [c for (c) in courses if not is_ch_course(c)]

  export_course(True, ch_courses)
  export_course(False, en_courses)
