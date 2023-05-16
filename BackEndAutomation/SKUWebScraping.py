import bs4
import requests
import re

import googlesearch
from googlesearch import search

query = 'REV-21-1651'
site = None

for i in search(query, tld="co.in", num=1, stop=1, pause=2):
    site = i

def getHTMLDocument(url):
    response = requests.get(url)
    return response.text

html_document = getHTMLDocument(site)

soup = bs4.BeautifulSoup(html_document, 'html.parser')

for link in soup.find_all('a',
                          attrs={'href': re.compile("^https://")}):
    # display the actual urls
    print(link.get('href'))