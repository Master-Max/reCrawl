import sys
import requests
from bs4 import BeautifulSoup, SoupStrainer
import re

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


#####	Finding n links on the first page, where n = breadth
#link = soup.find_all('a')

lNum = 0
for link in soup.find_all('a', href=desiredLinks):
	A = link.get('href')
#	print(A)
#	lNum +=1
	if A not in linkList:
		linkList.append(A)

print(*linkList, sep='\n')

#for link in soup.find_all('a'):
#	A = link.get('href')
#	print(A)
#	if url not in str(A):
#		continue
#	else:
#		linkList.append(A)



#	linkList.append(A)
#	if url not in 

print('def method len: {}'.format(lNum))

print('linkList Length: {}'.format(len(linkList)))

#link = soup.find_all('a'):



#for i in range(0,breadth):	
#	print(l)
#	linkList.append()


#####	Test Case

#links = soup.find_all('a')

#print('#############################\n{}'.format(links))
