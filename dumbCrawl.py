import sys
import requests
import re
import hashlib
from bs4 import BeautifulSoup

dbg = False

limit = 10

crawledLinks = {}
cashedHtml = {}
toGetLinks = []
key = 0
i = 0
##### Filter out unwanted links
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

def addAll(url, m5):
    global crawledLinks, cashedHtml
    crawledLinks.update({key: url})
    cashedHtml.update({key: str(m5)})
    keyPlus()

def addLink(l):
    global crawledLinks
    crawledLinks.update({key:l})
    keyPlus()

def storeHtml(k, h):
    global cashedHtml
    cashedHtml.update({int(k) : str(h)})

def md5(fname):
    m = hashlib.md5()
    m.update(str(fname).encode('utf-8'))
    return m.hexdigest()

def needMoreLinks():
    global i, limit
    i += 1
    limit += 1

def toGetLinksLength():
    tmpX = len(toGetLinks)
    return tmpX

##### Define Crawl
def crawl(url, b):
    url = str(url)
    b = int(b)
    tmpB = b
    print('\nCrawling: {}'.format(url))
    #print('bre: {} | dep: {}'.format(b,d))

    r = requests.get(url)
    r_html = r.text
    m5 = md5(r_html)

    if m5 not in cashedHtml:
    #    linkList = []
    #    addLink(url)
    #    storeHtml(key, m5)
        addAll(url, m5)

        if toGetLinksLength() < limit:
            soup = BeautifulSoup(r_html,'lxml')
            global toGetLinks
            for link in soup.find_all('a',href=desiredLinks):
                A = link.get('href')
                if A not in toGetLinks:
                    if A not in crawledLinks:
                        if tmpB > 0:
                            toGetLinks.append(A)
                            tmpB -= 1

    #                        global toGetLinks
    #                        toGetLinks.append(linkList)
    else:
        needMoreLinks()

##### Get command line args and throw usage case if user f'ed up
if len(sys.argv) < 2:
	print('Usage: reCrawl.py [string - URL] [int - Breadth]')
	sys.exit()

url = str(sys.argv[1])
breadth = int(sys.argv[2])
print('Url: {u}\nBreadth: {b}\n'.format(u = url, b = breadth))

if 'www' not in url:
	url = 'www.' + str(url)
if 'https://' not in url:
	url = 'https://' + str(url)

#i = 0

crawl(url,breadth)
#print ('Crawled Links: {}\ni: {}\nlimit: {}\n'.format(len(crawledLinks), i, limit))
#print ('ToGetLinks: {}\nNextUrl: {}'.format(toGetLinksLength(), toGetLinks[i]))
while len(crawledLinks) <= limit:
    print ('Crawled Links: {}\ni: {}\nlimit: {}\n'.format(len(crawledLinks), i, limit))
    #print ('ToGetLinks: {}\nNextUrl: {}'.format(toGetLinksLength(), toGetLinks[i]))
    crawl(str(toGetLinks[i]) , breadth)
    i += 1

print('Done')

print('Got {} links from {}'.format(len(crawledLinks), url))
for x in crawledLinks:
    print (x, crawledLinks[x])

print('len crawled: {}\nlen cashed: {}'.format(len(crawledLinks), len(cashedHtml)))

for j in cashedHtml:
    print (j, crawledLinks[j], cashedHtml[j])
