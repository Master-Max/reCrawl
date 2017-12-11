import urllib
import lxml.html
import sys

if(sys)

connection = urllib.urlopen('http://www.nytimes.com')

dom = lxml.html.fromstring(connection.read())

for link in dom.xpath('//a/@href'):
	print(link)
