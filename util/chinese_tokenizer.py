# -*- coding: utf-8 -*-
import sys
sys.path.append("../lib/")
import jieba
import jieba.analyse
import json

courses = json.loads(open('../output/classified_courses/ch/map_classcentral.json').read())

course_content = courses[0]['description']
# seg_list = jieba.cut(course_content)
# jieba.analyse.set_stop_words('stop_words.txt')
seg_list = jieba.cut('小明硕士毕业于中国科学院计算所 后在日本京都大学深造')
print ",".join(seg_list)