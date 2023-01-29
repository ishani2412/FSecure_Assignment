import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import string
import re
import nltk
import json
from nltk.corpus import stopwords
nltk.download('stopwords',quiet=True)
nltk.download('punkt',quiet=True)
nltk.download('wordnet',quiet=True)
from nltk.stem import PorterStemmer
from collections import Counter
import operator
import sys

#user input
websites = sys.argv[1]

# hunting websites related to gambling

def scapper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if response.status_code != 200:
        print(url, "site not reachable")
        return Dict 
    ps = PorterStemmer()
    keywords = []
    
    for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'li']):
        text_data = tag.get_text().lower()
        text_data = re.sub('['+string.punctuation+']', ' ',text_data)
        keywords.extend(text_data.split())
    
    text_tokens = [word for word in keywords if not word in stopwords.words('english')]
    text_tokens = [ps.stem(x) for x in text_tokens]
    return text_tokens
    

# scraping keywords for knowlwdge base
def gambling_dict_creator(url, Dict, threshold = 30):
    text_tokens = scapper(url)
    localDict = dict(Counter(text_tokens))
    localDict = {k:v for k,v in localDict.items() if v > threshold}
    Dict = dict(Counter(Dict) + Counter(localDict))
    return Dict          

Dict = {}
data = pd.read_csv(websites)
threshold = int(len(data))
for url in data.Link:
    try:
        Dict = gambling_dict_creator(url, Dict, threshold)
    except:
        print(url,"error in site")
        
print("Number of keywords: ", len(Dict)) 

with open("dict.json", "w") as f:
    json.dump(json.dumps(Dict), f)  