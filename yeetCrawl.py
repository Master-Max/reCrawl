import sys
import requests
import re
from bs4 import BeautifulSoup

dbg = False

crawledLinks = {}
cashedHtml = {}
toGetLinks = []
key = 0

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

def keyPlus():
    global key
    key += 1

def addLink(l):
    global crawledLinks
    crawled.update({key:l})
    keyPlus()

def storeHtml(k, h):
    global cashedHtml
    cashedHtml.update({k, h})

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

#####   Crawl def

def crawl(url,b,d):
    url = str(url)
    d = int(d)
    b = int(b)
    tmbB = b
    print('\nCrawling: {}'.format(url))
    print('bre: {} | dep: {}'.format(b,d))

    r = requests.get(url)
    r_html = r.text
    m5 = md5(r_html)

    if m5 not in cashedHtml:
        linkList = []
        addLink(url)
        storeHtml(key, m5)

        if d > 0:

            soup = BeautifulSoup(r_html, 'lxml')

            for link in soup.find_all('a',href=desiredLinks):
                A = link.get('href')
                if A not in linkList:
                    if A not in crawledLinks:
                        if tmpB > 0:
                            linkList.append(A)
                            tmpB -= 1

                            global toGetLinks
                            toGetLinks.append(linkList)

            return d - 1
        else:
            return breadth
    else:
        return -1





#####   Get Command line args and throw usage case if user f'ed up
if len(sys.argv) < 3:
	print('Usage: reCrawl.py [string - URL] [int - Breadth] [int - Depth]')
	sys.exit()

url = str(sys.argv[1]) #URL to go to
breadth = int(sys.argv[2]) #How Wide To Search
depth = int(sys.argv[3]) #How Deep To Search
print('Url: {u}\nBreadth: {b}\nDepth: {d}\n'.format(u = url, b = breadth, d = depth))

if 'www' not in url:
	url = 'www.' + str(url)
if 'https://' not in url:
	url = 'https://' + str(url)
####    Requesting the url
#print('Requesting: {}'.format(url))

if crawl(url,breadth,depth)
