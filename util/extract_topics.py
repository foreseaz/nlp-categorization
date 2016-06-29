# -*- coding: utf-8 -*-

import json
import os
import re
import shutil

def distribute_with_topics(data_path,json_path):
    train_path = data_path + "_train"
    test_path = data_path + "_test"

    subjects = {}
    topics = {}

    if os.path.exists(train_path):
        shutil.rmtree(train_path)
    os.makedirs(train_path)

    if os.path.exists(test_path):
        shutil.rmtree(test_path)
    os.makedirs(test_path)

    print json_path
    json_file = open(json_path)
    # print json_file.read()[:6000]
    # print json_file.read()
    courses = json.loads(json_file.read())

    for course in courses:
        if not course['topic_name'] or course['subject_name'] == course['topic_name']:
            continue

        if not course['title']:
            continue

        ###### temp exchange ######
        topic_name = course['subject_name'][0].replace("&", "and").strip()
        subject_name = course['topic_name'][0].replace("&", "and").strip()

        if subjects.has_key(subject_name):
            subjects[subject_name].append(topic_name)
        else:
            subjects[subject_name] = [topic_name]

        subjects[subject_name] = list(set(subjects[subject_name]))

        topic_status = topics.get(topic_name)
        if topic_status == None:
            topics[topic_name] = 0
            os.mkdir(train_path + "/" + topic_name)
            os.mkdir(test_path + "/" + topic_name)
            topic_status = 0

        if topic_status < 4:
            outfile = open(train_path + "/" + topic_name + "/" + re.sub("[\\/:*?\"<>\|\n]", " ",
                                                                                course['title']).strip() + ".json", "wb")
            outline = json.dumps(course,ensure_ascii=False,indent=4)
            outfile.write(outline.encode("utf-8"))
            outfile.close()
            topics[topic_name] = (topics[topic_name] + 1) % 5
        elif topic_status == 4:
            outfile = open(test_path + "/" + topic_name + "/" + re.sub("[\\/:*?\"<>\|\n]", " ",
                                                                                course['title']).strip() + ".json", "wb")
            outline = json.dumps(course,ensure_ascii=False,indent=4)
            outfile.write(outline.encode("utf-8"))
            outfile.close()
            topics[topic_name] = (topics[topic_name] + 1) % 5
    json_file.close()

    subjects_file = open('../output/udemy_subjects.json','w')
    output_subjects = json.dumps(subjects,ensure_ascii=False,indent=4)
    subjects_file.write(output_subjects.encode("utf-8"))
    subjects_file.close()

if __name__ == '__main__':
    # dir_path = "data/classcentral_topics"
    dir_path = "../data/datasets/udemy_topics"
    # json_path = "data/udemy_courses.json"
    json_path = "../data/raw_courses/udemy_courses.json"

    distribute_with_topics(dir_path,json_path)

    print "done!"