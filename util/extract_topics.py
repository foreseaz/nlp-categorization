# -*- coding: utf-8 -*-

import json
import os
import re
import shutil


keep_topics_path = "../data/provider_topics/keep_topics.json"

def mk_dirs(root_path):
    train_path = root_path + "/train"
    test_path = root_path + "/test"

    if os.path.exists(train_path):
        shutil.rmtree(train_path)
    os.makedirs(train_path)

    if os.path.exists(test_path):
        shutil.rmtree(test_path)
    os.makedirs(test_path)

    keep_topics_file = open(keep_topics_path,'r')
    keep_topics = json.loads(keep_topics_file.read())
    for subject_index in keep_topics.keys():
        for topic_index in keep_topics[subject_index]['topics']:
            topic_name = keep_topics[subject_index]['topics'][topic_index]
            os.mkdir(train_path + "/" + topic_name)
            os.mkdir(test_path + "/" + topic_name)

    keep_topics_file.close()


def distribute_with_topics(data_path,json_path,train_slices,total_slices):
    subjects = {}
    topics = {}

    json_file = open(json_path)
    courses = json.loads(json_file.read())

    for course in courses:
        if not course['topic_name'] or course['subject_name'] == course['topic_name']:
            continue

        if not course['title']:
            continue

        ###### temp exchange ######
        subject_name = course['subject_name'][0].strip()
        topic_name = course['topic_name'][0].strip()

        if subjects.has_key(subject_name):
            subjects[subject_name].append(topic_name)
        else:
            subjects[subject_name] = [topic_name]

        subjects[subject_name] = list(set(subjects[subject_name]))

        topic_status = topics.get(topic_name)
        if topic_status == None:
            topics[topic_name] = 0

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

    subjects_file = open('../output/classcentral_subjects.json','w')
    output_subjects = json.dumps(subjects,ensure_ascii=False,indent=4)
    subjects_file.write(output_subjects.encode("utf-8"))
    subjects_file.close()

if __name__ == '__main__':
    # make the datasets directories
    dir_path = "../data/datasets/total"
    # dir_path = "../data/datasets/en"
    # dir_path = "../data/datasets/zh"
    # dir_path = "../data/datasets/others"
    mk_dirs(dir_path)



    print "done!"