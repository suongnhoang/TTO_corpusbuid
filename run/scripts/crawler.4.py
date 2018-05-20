import pandas as pd
import requests
from bs4 import BeautifulSoup # To parse html text
import json, codecs, os
import xmltodict


with codecs.open('./FORMS/CORPUS_FORM.xml', encoding='utf-8') as fd:
    corpus_xml_string_default_front = fd.read().replace("</teiCorpus>","")
    
corpus_xml_string_default_back = "</teiCorpus>"

def read_CSV(filename):
    return pd.DataFrame.from_csv(filename)

def parse_html(url):
    html_content = requests.get(url).content
    return BeautifulSoup(html_content, 'html.parser')

def get_leaf_paragraphs(contents):
    pragraphs = []
    for pragraph in contents:
        tmp = pragraph.find_all('p', recursive=False)
        if (len(tmp) <= 0):
            pragraphs.append(pragraph)
        else:
            pragraphs.extend(get_leaf_paragraphs(tmp))
    return pragraphs

def TTO_crawler(link, category):
    
    id_ = link.split("-")[-1].replace(".htm", "")
    
    try:
        
        tree = parse_html(link)
        
        fck = tree.find(class_="fck")
        contents = get_leaf_paragraphs(fck.find_all('p', recursive=False))

        div = {}

        for i in range(len(contents)):
            text = contents[i].text.replace("\r", " ").replace("\n", " ").rstrip().lstrip()
            if(text != ""):
                paragraph_p = {}
                paragraph_p[u'p'] = text
                div[u"div" + str(i + 1)] = paragraph_p
                
        if(len(div) <= 0):
            return None
                
        #get titles
        
        titel = tree.find(class_="title-2").text.replace("\r"," ").replace("\n"," ").rstrip().lstrip()
        
        date = tree.find(class_="date").text.split(" ")[0].replace("\r"," ").replace("\n"," ").rstrip().lstrip()

        author = tree.find(class_="author").text.replace("\r"," ").replace("\n"," ").rstrip().lstrip().lower()

        front = tree.find(class_="txt-head").text.replace("\r", " ").replace("\n", " ").rstrip().lstrip()

        domain = category
        
    except:
        return None

    #open TEI format
    with codecs.open('./FORMS/TEI_FORM.xml') as fd:
        TEI_string = fd.read()


    TEI = xmltodict.parse(TEI_string, dict_constructor = dict)

    #replace text with format:
    TEI['TEI']['@id'] = id_

    TEI['TEI']['teiHeader']['fileDesc']['titleStmt']['title'] = titel
    TEI['TEI']['teiHeader']['fileDesc']['publicationStmt']['authority'] = author
    TEI['TEI']['teiHeader']['fileDesc']['publicationStmt']['date'] = date

    TEI['TEI']['teiHeader']['fileDesc']['profileDesc']['textDesc']['domain'][u'@type'] = domain

    TEI['TEI']['text']['front'] = front
    TEI['TEI']['text']['body'] = div

    #return xml
    
    return "\t" + xmltodict.unparse(TEI, encoding='utf-8', pretty=True).replace("\n\t", "\n\t\t").replace("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n",  "").replace("</TEI>", "\t</TEI>") + "\n"



with codecs.open('./FORMS/categories_dict.json', 'r', encoding='utf-8') as fp:
    categories_dict = json.load(fp)
    

try:
    valid_df = read_CSV(filename = "./VALIDS/VALIDS.4.csv")
except:
    valid_df =pd.DataFrame(columns=['url','category','day','month','year'])


file_path = "./LINKS/4/"
files = os.listdir(file_path)
files = [os.path.splitext(x)[0] for x in files]

for file_name in files:
    df = read_CSV(file_path + file_name + ".csv")
    
    #try to open or create CORPUS.xml
    try:    
        with codecs.open("./CORPUS/CORPUS."+file_name+".xml") as fd:
            fd.read()
    except:
        with codecs.open("./CORPUS/CORPUS."+file_name+".xml", 'a', encoding='utf-8') as fp:
            fp.write(corpus_xml_string_default_front.replace("TITLE_HERE", "TTO Corpus " + file_name))
    
    for index, row in df.iterrows():
        print "\r%d %s" %(len(df),file_name),
        
        TEI_string = TTO_crawler(row.url, categories_dict[row.category])
        
        if(TEI_string == None):
            valid_df = valid_df.append(row)
            valid_df.to_csv('./VALIDS/VALIDS.4.csv')
        else:
            with codecs.open("./CORPUS/CORPUS."+file_name+".xml", 'a', encoding='utf-8') as fp:
                fp.write(TEI_string)

        df = df.drop(index)
        df.to_csv(file_path + file_name + ".csv")

    with codecs.open("./CORPUS/CORPUS."+file_name+".xml", 'a', encoding='utf-8') as fp:
        fp.write(corpus_xml_string_default_back)
        
    os.remove(file_path + file_name + ".csv")

print "\rFINISHED."