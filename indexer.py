import sys
import os
import re
from bs4 import BeautifulSoup


fullPath = str()
fullDirName = str()

def setPath(p):
    global fullPath
    fullPath = p

def getLocalPath():
    pn = str(os.path.dirname(os.path.realpath(__file__)))
    return pn

class Term:
    def __init__(self, myKey, pageNum, pageLoc, rFreq):
        self.myKey = myKey
        self.pageNum = pageNum
        self.pageLoc = pageLoc
        self.rFreq = rFreq

##### Command Line
if len(sys.argv) < 2:
    print('Usage: indexer.py [options] [string - Directory]')
    sys.exit()

tmpD = str()
if '-' in sys.argv[1]:
    if 'l' in sys.argv[1]:
        tmpP = str(getLocalPath()) + '/' + str(sys.argv[2])
    else:
        tmpP = str(sys.argv[2])
else:
    tmpP = str(argv[1])

setPath(tmpP)
print (fullPath)

dirs = os.listdir(fullPath)
print(dirs)
toIndex = []

for f in dirs:
    if f.endswith('.pg'):
        toIndex.append(fullPath + '/' + f)

print(*toIndex, sep='\n')
toIndex = sorted(toIndex)
print('====================================')
print(*toIndex, sep='\n')
#toIndex.sort()
#print('====================================')
#print(*toIndex, sep='\n')
bigList = {}

for i in range(0,len(toIndex)):
    titleTerms = []
    bodyTerms = []
    lilList = {}
    with open(toIndex[i]) as inFile:
        soup = BeautifulSoup(inFile, 'lxml')

        title_tag = soup.title
        for child in title_tag.children:
            c = re.sub(r'\W+', ' ', child)
            c = c.split()
            for j in range(0,len(c)):
                titleTerms.append(c[j])

        body_tag = soup.body
        for text in body_tag.string:
            c = re.sub(r'\W+', ' ', child)
            c = c.split()
            for j in range(0,len(c)):
                bodyTerms.append(c[j])

    titleTerms.sort()
    bodyTerms.sort()

    print(*titleTerms, sep='\n')
    print(*bodyTerms, sep='\n')

    for t in range(0,len(titleTerms)):
        T = Term(titleTerms[t], i, 1, 0.000)
    for b in range(0,len(bodyTerms)):
        T = Term(bodyTerms[b], i, 1, 0.000)
