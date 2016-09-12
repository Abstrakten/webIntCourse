import dbUtility
import time
import queue
from fetch import base
import heapq

seed = "http://www.reddit.com"
pageCount = 1000
backQueueCount = 0
hitDelay = 2

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
  print(frontQueue.qsize())
  if(not frontQueue.empty()):
    url = frontQueue.get()[1]
    baseUrl = base(url)
    if(backQueue.get(baseUrl) == None):
      backQueue[baseUrl] = queue.Queue().put(url)
    else:
      backQueue[baseUrl].put(url)
    if baseUrl not in backHeap:
      heapq.heappush(backHeap,(int(time.time())+hitDelay,baseUrl))


def getFromBackQueue():
  time.sleep(2)
  if not backHeap:
    frontQueueSelector()
    return getFromBackQueue()
  else:
    target = heapq.heappop(backHeap)
    print(target)
    if(target[0] > int(time.time())):
      heapq.heappush(backHeap,target)
      frontQueueSelector()
      return getFromBackQueue()
    else:
      result = backQueue.get(target[1])
      if(not result == None):
        result = result.get()
      if(result == None):
        del backQueue[target[1]]
        return getFromBackQueue()
      else:
        return result


addToQueue(seed)

currentCount = 0

targetPage = getFromBackQueue()

print (targetPage)

#while(pageCount > currentCount):
#  currentCount += 1


