# -*- coding: utf-8 -*-
en_par = 0.8
ch_par = 0.4
en_ch_par = 0.6
en_or_ch = 2.0
en_path = "en/"
ch_path = "ch/"
others_path = "others/"
others_par = 0.01

import os
import json
import shutil
import codecs
import re

def clf(string):
    en_len = 0.0
    ch_len = 0.0
    others_len = 0.0
    tot_len = len(string)
    for char in string:
        if u'\u4e00' <= char and char <= u'\u9fa5':
            ch_len += 1
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
    if en_len/tot_len >= en_par:
        return "English"
    elif ch_len/tot_len >= ch_par:
        return "Chinese"
    elif (ch_len + en_len)/tot_len >= en_ch_par:
        if en_len >= en_or_ch * ch_len:
            return "English"
        else:
            return "Chinese"
    else:
        return "Others"