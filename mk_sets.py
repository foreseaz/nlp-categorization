import json
import os
import re
import shutil

topic = {}

if os.path.exists("tran_set"):
	shutil.rmtree('tran_set')
os.mkdir("tran_set")

if os.path.exists("test_set"):
	shutil.rmtree('test_set')
os.mkdir("test_set")


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
		os.mkdir("tran_set/" + course['topic_name'][0])
		os.mkdir("test_set/" + course['topic_name'][0])
		topic_status = 0
	
	if topic_status == 0:
		outfile = open("tran_set/" + course['topic_name'][0] + "/" + re.sub("[\\/:*?\"<>\|\n]", " ", course['title']) + ".json", "wb")
		outline = json.dumps(course)
		outfile.write(outline)
		outfile.close()
		topic[course['topic_name'][0]] = (topic[course['topic_name'][0]] + 1) % 2
	elif topic_status == 1:
		outfile = open("test_set/" + course['topic_name'][0] + "/" + re.sub("[\\/:*?\"<>\|\n]", " ", course['title']) + ".json", "wb")
		outline = json.dumps(course)
		outfile.write(outline)
		outfile.close()
		topic[course['topic_name'][0]] = (topic[course['topic_name'][0]] + 1) % 2
		
	line = file.readline()

file.close()