# -*- coding: utf-8 -*-

import json


def raw2json(raw_path,filename):
    raw_file = open(raw_path+filename+".json")
    output= {}
    for line in raw_file.readlines():
        topic_name = line.strip().split("\t")[0]
        keep_index = line.strip().split("\t")[1]
        output[topic_name] = keep_index
    raw_file.close()
    json_file = open(raw_path+filename+'.json', 'w')
    output_subjects = json.dumps(output, ensure_ascii=False, indent=2)
    json_file.write(output_subjects.encode("utf-8"))
    json_file.close()

if __name__ == '__main__':
    raw2json('../data/topic_mapping/','coursera2keep')
    # keep_topics_file = open("../data/topic_mapping/keep_topics.json")
    # keep_topics = json.loads(keep_topics_file.read())
    #
    # keep_subjects_new = {}
    # sub_index = 0
    # for subject in keep_topics:
    #     keep_subjects_new[sub_index] = {}
    #     keep_topics_new = {}
    #     top_index = 0
    #     for topic in subject['topics']:
    #         keep_topics_new[top_index] = topic
    #         print str(sub_index)+"-"+str(top_index),topic
    #         top_index += 1
    #     keep_subjects_new[sub_index]['subject_name'] = subject['subject_name']
    #     keep_subjects_new[sub_index]['topics'] = keep_topics_new
    #     sub_index += 1
    #
    # subjects_file = open('../data/topic_mapping/keep_subjects.json', 'w')
    # output_subjects = json.dumps(keep_subjects_new, ensure_ascii=False, indent=2)
    # subjects_file.write(output_subjects.encode("utf-8"))
    # subjects_file.close()
    #
    # keep_topics_file.close()
    print 'done!'