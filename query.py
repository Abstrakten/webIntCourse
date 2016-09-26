from dbUtility import putPage, getPage, getAllPages, getPageFromId, getTerm, createTerm, putTerm
import time
import queue
from fetch import base
import heapq
import threading
from htmlParser import parseLink, getTerms
from bs4 import BeautifulSoup
from stop_words import get_stop_words
from stemming.porter2 import stem
from dbUtility import getPageFromId, getTerm, getPage
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
            resDic[x] = y/getPage(x)['docLen']
        res = sorted([(y,x) for x,y in resDic.items()], reverse=True)[:5]
        return [y for x,y in res]


print(search(" ".join(sys.argv[1:])))
            

