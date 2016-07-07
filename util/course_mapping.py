# -*- coding: utf-8 -*-

import json

def print_topics_index():
    keep_topics_file = open("../data/topic_mapping/keep_topics.json")
    keep_topics = json.loads(keep_topics_file.read())

    keep_subjects_new = {}
    sub_index = 0
    for subject in keep_topics:
        keep_subjects_new[sub_index] = {}
        keep_topics_new = {}
        top_index = 0
        for topic in subject['topics']:
            keep_topics_new[top_index] = topic
            print str(sub_index) + "-" + str(top_index), topic
            top_index += 1
        keep_subjects_new[sub_index]['subject_name'] = subject['subject_name']
        keep_subjects_new[sub_index]['topics'] = keep_topics_new
        sub_index += 1

    subjects_file = open('../data/topic_mapping/keep_topics.json', 'w')
    output_subjects = json.dumps(keep_subjects_new, ensure_ascii=False, indent=2)
    subjects_file.write(output_subjects.encode("utf-8"))
    subjects_file.close()

    keep_topics_file.close()

def raw2json(raw_path,filename,isCoursera):
    raw_file = open(raw_path+filename+".json")
    output= {}
    for line in raw_file.readlines():
        topic_name = line.split("\t")[0].strip()
        keep_index = line.split("\t")[1].strip()
        if isCoursera:
            topic_name = topic_name.lower().replace(" ","-")
        output[topic_name] = keep_index
    raw_file.close()
    json_file = open(raw_path+filename+'.json', 'w')
    output_subjects = json.dumps(output, ensure_ascii=False, indent=2)
    json_file.write(output_subjects.encode("utf-8"))
    json_file.close()

def map_courses(raw_path,mapper_path,output_path,unmap_path):
    keep_topics_file = open("../data/provider_topics/keep_topics.json","r")
    raw_file = open(raw_path,'r')
    mapper_file = open(mapper_path, 'r')
    keep_topics = json.loads(keep_topics_file.read())
    raw_courses = json.loads(raw_file.read())
    mapper = json.loads(mapper_file.read())
    map_courses = []
    unmap_courses = []
    for course in raw_courses:
        topic_name = ""
        if len(course['topic_name']) > 0:
            topic_name = course['topic_name'][0].strip()
        elif len(course['subject_name']) > 0:
            topic_name = course['subject_name'][0].strip()
            course['subject_name'] = []
        if topic_name != "" and mapper.has_key(topic_name):
            if mapper[topic_name] == "-":
                unmap_courses.append(course)
            else:
                sub_index = mapper[topic_name].split("-")[0].encode('utf-8')
                top_index = mapper[topic_name].split("-")[1].encode('utf-8')
                # print topic_name,sub_index,top_index
                map_subject = keep_topics[sub_index]['subject_name'].strip()
                map_topic = keep_topics[sub_index]['topics'][top_index].strip()
                course['topic_name'] = [map_topic]
                course['subject_name'] = [map_subject]
                map_courses.append(course)
        else:
            unmap_courses.append(course)
    mapper_file.close()
    raw_file.close()
    keep_topics_file.close()

    print "total:",len(raw_courses),
    output_file = open(output_path,'w')
    print "map:",len(map_courses),
    output_file.write(json.dumps(map_courses,ensure_ascii=False,indent=2).encode('utf-8'))
    output_file.close()
    unmap_file = open(unmap_path,'w')
    print "unmap:",len(unmap_courses)
    unmap_file.write(json.dumps(unmap_courses,ensure_ascii=False,indent=2).encode('utf-8'))
    unmap_file.close()

def excute_mapping(language):
    # mapping classcentral
    print "\tmapping classcentral ==>",
    map_courses('../data/raw_courses/'+language+'/classcentral_courses.json',
                '../data/topic_mapping/classcentral2keep.json',
                '../output/classified_courses/'+language+'/map_classcentral.json',
                '../output/unmap_courses/'+language+'/unmap_classcentral.json')

    # mapping udemy
    print "\tmapping udemy ==>",
    map_courses('../data/raw_courses/'+language+'/udemy_courses.json',
                '../data/topic_mapping/udemy2keep.json',
                '../output/classified_courses/'+language+'/map_udemy.json',
                '../output/unmap_courses/'+language+'/unmap_udemy.json')

    # mapping coursera
    print "\tmapping coursera ==>",
    map_courses('../data/raw_courses/'+language+'/coursera_courses.json',
                '../data/topic_mapping/coursera2keep.json',
                '../output/classified_courses/'+language+'/map_coursera.json',
                '../output/unmap_courses/'+language+'/unmap_coursera.json')

if __name__ == '__main__':
    excute_mapping('en')
    print 'done!'