from dbUtility import putPage, getPage, getAllPages, getPageFromId, getTerm, createTerm, putTerm
from htmlParser import getTerms
import sys

def search(text):
    vector = {}
    resDic = {}
    terms = getTerms(text)
    termObjs = [getTerm(x) for x in terms]
    if(len(termObjs) == 0):
        return []
    else:
        termObjs = [x for x in termObjs if x is not None]
        l = [(x['term'], x['postings']) for x in termObjs]
        pairList = []
        for term, postings in l:
            for x in postings:
                pairList.append((term, getPageFromId(x['docId'][1])))
        for term, doc in pairList:
            score = doc['vector'][term]
            url = doc['url']
            currentScore = resDic[url] if url in resDic else 0
            currentScore += score
            resDic[url] = currentScore
        for x,y in resDic.items():
            page = getPage(x)
            resDic[x] = (y / page['docLen']) * page['pagerank']
        res = sorted([(y,x) for x,y in resDic.items()], reverse=True)[:5]
        return [y for x,y in res]


print(search(" ".join(sys.argv[1:])))
            

