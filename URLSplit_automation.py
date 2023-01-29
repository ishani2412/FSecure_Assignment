import sys
from urllib.parse import urlsplit
import LinkExtractor
# Take input from the terminal
url = sys.argv[1]

def URL_to_split(url):
    print("URL:", url)
    parsed_url = urlsplit(url)
    tld = parsed_url.netloc.split('.')[-1]
    base_domain = parsed_url.netloc
    base_domain = ('.'.join(base_domain.split('.')[-2:]))
    base_hostname = parsed_url.hostname
    path = parsed_url.path
    links=[]
    LinkExtractor.URL_Extractor(url)
    # Reading file containing all the URL
    URLfile = open("URL_automation.txt", "r") 
    for link in URLfile:
        links.append(link.rstrip())
    URLfile.close()
    same_hostname = []
    same_domain = []
    diff_domain = []

    for link in links:
        parsed_link = urlsplit(link)
        tld = parsed_url.netloc.split('.')[-1]
        domain = parsed_link.netloc
        domain = ('.'.join(domain.split('.')[-2:]))
        hostname = parsed_link.hostname
        if hostname == base_hostname:
            same_hostname.append(link)
        elif domain == base_domain:
            same_domain.append(link)
        else:
            diff_domain.append(link)

    print("TLD:", tld)
    print("DOMAIN:", base_domain)
    print("HOSTNAME:", base_hostname)
    print("PATH:", path)
    print("LINKS:")
    print("\t Same hostname: ",*same_hostname, sep="\n \t \t")
    print("\t Same domain: ",*same_domain,sep="\n \t \t")
    print("\t Different domain: ",*diff_domain, sep="\n \t \t")

URL_to_split(url)