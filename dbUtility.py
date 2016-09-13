import datetime
from pymongo import MongoClient

#Create

dbName = 'crawlerDB26'

def createPage(page):
  client = MongoClient()
  db = client[dbName]
  pages = db['pages']
  page_id = pages.insert_one(page).inserted_id
  client.close()
  return page_id

#Read

def getPage(url):
  client = MongoClient()
  db = client[dbName]
  pages = db['pages']
  page = pages.find_one({"url": url})
  client.close()
  return page


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
