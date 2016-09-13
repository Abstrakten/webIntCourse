from fetch import getPage
from fetch import base
from bs4 import BeautifulSoup
import urltools
import os

goodFileEndings = ['html', 'htm', 'php', '', 'shtml', 'shtm', 'asp', 'php3', 'cgi']

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
      return {'url': url, 'html': soup.get_text(), 'links': arr3}
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

