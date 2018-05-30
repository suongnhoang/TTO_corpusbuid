import argparse
import pandas as pd
import requests
import pickle
from bs4 import BeautifulSoup # To parse html text
import json, codecs
from time import sleep

TEMPT_file_path = '../FILES/TEMPT'
links_cvs_file_path = '../FILES/LINKS.csv'
categories_json_path = '../FILES/categories.json'
categories_dict_json_path = '../FORMS/categories_dict.json'

def get_links(url, date): 
    url_list = []
    

    while True:
        tree = parse_html(url)
        list_news_content = tree.find(class_="list-news-content pdt30")

        if(list_news_content != None):
            break
            
    url_dict = {}

    for item in list_news_content.find_all(class_="block-right-info fr"):
        url_dict['url'] = 'https://tuoitre.vn' + item.find('a')['href']
        url_dict['category'] = url.split('/')[3]
        url_dict['day'] = date[0]
        url_dict['month'] = date[1]
        url_dict['year'] = date[2]
        
        url_list.append(url_dict)
    return url_list
	
def get_page_links(link):
    links_tuple = []
    
    date = link.split('/')[5].replace('.html', '').split('-')

    html_tree = parse_html(link)
    mgr = html_tree.find(class_="page_right mgr15")

    if mgr != None:
        mgr15 = mgr.find_all('a')
        for item in mgr15[:len(mgr15) - 1]:
            links_tuple.extend(get_links('https://tuoitre.vn' + item['href'], date))
    else:
        links_tuple.extend(get_links(link, date))
    return links_tuple
	


i = 0

try:
    df  = read_CSV(links_cvs_file_path)
except:
    df =pd.DataFrame(columns=['url','category','day','month','year'])
    df.to_csv(links_cvs_file_path)

with codecs.open(TEMPT_file_path, 'rb') as fp:
    url_links = pickle.load(fp)

tmp = []

for link in url_links:
    
    if(i%100 == 0 and i > 0):
        with codecs.open(TEMPT_file_path, 'wb') as fp:
            pickle.dump(url_links, fp)
        df = df.append(pd.DataFrame(tmp), ignore_index=True)
        df.to_csv(links_cvs_file_path)
        tmp = []
        sleep(10)
    
    tmp.extend(get_page_links(url_links[i]))
    
    url_links.remove(url_links[i])
    

    i += 1
    print "\r%d %d" %(len(url_links),len(tmp)),