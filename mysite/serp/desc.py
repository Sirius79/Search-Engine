import re
import queue
import urllib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import os
from bs4 import BeautifulSoup
import PIL.Image
import numpy as np
from IPython.display import Image
import pymongo
from pymongo import MongoClient

class serp():

    def __init__(self, links=[]):
        self.links = links
        self.og_description = ''
        self.og_title = ''
        self.description = ''
        self.descriptions = []
        self.titles = []

    def getDescription(self, link):

        html_page = urllib.request.urlopen(link)
        soup = BeautifulSoup(html_page, 'html5lib')

        # get og description of site
        o_desc = soup.find('meta', property="og:description")
        if o_desc:
            self.og_description = o_desc["content"]

        # get og title of site
        o_title = soup.find('meta', property="og:title")
        if o_title:
            self.og_title = o_title["content"]

        # get description of site
        desc = soup.find('meta', attrs={'name': 'description'})
        if desc:
            self.description = desc["content"]

        if len(self.og_description) > len(self.description):
            return self.og_title, self.og_description
        else:
            return self.og_title, self.description

    def Descriptions(self):
        for link in self.links:
            tit, temp_des = self.getDescription(link)
            self.descriptions.append(temp_des)
            self.titles.append(tit)

        return self.titles, self.descriptions