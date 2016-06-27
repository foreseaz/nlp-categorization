import json
import os
import re
import shutil

topic = {}
# subjects = {}

if os.path.exists("./data/tran_set"):
  print "tran_set removed"
  shutil.rmtree("./data/tran_set")

os.mkdir("./data/tran_set")

if os.path.exists("./data/test_set"):
  print "test_set removed"
  shutil.rmtree("./data/test_set")

os.mkdir("./data/test_set")


file = open('classcentral_courses_test.json', 'r')
line = file.readline()
while line:
	course = json.loads(line)
	if not course['topic_name'] or course['subject_name'] == course['topic_name']:
		line = file.readline()
		continue
	
	topic_status = topic.get(course['topic_name'][0])
	if topic_status == None:
		topic[course['topic_name'][0]] = 0
		os.mkdir("./data/tran_set/" + course['topic_name'][0])
		os.mkdir("./data/test_set/" + course['topic_name'][0])
		topic_status = 0
	
	if topic_status == 0:
		outfile = open("./data/tran_set/" + course['topic_name'][0] + "/" + re.sub("[\\/:*?\"<>\|\n]", " ", course['title']) + ".json", "wb")
		outline = json.dumps(course)
		outfile.write(outline)
		outfile.close()
		topic[course['topic_name'][0]] = (topic[course['topic_name'][0]] + 1) % 2
	elif topic_status == 1:
		outfile = open("./data/test_set/" + course['topic_name'][0] + "/" + re.sub("[\\/:*?\"<>\|\n]", " ", course['title']) + ".json", "wb")
		outline = json.dumps(course)
		outfile.write(outline)
		outfile.close()
		topic[course['topic_name'][0]] = (topic[course['topic_name'][0]] + 1) % 2
		
	line = file.readline()

file.close()
