import json
import os

try:
  os.remove('ch_courses.json')
  os.remove('en_courses.json')
  print "========= Init languages classifier"
except:
  print "========= Init languages classifier"

def export_course(is_ch, courses):
  if is_ch:
    with open('ch_courses.json', 'w') as f:
      f.write(json.dumps(courses))
    print "DONE: Write Chinese courses to ch_courses.json \n      Total course: %d" %len(courses)
  else:
    with open('en_courses.json', 'w') as f:
      f.write(json.dumps(courses))
    print "DONE: Write English courses to en_courses.json \n      Total course: %d" %len(courses)

def is_ch_course(course):
  is_ch = False
  content = course.get("content")

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

with open('./../raw_courses.json') as json_data:
  courses = json.load(json_data).get("response").get("docs")
  json_data.close()

  ch_courses = [c for (c) in courses if is_ch_course(c)]
  en_courses = [c for (c) in courses if not is_ch_course(c)]

  export_course(True, ch_courses)
  export_course(False, en_courses)
