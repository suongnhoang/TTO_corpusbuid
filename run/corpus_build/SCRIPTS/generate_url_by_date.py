import argparse
import pandas as pd
import requests
import pickle
from bs4 import BeautifulSoup # To parse html text
import json, codecs
from datetime import datetime
from datetime import timedelta

first_year = 2008
last_year = 2018

TEMPT_file_path = '../FILES/TEMPT'
links_cvs_file_path = '../FILES/LINKS.csv'
categories_json_path = '../FILES/categories.json'
categories_dict_json_path = '../FORMS/categories_dict.json'

def parse_html(url):
    html_content = requests.get(url).content
    return BeautifulSoup(html_content, 'html.parser')
	
def read_CSV(filename):
    return pd.DataFrame.from_csv(filename)

def list_all_day_in_month(url, year, day = 1 ,month = 1):
    url_list_in_moth = []
    front_URL = url + "/xem-theo-ngay/"
    str_date = str(year) + '-' + str(month) + '-' + str(day)
    date_object = datetime.strptime(str_date, '%Y-%m-%d')
    while(int(date_object.month) == month):
        if (date_object < datetime.now()):
            url_list_in_moth.append(front_URL + date_object.strftime('%#d-%#m-%Y') + '.html')
            date_object += timedelta(days=1)
        else:
            break
    return url_list_in_moth
	
with codecs.open(categories_json_path, 'r', encoding='utf-8') as fp:
    categories = json.load(fp)
    url_links = []

for title1 in categories:
    
    back = categories[title1]
    
    if (isinstance(back, basestring)):
        href = back
        if(href.find('https') == -1):
            url = 'https://tuoitre.vn' + href.replace(".htm",'')
            for year in range(first_year, last_year+1):
                    for month in range(1,13):
                        url_links.extend(list_all_day_in_month(url, year = year, month = month))
    else:
        categories_lv2 = back
        href_main = ""
        for title2 in categories_lv2:
            
            if(categories_lv2[title2].find('https') == -1):
                href_main = categories_lv2[title2].split('/')[1]
                href2 = categories_lv2[title2].split('/')[2]
                
                url2 = 'https://tuoitre.vn/' + href2.replace(".htm",'')
                for year in range(first_year, last_year):
                        for month in range(1,13):
                            url_links.extend(list_all_day_in_month(url2, year = year, month = month))
                        
        if(href_main != ""):
            url_main = 'https://tuoitre.vn/' + href_main
            for year in range(first_year, last_year):
                for month in range(1,13):
                    url_links.extend(list_all_day_in_month(url_main, year = year, month = month))

with codecs.open(TEMPT_file_path, 'wb') as fp:
    pickle.dump(url_links, fp)