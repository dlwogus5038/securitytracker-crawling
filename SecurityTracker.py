#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests #导入requests 模块
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import re
import json
from pathlib import Path

home_url = 'https://securitytracker.com/topics/topics.html#category'
pre_url = 'https://securitytracker.com'

def get_html_label(web_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}  # 给请求指定一个请求头来模拟chrome浏览器
    req = requests.get(web_url, headers=headers)  # 像目标url地址发送get请求，返回一个response对象
    req.encoding = 'utf-8'

    html_label = BeautifulSoup(req.text, 'lxml')
    return html_label


def get_url_list(url):
    tmp_url = 'https://securitytracker.com/archives/category/'

    labels = get_html_label(url)
    table = labels.find('table', cellspacing='0', cellpadding='0')
    try:
        urls = table.find_all('a', href=re.compile('/id/'))
    except:
        return []

    return_list = []
    for elem in urls:
        return_list.append(pre_url + elem['href'])

    check_next = labels.find('a', text='Next Page')
    if check_next is not None:
        return_list.extend(get_url_list(tmp_url + check_next['href']))

    return return_list


def get_page_content(url, dict_list):
    labels = get_html_label(url)
    table_labels = labels.find_all('table', width='100%')
    result_dict = {}
    result_dict['source'] = '1-2'
    for table in table_labels:
        if 'Source Message Contents' in table.text:
            fonts = table.find_all('font', face='Arial, Helvetica')
            for font in fonts:
                img_label = font.find('img')
                if img_label is not None:
                    break

                b_labels = font.find_all('b')
                if len(b_labels) == 0:
                    continue

                for b_label in b_labels:
                    if len(b_labels) > 1:
                        tmp_list = font.find_all('b')
                        index_list = []
                        font_text = font.text
                        for tmp in tmp_list:
                            index_list.append(font_text.find(tmp.text))

                        str_list = []
                        pre_ind = index_list[0]
                        count = 0
                        for ind in index_list:
                            if count == 0:
                                count = count + 1
                                continue
                            str_list.append(font_text[pre_ind : ind])
                            pre_ind = ind

                        str_list.append(font_text[pre_ind : ])

                        for st in str_list:

                            cut_ind = st.find(':')
                            result_dict[st[0:cut_ind]] = st[cut_ind + 1 : ]

                        break

                    b_text = b_label.string
                    end_index = b_text.find(':')

                    if int(font['size']) >= 0:
                        result_dict['Title'] = b_text
                        print(b_text)
                    else:
                        if b_text[0:end_index] not in result_dict:
                            result_dict[b_text[0:end_index]] = None
                        b_label.extract()

                        if b_text[0:end_index] == 'Message History' and 'None' not in font.text:
                            result_dict[b_text[0:end_index]] = []
                            a_labels = font.find_all('a')
                            for a in a_labels:
                                result_dict[b_text[0:end_index]].append(pre_url + a['href'])
                            break

                        a_labels = font.find_all('a')
                        if len(a_labels) > 0:
                            if len(a_labels) > 1:
                                result_dict[b_text[0:end_index]] = []
                                for a in a_labels:
                                    result_dict[b_text[0:end_index]].append(a.text)
                            else:
                                for a in a_labels:
                                    result_dict[b_text[0:end_index]]= a.text
                        else:
                            if result_dict[b_text[0:end_index]] is not None:
                                result_dict[b_text[0:end_index] + '\''] = font.text
                            else:
                                result_dict[b_text[0:end_index]] = font.text


    for elem in result_dict:
        while(1):
            if result_dict[elem][0] == '\n' or result_dict[elem][0] == ' ' or result_dict[elem][0] == '\xa0':
                result_dict[elem] = result_dict[elem][1:]
            else:
                break
        while(1):
            if result_dict[elem][-1] == '\n' or result_dict[elem][-1] == ' ' or result_dict[elem][-1] == '\xa0':
                result_dict[elem] = result_dict[elem][0:-1]
            else:
                break
    dict_list.append(result_dict)




html_label = get_html_label(home_url)

result = {}
category = html_label.find_all('a', href=re.compile('/archives/category/'))
for elem in category:
    print(elem.text)
    result[elem.text] = []

    file_name = re.sub('/', '-', elem.text)
    file_exist = Path('C:\\Users\\dlwog\\Pictures\\SecurityTracker\\' + file_name + '.json')
    if file_exist.is_file():
        print('C:\\Users\\dlwog\\Pictures\\SecurityTracker\\' + file_name + '.json' + "already exist")
        continue

    url_list = get_url_list(pre_url + elem['href'])
    for url in url_list:
        get_page_content(url, result[elem.text])

    with open('C:\\Users\\dlwog\\Pictures\\SecurityTracker\\' + file_name + '.json', 'w', encoding='utf-8') as json_file:
        for elem in result[elem.text]:
            json.dump(elem, json_file, ensure_ascii=False, indent=4)
print('abc')

