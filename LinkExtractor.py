from bs4 import BeautifulSoup
import requests

def URL_Extractor(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    URLfile = open("URL_automation.txt", "w")
    for link in links:
        if(link.startswith('http')):
            URLfile.write(link +"\n")
    URLfile.close()

