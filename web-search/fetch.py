import urllib.robotparser
import requests
import time

def getPage(url):
    try:
      if(not url[0:4] == "http"):
        url = "http://" + url
      if(checkRobot(url)):
        headers = {
            'User-Agent': 'awsomeBot',
        }
        page = requests.get(url, headers=headers, timeout=5.00)
        if(page.status_code == requests.codes.ok):
            return page.text
        else:
            return None
      else:
        return None
    except:
      return None

def checkRobot(url):
  robotUrl = getRobot(url)
  rp = urllib.robotparser.RobotFileParser()
  rp.set_url(robotUrl)
  rp.read()
  return rp.can_fetch("awsomeBot", url)

def base(url):
  st = ""
  if(not (url[0:7] == "http://" or url[0:8] == "https://")):
    url = "http://" + url
  i = 0
  for x in url:
    st += x
    if(x == "/"):
      i += 1
      if(i == 3):
        return st[:-1]
  return st

def getRobot(url):
  return base(url) + "/robots.txt"

