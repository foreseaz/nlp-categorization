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


def inject_into_datasets(root_path,json_path,train_slices,total_slices,prefix):
    train_path = root_path + "/train"
    test_path = root_path + "/test"

    json_file = open(json_path)
    courses = json.loads(json_file.read())

    topics = {}
    train_count = 0
    test_count = 0
    for course in courses:
        if not course['title']:
            print "the course",course,"has no title!!"
            exit(1)

        ###### temp exchange ######
        topic_name = course['topic_name'][0]

        topic_status = topics.get(topic_name)
        if topic_status == None:
            topics[topic_name] = 0
            topic_status = 0

        if topic_status < train_slices:
            outfile = open(train_path + "/" + topic_name + "/" + prefix + "-" + str(train_count) + ".json", "wb")
            outline = json.dumps(course,ensure_ascii=False,indent=2)
            outfile.write(outline.encode("utf-8"))
            outfile.close()
            topics[topic_name] = (topics[topic_name] + 1) % total_slices
            train_count += 1
        elif topic_status >= train_slices:
            outfile = open(test_path + "/" + topic_name + "/" + prefix + "-" + str(test_count) + ".json", "wb")
            outline = json.dumps(course,ensure_ascii=False,indent=2)
            outfile.write(outline.encode("utf-8"))
            outfile.close()
            topics[topic_name] = (topics[topic_name] + 1) % total_slices
            test_count += 1
    print "train:",train_count,"test:",test_count
    json_file.close()

def trainset_count(root_path):
    train_path = root_path + "/train"
    topic_dirs = {}
    for topic_dir in os.listdir(train_path):
        file_count = len([name for name in os.listdir(train_path+"/"+topic_dir)])
        topic_dirs[topic_dir] = file_count
    return topic_dirs


if __name__ == '__main__':
    # make the datasets directories

    # dir_path = "../data/datasets/en"
    # dir_path = "../data/datasets/zh"
    # dir_path = "../data/datasets/others"
    dir_path = "../data/datasets/en"
    mk_dirs(dir_path)
    print "#### class central"
    inject_into_datasets(dir_path,"../output/classified_courses/en/map_classcentral.json",4,5,"classcentral")
    print "#### udemy"
    inject_into_datasets(dir_path, "../output/classified_courses/en/map_udemy.json", 4, 5,"udemy")
    print "#### coursera"
    inject_into_datasets(dir_path, "../output/classified_courses/en/map_coursera.json", 3, 5,"coursera")
    print "Count train set:"
    # topic_dirs = trainset_count(dir_path)
    # for topic in topic_dirs.keys():
    #     if topic_dirs[topic] < 100:
    #         print "\t"+topic+":",topic_dirs[topic]
    print "done!"