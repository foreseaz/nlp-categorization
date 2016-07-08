# -*- coding: utf-8 -*-

import os
import json
import shutil
import codecs
import re

en_par = 0.8
ch_par = 0.6
jp_par = 0.4
ko_par = 0.4
others_par = 0.05
en_ch_par = 0.6
en_or_ch = 2.0

def is_jp(char):
    isHiragana = u'\u3040' <= char and char <= u'\u309f'
    isKatakana = (u'\u30a0' <= char and char <= u'\u30ff') or (u'\u31f0' <= char and char <= u'\u31ff')
    return isHiragana or isKatakana

def is_ch(char):
    isChar = u'\u4e00' <= char and char <= u'\u9fa5'
    # isPunc = u'\u3000' <= char and char <= u'\u303f'
    return isChar

def is_ko(char):
    isChar = u'\uac00' <= char and char <= u'\ud7af'
    isAlpha =(u'\u1100' <= char and char <= u'\u11ff') or (u'\u3130' <= char and char <= u'\u318f')
    return isChar or isAlpha

def clf(string):
    en_len = 0.0
    ch_len = 0.0
    jp_len = 0.0
    ko_len = 0.0
    others_len = 0.0
    tot_len = len(string)
    for char in string:
        if is_ch(char):
            ch_len += 1
        if is_jp(char):
            jp_len += 1
        if is_ko(char):
            ko_len += 1
        if (u'a' <= char and char <= u'z') or (u'A' <= char and char <= u'Z'):
            en_len += 1
        if u',' == char or u'.' == char or u'、' == char or u'\r' == char or u' ' == char \
        or u'\n' == char or (u'\u2700' <= char and char <= u'\u27bf') or (u'\u2600' <= char and char <= u'\u26ff') \
        or (u'\u0000' <= char and char <= u'\u007f' and not ((u'a' <= char and char <= u'z') or (u'A' <= char and char <= u'Z'))):
            tot_len -= 1
        if u'ó' == char or u'ú' == char or u'é' == char or u'á' == char or u'ö' == char or u'ç' == char or u'ã' == char:
            others_len += 1
    if tot_len <= 0:
        tot_len = 1
    if others_len >= others_par * tot_len:
        en_len = 0
        ch_len = 0
        jp_len = 0
        ko_len = 0
    if ko_len/tot_len >= ko_par:
        return "Korean"
    elif jp_len/tot_len >= jp_par:
        return "Japanese"
    elif ch_len/tot_len >= ch_par:
        return "Chinese"
    elif en_len / tot_len >= en_par:
        return "English"
    elif (ch_len + en_len)/tot_len >= en_ch_par:
        if en_len >= en_or_ch * ch_len:
            return "English"
        else:
            return "Chinese"
    else:
        return "Others"


if __name__ == '__main__':
    raw_path = '../data/raw_courses/total'
    output_dirs = {
        'English': '../data/raw_courses/en',
        'Chinese': '../data/raw_courses/ch',
        'Japanese': '../data/raw_courses/jp',
        'Korean': '../data/raw_courses/ko',
        'Others': '../data/raw_courses/others'
    }

    for dir_key in output_dirs.keys():
        dir = output_dirs[dir_key]
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.mkdir(dir)
    files = os.listdir(raw_path)
    for f in files:
        lang_courses = {'English':[],'Chinese':[],'Japanese':[],'Korean':[],'Others':[]}
        file = open(os.path.join(raw_path,f))
        course_set = json.loads(file.read())
        for course in course_set:
            if course['title'] is None or course['course_url'] is None:
                continue
            if course['description'] is None:
                course['description'] = ''
            content = course['title']+'\n'+course['description']
            lang = clf(content)
            course['language_name'] = [lang]
            lang_courses[lang].append(course)
        file.close()
        for lang_key in lang_courses.keys():
            if len(lang_courses[lang_key]) > 0:
                output_file = open(os.path.join(output_dirs[lang_key], f), 'w')
                output_file.write(json.dumps(lang_courses[lang_key],ensure_ascii=False,indent=2).encode('utf-8'))
                output_file.close()

    print 'done.'