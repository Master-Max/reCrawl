import httplib2
from bs4 import BeautifulSoup, SoupStrainer

http = httplib2.Http()
status, response = http.request('http://www.nytimes.com')

soup = BeautifulSoup(response, "lxml")

for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
	if link.has_attr('href'):
		print link['href']
