import datetime
from pymongo import MongoClient

#Create

# 48 5
dbName = 'crawlerDB51'
termDbName = "terms7"

client2 = MongoClient()
db2 = client2[dbName]
terms = db2[termDbName]

client3 = MongoClient()
db3 = client3[dbName]
pages3 = db3['pages']


def createPage(page):
  client = MongoClient()
  db = client[dbName]
  pages = db['pages']
  page_id = pages.insert_one(page).inserted_id
  client.close()
  return page_id

def createTerm(termObj):
  termId = terms.insert_one(termObj).inserted_id
  return termId

#Read

def getPage(url):
  client = MongoClient()
  db = client[dbName]
  pages = db['pages']
  page = pages.find_one({"url": url})
  client.close()
  return page

def getTerm(term):
  client = MongoClient()
  db = client[dbName]
  terms = db[termDbName]
  term = terms.find_one({'term': term})
  client.close()
  return term

def getPageFromId(postId):
    client = MongoClient()
    db = client[dbName]
    pages = db['pages']
    page = pages.find_one({"_id": postId})
    client.close()
    return page

def replacePage(page):
    url = page['url']
    pages3.replace_one({"url": url}, page)

def putPage(page):
  url = page['url']
  pageFromDb = getPage(url)
  if(pageFromDb == None):
    createPage(page)
  else:
    updateObj = {"$set": { 'stamp': page['stamp'], 'html': page['html'] }}
    client = MongoClient()
    db = client[dbName]
    pages = db['pages']
    pages.update_one({ "url": url }, updateObj)
    client.close()

def putTerm(termObj):
    term = termObj[termDbName]
    termFromDb = getTerm(term)
    if(termFromDb == None):
        createTerm(termObj)
    else:
        updateObj = termObj
        client = MongoClient()
        db = client[dbName]
        terms = db[termDbName]
        terms.replace_one({"term": term}, updateObj)
        client.close()

def getAllPages():
    client = MongoClient()
    db = client[dbName]
    pages = db['pages']
    pag = pages.find()
    client.close()
    res = []
    for x in pag:
      res.append(x)
    return res

#Update

#Delete
