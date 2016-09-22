from fetch import getPage
from fetch import base
from bs4 import BeautifulSoup
import urltools
import os
from stop_words import get_stop_words
from stemming.porter2 import stem
import string

goodFileEndings = ['html', 'htm', 'php', '', 'shtml', 'shtm', 'asp', 'php3', 'cgi']

stop_words = get_stop_words('en')

special = "-_,.:%&()\';#!?"
valid = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') | set(special)

translation_table = dict.fromkeys(map(ord, special), None)

def testSpecial(s):
    return set(s).issubset(valid)

def clearHtml(html):
    soup = BeautifulSoup(html.lower(), 'html.parser')
    to_extract = soup.findAll(lambda tag: tag.name == "script" or tag.name == "style")
    for item in to_extract:
        item.extract()
    cleanText = soup.text
    terms = cleanText.split()
    terms = [stem(x).translate(translation_table) for x in terms if (x not in stop_words) and testSpecial(x)]
    return terms


def parseLink(url): #be aware example.com is malformed 
  arr = []
  baseUrl = base(url)
  page = getPage(url)
  if(page is not None):
      soup = BeautifulSoup(page, 'html.parser')
      for x in soup.find_all('a'):
        link = x.get('href')
        if(link is not None and link[0:4] == "http"):
          arr.append(link)
        elif(link is not None and len(link) >= 1 and link[0] == "/"):
          arr.append(baseUrl + link)
        elif(link is not None and link[0:4] == "www."):
          arr.append("http://" + link)
      arr2 = [urltools.normalize(x) for x in arr]
      arr3 = [transform(x) for x in arr2 if checkLinkStr(x)]
      terms = clearHtml(page)
      if(terms == None):
          return None
      return {'url': url, 'html': page, 'links': arr3, 'terms': terms, 'title': soup.title.text if(soup.title is not None) else "" }
  return None

def checkLinkStr(url):
    filename, file_extension = os.path.splitext(url)
    if file_extension in goodFileEndings:
        return True
    if " " in filename:
        return False
    return False

def transform(url):
    if(url[-1] == '/'):
        return url[:-1]
    return url


