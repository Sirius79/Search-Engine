import re
import queue
import os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

class Crawler():
  
  def __init__(self, links=None):
    if links is None:
        links = []
    self.links = links
    self.old_links = []
    self.q = queue.Queue()
    if links is not None:
      for link in links:
        self.q.put(link)
  
  def getLinks(self, link):
    req = Request(link)
    try:
      html_page = urlopen(req)
      soup = BeautifulSoup(html_page, 'html5lib')
      for _link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        if _link not in self.old_links:
          self.q.put(_link.get('href'))
    except HTTPError as e:
      print('Error code: ', e.code)
    except URLError as e:
      print('Reason: ', e.reason)
    except Exception:
      print('Ignore')
  
  def crawlLinks(self):
    while not self.q.empty():
      link = self.q.get()
      if link not in self.old_links:
        self.old_links.append(link)
        self.getLinks(link)
      else:
        continue
      print("Links visted: " + str(len(self.old_links)))
