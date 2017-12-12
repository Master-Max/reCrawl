import sys
import requests
import re
from bs4 import BeautifulSoup

#crawledLinks = []
crawled = {}
virgin = True
key = 0

def keyPlus():
    global key
    key += 1

def addCrawled(l):
    global crawled
    crawled.update({key:l})
    keyPlus()
    #return key-1

class Link:
    def __init__(self, myKey, parent, fullHtml, url, children):
        self.myKey = myKey
        self.parent = parent
        self.fullHtml = fullHtml
        self.url = url
        self.children = children

#####	Filter out unwanted links
ignoreVals = {'','/'}
def desiredLinks(href):
	if not href:
		return False
	if href.startswith('#'):
		return False
	if href in ignoreVals:
		return False
	if href.startswith('/'):
		return False
	if not href.startswith('http'):
		return False
	return True

def crawl(parent, current, breadth, depth, ex):
    if ex:
        x = crawled.get(current)
        parent = x.parent
        url = x.url
    else:
        p = parent
        url = current.
    b = int(b)
    d = int(d)
    tmpB = b
    print('\nCrawling: {}'.format(url))
    print('bre: {} | dep: {}'.format(b, d))

    linkList = []
    r = requests.get(url)
    r_html = r.text
    soup = BeautifulSoup(r_html, 'lxml')

    for link in soup.find_all('a',href=desiredLinks):
        A = link.get('href')
        if A not in linkList:
            if A not in crawledLinks:
                if tmpB > 0:
                    linkList.append(A)
                    tmpB -= 1

    if ex:
        continue
    else:
        if virgin:
            x = Link(key, key, r_html, url, linkList)
            addCrawled(x)
            virgin = False
        else:
            x = Link(key, parent, r_html, url, linkList)
            addCrawled(x)

    if d > 0:
        for i in range(0,b):
            if x.children[i] not in crawledLinks:
                crawl(x.myKey, x.children[i], b, d-1, False)
    else:
        crawl()
