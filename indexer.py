from dbUtility import putPage, getPage, getAllPages, getPageFromId, getTerm, createTerm, putTerm, replacePage
import time
import queue
from fetch import base
import heapq
import threading
from htmlParser import parseLink
from bs4 import BeautifulSoup
from stop_words import get_stop_words
from stemming.porter2 import stem
import math

dictonary = {}
docId = 0

allPages = getAllPages()
docCount = len(allPages)

for page in allPages:
    termPosition = 0
    for term in page['terms']:
        termObj = dictonary.get(term)
        if(termObj is None):
            termObj = { 'term': term, 'docFreq': 1, 'postings': [{ 'docId': (docId, page['_id']) , 'termPositions':[termPosition] }] }
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

for term,termObj in dictonary.items():
    totalCount = 0
    for x in termObj['postings']:
        x['termFreq'] = len(x['termPositions'])
        x['termLogFreq'] = 1 + math.log(x['termFreq'], 10)
        totalCount += x['termFreq']
    termObj['totalTermFreq'] = totalCount
    termObj['idf'] = math.log(docCount/termObj['docFreq'], 10)
    createTerm(termObj)
    dictonary[term] = termObj


count = 0
for doc in allPages:
    doc['vector'] = {}
    for term in doc['terms']:
        termObj = dictonary[term]
        posting = [x for x in termObj['postings'] if str(x['docId'][1]) == str(doc['_id'])][0]
        idf = termObj['idf']
        termLog = posting['termLogFreq']
        key = term
        value = idf * termLog
        doc['vector'][key] = value
    docLen = math.sqrt(sum([x[1]*x[1] for x in doc['vector'].items()]))
    doc['docLen'] = docLen
    for key,value in doc['vector'].items():
        doc['vector'][key] = value / docLen
    replacePage(doc)
    count += 1
    print(count)

