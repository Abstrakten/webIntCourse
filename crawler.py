from dbUtility import putPage, getPage, getAllPages
import time
import queue
from fetch import base
import heapq
import threading
from htmlParser import parseLink
 
seed = "http://www.reddit.com"
pageCount = 1000
backQueueCount = 0
hitDelay = 1

numThreads = 0
maxThreads = 10
threads = []

frontQueue = queue.PriorityQueue()
backQueue = {}
backHeap = []   

lock = threading.Lock()
lock2 = threading.Lock()

def addToQueue(url):
  if(len(url) < 30):
    frontQueue.put((0,url))
  elif(len(url) < 50):
    frontQueue.put((1,url))
  elif(len(url) < 100):
    frontQueue.put((2,url))
  else:
    frontQueue.put((3,url))

def frontQueueSelector():
  if(not frontQueue.empty()):
    url = frontQueue.get()[1]
    baseUrl = base(url)
    if(backQueue.get(baseUrl) == None):
      backQueue[baseUrl] = queue.Queue()
      backQueue[baseUrl].put(url)
    else:
      backQueue[baseUrl].put(url)
    if baseUrl not in [x[1] for x in backHeap]:
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


def start():
    global backQueueCount
    while(backQueueCount < pageCount):
        lock.acquire()
        targetPageUrl = getFromBackQueue()
        lock.release()
        if(targetPageUrl is not None):
            dbPage = getPage(targetPageUrl)
            if((dbPage is None) or ((dbPage['stamp'] + 864000) < int(time.time()) and dbPage['canSee'])):
                page = parseLink(targetPageUrl)
                if(page is not None):
                    storePage = {'stamp': int(time.time()), 'html': page['html'], 'url': targetPageUrl, 'canSee':True }
                    putPage(storePage)
                    for x in page['links']:
                        addToQueue(x)
                    lock2.acquire()
                    backQueueCount += 1
                    lock2.release()
                    print(str(backQueueCount) + ": " + targetPageUrl)
                else:
                    storePage = {'stamp': int(time.time()), 'html': "", 'url': targetPageUrl, 'canSee': False }
        else:
            break

    print("no more to search")

class crawler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())

    def run(self):
        start()

    def pause(self):
        self.paused = True
        self.pause_cond.acquire()

    def resume(self):
        self.paused = False
        self.pause_cond.notify()
        self.pause_cond.release()

addToQueue(seed)

for x in range(0, maxThreads):
    threads.append({ 'started': False, 'thread': crawler() })

def main():
    global numThreads
    while True:
        backCount = int(len(backQueue.keys()))
        thd = int(backCount/3)
        thd = 1 if (thd == 0) else thd
        thd = maxThreads if (thd > maxThreads) else thd
        if(numThreads < thd):
            thread = threads[numThreads]
            if(thread['started']):
                thread['thread'].resume()
            else:
                thread['thread'].start()
            numThreads += 1
            print("number of threads: " + str(numThreads) + ", number of back queues: " + str(backCount))
        if(numThreads > thd):
            numThreads -= 1
            print("number of threads: " + str(numThreads) + ", number of back queues: " + str(backCount))
            thread = threads[numThreads]
            thread['thread'].pause()

mainThread = threading.Thread(target=main)
mainThread.start()
