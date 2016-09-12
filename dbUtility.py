from pymongo import MongoClient
import datetime

#Create

def createPage(page):
  client = MongoClient()
  db = client['crawlerDB']
  pages = db['pages']
  page_id = pages.insert_one(page).inserted_id
  clint.close()
  return page_id

#Read

#Update

#Delete