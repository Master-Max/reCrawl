import sys
import requests
import re
from bs4 import BeautifulSoup

dbg = False #Set to True to Enable DeBug Mode

#linkList = [] #Global Variable that stores all links
crawledLinks = []

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

memo = {}
def crawl(url, b, d, idN):
    url = str(url)
    d = int(d)
    b = int(b)
    idN = int(idN)
    tmpB = b
    print('\nCrawling: {}'.format(url))
    print('bre: {} | dep: {}'.format(b, d))
    global crawledLinks
    #global linkList
    linkList = []
    crawledLinks.append(url)
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

    print(*linkList, sep='\n')
    #ADD to dictonary memo?

    if d > 0:
        for i in range(0, b):
            if linkList[i] not in crawledLinks:
                crawl(linkList[i], b, d-1, idN+1)
    else:
        print('Depth reached')
        continue

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

crawl(url,breadth,depth)

#print(*linkList, sep='\n')
#print('linkList Length: {}'.format(len(linkList)))

#print(*crawledLinks, sep='\n')
print('Crawled Links: {}'.format(len(crawledLinks)))
