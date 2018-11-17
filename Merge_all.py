from nltk.stem.porter import PorterStemmer
import jieba
import math
import sys
import os
import json
from pathlib import Path
import re

tmp_reader = {}
file_list = os.listdir('C:\\Users\\dlwog\\Pictures\\SecurityTracker')

tmp_list = []
for file_name in file_list:
    if '.json' in file_name:
        tmp_list.append(file_name)

tmp_json = {}
for tmp in tmp_list:
    print(tmp)
    key = tmp[0 : tmp.find('.json')]

    if 'E-mail' not in key:
        key = re.sub('-', '/', key)

    tmp_str = ""
    with open('C:\\Users\\dlwog\\Pictures\\SecurityTracker\\' + tmp, 'r', encoding='utf-8-sig') as json_file:
        for line in json_file.readlines():
            if line == '}{\n':
                tmp_str = tmp_str + '}ㅂ{'
            else:
                tmpstring = re.sub('\n', '', line)
                while (1):
                    if tmpstring[0] == ' ' or tmpstring[0] == '\xa0':
                        tmpstring = tmpstring[1:]
                    else:
                        break
                tmp_str = tmp_str + tmpstring

    if tmp_str == "":
        tmp_json[key] = []
        print(key)
        continue

    new_list = tmp_str.split('ㅂ')
    dict_list = []
    for lis in new_list:
        dict_list.append(json.loads(lis))

    tmp_json[key] = dict_list
    print(key)



with open('C:\\Users\\dlwog\\Pictures\\hi\\SecurityTracker.json', 'w', encoding='utf-8') as json_file:
    json.dump(tmp_json, json_file, ensure_ascii=False)

