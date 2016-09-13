import datetime
from pymongo import MongoClient

#Create

def createPage(page):
  client = MongoClient()
  db = client['crawlerDB2']
  pages = db['pages']
  page_id = pages.insert_one(page).inserted_id
  client.close()
  return page_id

#Read

def getPage(url):
  client = MongoClient()
  db = client['crawlerDB2']
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
    db = client['crawlerDB2']
    pages = db['pages']
    pages.update_one({ "url": url }, updateObj)
    client.close()

#Update

#Delete
