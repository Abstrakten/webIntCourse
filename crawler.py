import dbUtility
import time
import queue
from fetch import base
import heapq

seed = "http://www.reddit.com"
pageCount = 1000
backQueueCount = 0
hitDelay = 1

frontQueue = queue.PriorityQueue()
backQueue = {}
backHeap = []

def addToQueue(url):
  if(len(url) < 30):
    frontQueue.put((0,url))
  elif(len(url) < 50):
    frontQueue.put((1,url))
  elif(len(url) < 100):
    frontQueue.put((2,url))
  else:
    frontQueue.put((3,url))

#TODO add cleanup functionality

# def backQueueRouter():
#   while(True):
#     if(not frontQueue.empty()):
#       url = frontQueue.pop()
#       baseUrl = base(url)
#       if(backQueue.get(baseUrl) == None):
#         backQueue[baseUrl] = [url]
#       else
#         backQueue[baseUrl].append(url)

def frontQueueSelector():
  if(not frontQueue.empty()):
    url = frontQueue.get()[1]
    baseUrl = base(url)
    if(backQueue.get(baseUrl) == None):
      backQueue[baseUrl] = queue.Queue()
      backQueue[baseUrl].put(url)
    else:
      backQueue[baseUrl].put(url)
    if baseUrl not in backHeap:
      heapq.heappush(backHeap,(int(time.time())+hitDelay,baseUrl))
    return True
  return False


def getFromBackQueue():
  while(not backHeap):
    status = frontQueueSelector()
    if(not status):
      return None
  target = heapq.heappop(backHeap)
  while(target[0] > int(time.time())):
    heapq.heappush(backHeap,target)
    frontQueueSelector()
    target = heapq.heappop(backHeap)
  result = backQueue.get(target[1])
  if(not result == None):
    result = result.get()
  if(result == None):
    del backQueue[target[1]]
    return getFromBackQueue()
  else:
    return result


addToQueue(seed)

targetPage = getFromBackQueue()

print (targetPage)

