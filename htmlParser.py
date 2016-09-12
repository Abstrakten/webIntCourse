from fetch import getPage
from fetch import base
from bs4 import BeautifulSoup
import urltools

def parseLink(url): #be aware example.com is malformed 
  arr = []
  baseUrl = base(url)
  soup = BeautifulSoup(getPage(url), 'html.parser')
  for x in soup.find_all('a'):
    link = x.get('href')
    if(link[0:4] == "http"):
      arr.append(link)
    elif(link[0] == "/"):
      arr.append(baseUrl + link)
    elif(link[0:4] == "www."):
      arr.append("http://" + link)
  arr2 = [urltools.normalize(x) for x in arr]
  return {'url': url, 'html': soup, 'links': arr2}

  