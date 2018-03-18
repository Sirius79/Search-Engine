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
        
  def getKeys(self, link):
    req = Request(link)
    try:
      if link not in self.old_links:
        html_page = urlopen(req)
        soup = BeautifulSoup(html_page, 'html5lib')
        client = MongoClient('localhost', 27017)
        db = client['keywords']
        collection = db.test['keys']
        meta = soup.findAll('meta')
        for tag in meta:
          if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['keywords']:
            keys = tag.attrs['content'].split(',')
            for i in keys:
              if i.lower() not in self.keywords:
                self.keywords[i.lower()] = list()
                new = i.replace('.','*')
                db.keys.insert({'keyword':new.lower()} , {'site': []})
              if link not in self.keywords[i.lower()]:
                self.keywords[i.lower()].append(link)
                new = i.replace('.','*')
                db.keys.update_one({'keyword':new.lower()},{'$push' : {'site':link}})
        title = soup.findAll('title')
        for tag in title:
          tilt = tag.string
          words = tilt.split()
          if words[0].lower() not in self.keywords:
            self.keywords[words[0].lower()] = list()
            new = words[0].replace('.','*')
            db.keys.insert({'keyword':new.lower()} , {'site': []})
          if link not in self.keywords[words[0].lower()]:
            self.keywords[words[0].lower()].append(link)
            new = words[0].replace('.','*')
            db.keys.update_one({'keyword':new.lower()},{'$push' : {'site':link}})
        print(self.keywords)

    except HTTPError as e:
      print('Error code: ', e.code)
    except URLError as e:
      print('Reason: ', e.reason)
    '''except Exception:
      print('good!')'''
  
  def getLinks(self, link):
    req = Request(link)
    try:
      html_page = urlopen(req)
      soup = BeautifulSoup(html_page, 'html5lib')
      for li in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        if li.get('href') not in self.old_links:
          self.q.put(li.get('href'))
      self.getKeys(link)
    except HTTPError as e:
      print('Error code: ', e.code)
    except URLError as e:
      print('Reason: ', e.reason)
    '''except Exception:
      print('good!')'''
  
  def crawlLinks(self):
    while not self.q.empty():
      link = self.q.get()
      if link not in self.old_links:
        self.getLinks(link)
        self.old_links.append(link)
        print('\n'+ link + '\n')

crawler = Crawler(["http://www.walmart.com"])
crawler.crawlLinks()

