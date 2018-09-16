import re
import queue
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import os
from bs4 import BeautifulSoup
import PIL.Image
import numpy as np
from IPython.display import Image
import pymongo
from pymongo import MongoClient

class Crawler():
  
  def __init__(self, links=None):
    if links is None:
        links = []
    self.links = links
    self.old_links = []
    self.keywords = {}
    self.q = queue.Queue()
    if links is not None:
      for link in links:
        self.q.put(link)

  
  def getLinks(self,i,link,j):
    req = Request(link)
    try:
      html_page = urlopen(req)
      soup = BeautifulSoup(html_page, 'html5lib')
      client = MongoClient('localhost', 27017)
      db = client['new']
      collection = db.test['test']
      count = 0
      for li in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        count+=1
      if j==1:
        db.keys.insert({'keyword':i ,'count': [count],'site': [link]})
      else:
        db.keys.update_one({'keyword':i},{'$push' : {'site':link}})
        db.keys.update_one({'keyword':i},{'$push' : {'count':count}})
    except HTTPError as e:
      print('Error code: ', e.code)
    except URLError as e:
      print('Reason: ', e.reason)
    '''except Exception:
      print('good!')'''
  
  def crawlLinks(self):
    j = 1
    while not self.q.empty():
      link = self.q.get()
      self.getLinks('vanilla',link,j)
      j+=1

#crawler = Crawler(["https://en.wikipedia.org/wiki/Vanilla","http://www.geniuskitchen.com/about/vanilla-350","https://www.smithsonianmag.com/science-nature/bittersweet-story-vanilla-180962757/"])
#crawler.crawlLinks()

import numpy as np

matrix = np.random.rand(6, 6)
print(matrix)
np.fill_diagonal(matrix, 0)
print(matrix)
partition = np.sum(matrix, axis=0)
matrix = np.divide(matrix, partition)

print(matrix)