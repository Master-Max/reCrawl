import sys
import os
import re
from collections import Counter
from bs4 import BeautifulSoup


fullPath = str()
fullDirName = str()

stopWords = ['and','are','for','from','has','that','the','was','were','will','with']



class Term:
    def __init__(self, myKey, pageNum, pageLoc, rFreq):
        self.myKey = myKey
        self.pageNum = pageNum
        self.pageLoc = pageLoc
        self.rFreq = rFreq
    def getList(self):
        return str(self.pageNum) +' '+ str(self.pageLoc) +' '+ str(self.rFreq)
    def __srt__(self):
        return "member of Term"
    def __repr__(self):
        return self.getList()

def setPath(p):
    global fullPath
    fullPath = p

def getLocalPath():
    pn = str(os.path.dirname(os.path.realpath(__file__)))
    return pn

def fq(word, c):
    if word in c:
        tmpF = c[word] / len(mixedList)
        return round(tmpF,5)

def addToBigList(wd, trm):
    global bigList
    if wd in bigList.keys():
        bigList[wd].append(trm)
    else:
        trm = [trm]
        bigList.update({wd:trm})

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
print (fullPath, '\n')

dirs = os.listdir(fullPath)
toIndex = []

for f in dirs:
    if f.endswith('.pg'):
        toIndex.append(fullPath + '/' + f)


print(*toIndex, sep='\n')
toIndex.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
print('====================================')
print(*toIndex, sep='\n')
bigList = {}

for i in range(0,len(toIndex)):
    titleTerms = []
    bodyTerms = []
    with open(toIndex[i]) as inFile:
        soup = BeautifulSoup(inFile, 'lxml')

        title_tag = soup.title
        for child in title_tag.children:
            c = re.sub(r'\W+', ' ', child)
            c = c.split()
            for j in range(0,len(c)):
                titleTerms.append(c[j])

        body = soup.find('body')
        #body = body.findChildren()
        body = body.get_text()
        b = re.sub(r'\W+', ' ', body)
        b = b.split()
        for j in range(0,len(b)):
            bodyTerms.append(b[j])

    for j in range(0,len(titleTerms)):
        tT = titleTerms[j].lower()
        titleTerms[j] = tT

    for j in range(0,len(bodyTerms)):
        B = bodyTerms[j].lower()
        bodyTerms[j] = B

    for word in list(bodyTerms):
        if word in stopWords:
            bodyTerms.remove(word)
        if len(word) <= 2:
            bodyTerms.remove(word)

    mixedList = titleTerms + bodyTerms
    mixedList.sort()

    cnt = Counter()
    for word in mixedList:
        cnt[word] += 1
    print('\n',i)
    print(len(cnt), " || ", len(mixedList))



    tnt = Counter()
    for word in titleTerms:
        tnt[word] += 1

    for word in tnt:
        print(word, tnt[word])
        T = Term(word , i, 1, fq(word,cnt))
        #TT = []
        #TT.append(T)
        addToBigList(word, T)

    print('====================================')

    bnt = Counter()
    for word in bodyTerms:
        bnt[word] += 1

    for word in bnt:
        print(word, bnt[word])
        B = Term(word, i, 0, fq(word,cnt))
        #BB = []
        #BB.append(B)
        addToBigList(word, B)

##################################
#for word in bigList.keys():
#    BL = bigList[word]
#    print('\n',word)
#    for i in range(0,len(BL)):
#        L = BL[i]
#        v = str(L)
#        print(' ', v)
####################################
data = str()
#for word in bigList.keys():
#    BL = bigList[word]
#    data = '\n' + word
#    for i in range(0,len(BL)):
#        L = BL[i]
#        v = str(L)
#        data = ' ' + v

for k,v in sorted(bigList.items()):
    #print(k)
    data += '\n'+k
    for i in range(0,len(v)):
        V = v[i]
        p = str(V)
        #print(' ',p)
        data += '\n   '+p

print(data)

with open('index.dat', 'w') as tf:
    tf.write(data)
