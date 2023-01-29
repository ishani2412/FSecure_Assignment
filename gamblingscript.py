import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import string
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords',quiet=True)
nltk.download('punkt',quiet=True)
nltk.download('wordnet',quiet=True)
from nltk.stem import PorterStemmer
from collections import Counter
import operator
import sys
import json

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
    
# classifying 
def classifier(url, customKeywords, Dict, checkThreshold = 30, fastClassificationFlag = True):
    # for fast classification without opening the URL
    if fastClassificationFlag:
        for customKeyword in customKeywords:
            if customKeyword in url:
                return 'Gambling site' 
    text_tokens = scapper(url)
    localDict = dict(Counter(text_tokens))
    ## classification part
    Dict = dict(sorted(Dict.items(), key=operator.itemgetter(1), reverse = False))
    Dict = {x:e*2 for e,x in enumerate(Dict)}
    
    localDict = {k:v for k,v in localDict.items() if k in list(Dict)}
    ratioDict = {k: localDict[k]/Dict[k] for k in Dict.keys() & localDict}
    ratioDict = dict(sorted(ratioDict.items(), key=operator.itemgetter(1), reverse = True))
    weightDict = {k:v/max(Dict.values()) for k,v in Dict.items() }
    weightedRatioDict = {k:ratioDict[k]*weightDict[k] for k in ratioDict.keys() & weightDict}    
    score = sum(weightedRatioDict.values())*100
    
    retVal = "Gambling site" if score > checkThreshold else "Non-Gambling site"
    return retVal, score

#user input
websiteToTest = sys.argv[1]
Dict = json.loads(json.load(open("dict.json")))
# for fast classification, fill more if needed
customKeywords = ['casino','gamble','betting','roullete']
checkThreshold = 50
print(classifier(websiteToTest, customKeywords, Dict, checkThreshold, fastClassificationFlag = True) )  
