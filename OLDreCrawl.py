import sys
import requests
from bs4 import BeautifulSoup, SoupStrainer
import re

print(sys.getrecursionlimit())

#####	Getting the command line arguments and returning Usage case if the user fucks up

if len(sys.argv) < 3:
	#print('{} is not enough arguments'.format(sys.argv))
	print('Usage: reCrawl.py [string - URL] [int - Breadth] [int - Depth]')
	sys.exit()

url = str(sys.argv[1]) #URL to go to
breadth = int(sys.argv[2]) #How Wide To Search
depth = int(sys.argv[3]) #How Deep To Search

print('Url: {u}\nBreadth: {b}\nDepth: {d}\n'.format(u = url, b = breadth, d = depth))

#####	Requesting the url

if 'www' not in url:
	url = 'www.' + str(url)
if 'https://' not in url:
	url = 'https://' + str(url)

print('Requesting: {}'.format(url))

r = requests.get(url)
r_html = r.text

soup = BeautifulSoup(r_html, 'lxml')

linkList = []

#####	Filter out links to other domains

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


#####	Finding all links on the first page

lNum = 0
for link in soup.find_all('a', href=desiredLinks):
	A = link.get('href')
#	print(A)
#	lNum +=1
	if A not in linkList:
		linkList.append(A)

print(*linkList, sep='\n')

print('linkList Length: {}'.format(len(linkList)))

if depth > 0:
	
