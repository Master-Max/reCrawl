import sys
import requests
import re
import hashlib
import os
import os.path
import time
import datetime
from pathlib import Path
from bs4 import BeautifulSoup

dbg = False
simpleNames = True

limit = 10

cashedLinks = {}
cashedHtml = {}
cashedMd5 = {}
timeStamps = {}
toGetLinks = []
BigUrl = str()
originalUrl = str()
key = 0
i = 0

##### Filestorage and the like
def properFileName(fname):
    fn = str(fname)
    if simpleNames:
        return originalUrl

    else:
        if 'http://' in fn:
            fn = fn.lstrip('http://')
        if 'https://' in fn:
            fn = fn.lstrip('https://')
        if 'www.' in fn:
            fn = fn.lstrip('www.')

        fn = fn.split('/')
        FN = fn[0] + '_'
        fn[0] = ''
        FN += ''.join(x.capitalize() for x in fn)
        print(FN)
        return FN

def saveData(fname, data, NUM):
    pathName = str(os.path.dirname(os.path.realpath(__file__)))
    toDir = '/pages'
    fDes = '.pg'

    fullDir = pathName + toDir

    fn = properFileName(fname)

    fullFileName = fullDir + '/' + fn
    if simpleNames:
        fullFileName += '_' + str(NUM)
    print(fullFileName)
    if not os.path.exists(fullDir): #Make Sure Dir exists. If not, builds dir
        os.makedirs(fullDir)

    mf = Path(str(fullFileName) + fDes) #If file already exists, renames file
    if mf.is_file():
        i = 1
        fileExists = True
        while fileExists:
            tmp = fullFileName + '_' + str(i)
            fm = Path(str(tmp) + fDes)
            if not fm.is_file():
                fullFileName = tmp
                fileExists = False
            else:
                i += 1

    fullFileName += fDes
    print('Saving: {}'.format(fullFileName))

    with open(str(fullFileName), 'w') as tf:
        tf.write(data)#TODO put in write data

    print('Saved')

##### File Structure
def makeData(k):
    k = k
    data = str()
    data += 'URL: ' + cashedLinks[k] + '\n'
    data += 'TimeStamp: ' + timeStamps[k] + '\n'
    data += 'Md5 Hash: ' + cashedMd5[k] + '\n'
    data += 'Html Line Count: ' + str(cashedHtml[k].count('\n')) + '\n'
    data += '\n==============================HTML==============================\n'
    data += cashedHtml[k]
    return data

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
    if href[-1] in ignoreVals:
        return False
    if BigUrl not in href:
        return False
    return True

def keyPlus():
    global key
    key += 1

def getTimeStamp():
    ts = time.time()
    tmpTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return tmpTime

def addAll(url, m5, p_html):
    global cashedLinks, cashedMd5, cashedHtml, timeStamps
    tmpTs = getTimeStamp()
    timeStamps.update({key: tmpTs})
    cashedLinks.update({key: url})
    cashedHtml.update({key: str(p_html)})
    cashedMd5.update({key: str(m5)})
    keyPlus()

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

    r = requests.get(url)
    r_html = r.text
    m5 = md5(r_html)

    if m5 not in cashedMd5:
        soup = BeautifulSoup(r_html, 'lxml')

        pHtml = soup.prettify()

        addAll(url, m5, pHtml)

        if toGetLinksLength() < limit:

            global toGetLinks
            for link in soup.find_all('a',href=desiredLinks):
                A = link.get('href')
                if A not in toGetLinks:
                    if A not in cashedLinks:
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

#################################################################
#    What Actually Executes
#################################################################
url = str(sys.argv[1])
originalUrl = url
breadth = int(sys.argv[2])
print('Url: {u}\nBreadth: {b}\n'.format(u = url, b = breadth))

if 'www' not in url:
    url = 'www.' + str(url)
if 'https://' not in url:
    url = 'https://' + str(url)
BigUrl = url

crawl(url,breadth)

while len(cashedLinks) <= limit:
    print ('Crawled Links: {}\ni: {}\nlimit: {}\n'.format(len(cashedLinks), i, limit))
    crawl(str(toGetLinks[i]) , breadth)
    i += 1

print('Done')

print('\nGot {} links from {}'.format(len(cashedLinks), url))

print('\nlen crawled: {}\nlen cashed: {}\n'.format(len(cashedLinks), len(cashedMd5)))

for j in cashedMd5:
    print('{}    {}\n        \nmd5: {}\n'.format(j,cashedLinks[j],cashedMd5[j]))

for i in range(0,len(cashedLinks)):
    tmpData = makeData(i)
    print('Made Data')
    saveData(cashedLinks[i], tmpData, i)
