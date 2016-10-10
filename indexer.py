from dbUtility import putPage, getPage, getAllPages, getPageFromId, getTerm, createTerm, putTerm, replacePage, updatePage
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
import numpy

dictonary = {}
UrlToDocId = {}
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
    UrlToDocId[page['url']] = docId
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


numberOfPages = docId
linkMatrix = numpy.zeros((numberOfPages, numberOfPages))
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

    # Construct the link matrix used for calculating PageRank
    outLinks = []
    numberOfOutLinks = 0
    pageId = UrlToDocId[doc['url']]
    alpha = .10
    errorMargin = 0.01
    for url in doc['links']:
        linkId = UrlToDocId.get(url, math.inf)
        if linkId < numberOfPages:
            outLinks.append(linkId)
            numberOfOutLinks += 1
    for link in outLinks:
        linkMatrix[link, pageId] = 1.0 / numberOfOutLinks
    if numberOfOutLinks is 0:       # Handles dead ends by random teleportation...
        for i in range(numberOfPages):
            linkMatrix[i, pageId] = 1.0 / numberOfPages
    # End of link matrix construction

    replacePage(doc)
    count += 1
    print(count)

# Adds random teleportation to the link matrix
transitionMatrix = (1 - alpha) * linkMatrix + numpy.full((numberOfPages, numberOfPages), alpha / numberOfPages)
qPrev = numpy.full(numberOfPages, 1.0 / numberOfPages)
error = math.inf
counter = 0
while error > errorMargin:
    qCurrent = transitionMatrix @ qPrev
    print(qCurrent)
    error = numpy.linalg.norm(qCurrent - qPrev)
    qPrev = qCurrent
    counter += 1
res = qPrev

print("Finished the while loop")
print(counter)

# Update the database with PageRank
invDict = {v: k for k, v in UrlToDocId.items()}
for i in range(numberOfPages):
    url = invDict[i]
    pageRank = {"$set": { 'pagerank': res[i] }}
    updatePage(url, pageRank)

print("Done updating database")
