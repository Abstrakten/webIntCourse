#import requests
#import robotparser



def getRobot(url):
  st = ""
  if(not (url[0:7] == "http://" or url[0:8] == "https://")):
    url = "http://" + url
  i = 0
  for x in url:
    st += x
    if(x == "/"):
      i += 1
      if(i == 3):
        return st + "robots.txt"
  return st + "/robots.txt"