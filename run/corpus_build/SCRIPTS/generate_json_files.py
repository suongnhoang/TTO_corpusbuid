import argparse
import pandas as pd
import requests
import pickle
from bs4 import BeautifulSoup # To parse html text
import json, codecs

TEMPT_file_path = '../FILES/TEMPT'
links_cvs_file_path = '../FILES/LINKS.csv'
categories_json_path = '../FILES/categories.json'
categories_dict_json_path = '../FORMS/categories_dict.json'

def parse_html(url):
    html_content = requests.get(url).content
    return BeautifulSoup(html_content, 'html.parser')
	
post_url = 'https://tuoitre.vn/'
try:
    post_tree = parse_html(post_url)
except:
    print 'Cannot read ' + post_url

categories = {}
categories_dict = {}

for item in post_tree.find(class_="clearfix fl").find_all('a'):
    if(item['title'] != 'Home' and item['title'] != 'Media'):
        
        categories_2 = {}
        
        if(item['href'].find('https') == -1):
            url = 'https://tuoitre.vn' + item['href']
            
            categories_dict[item['href'].replace(".htm", "").replace("/", "")] = item['title'].rstrip().lstrip()
            
            tree = parse_html(url)
            
            for item2 in tree.find(class_="list-bc").find_all('a'):
                if(item2['href'].find('https') == -1):
                    categories_2[item2['title']] = item2['href']
                    categories_dict[item2['href'].split("/")[2].replace(".htm", "")] = item2['title'].rstrip().lstrip()

            if(len(categories_2) > 0):
                categories[item['title']] = categories_2
            else:
                categories[item['title']] = item['href']
        else:
            categories[item['title']] = item['href']
        
        
with codecs.open(categories_json_path, 'w', encoding='utf-8') as fp:
    json.dump(categories, fp, ensure_ascii=False)
    
with codecs.open(categories_dict_json_path, 'w', encoding='utf-8') as fp:
    json.dump(categories_dict, fp, ensure_ascii=False)