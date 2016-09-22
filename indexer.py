from dbUtility import putPage, getPage, getAllPages, getPageFromId
import time
import queue
from fetch import base
import heapq
import threading
from htmlParser import parseLink
from bs4 import BeautifulSoup
from stop_words import get_stop_words
from stemming.porter2 import stem

dictonary = {}

docId = 0

for page in getAllPages():
    termPosition = 0
    for term in page['terms']:
        termObj = dictonary.get(term)
        if(termObj is None):
            termObj = { 'docFreq': 1, 'postings': [{ 'docId': (docId, page['_id']) , 'termPositions':[termPosition] }] }
        else:
            if docId in [x['docId'][0] for x in termObj['postings']]:
                posting = [x for x in termObj['postings'] if x['docId'][0] == docId][0]
                posting['termPositions'].append(termPosition)
            else:
                termObj['postings'].append({ 'docId':(docId, page['_id']), 'termPositions':[termPosition] })
                termObj['docFreq'] += 1
        termPosition += 1
        dictonary[term] = termObj
    docId += 1


def search(text):
    res = dictonary.get(text)['postings'][:]
    if(res is None):
        return None
    else:
        res.sort(key=lambda x: len(x['termPositions']), reverse=True)
        res = [x['docId'][1] for x in res]
        return res
        
for x in search("hello"):
    print(getPageFromId(x)['url'])
