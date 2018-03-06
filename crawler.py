import re
import queue
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

class Crawler():
  
  def __init__(self, links=None):
    if links is None:
        links = []
    self.links = links
    self._old_links = []
    self.q = queue.Queue()
    if links is not None:
      for link in links:
        self.q.put(link)
  
  def getLinks(self, link):
    req = Request(link)
    try:
      html_page = urlopen(req)
      soup = BeautifulSoup(html_page, 'html5lib')
      for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        if link not in self._old_links:
          self.q.put(link.get('href'))
          print(link.get('href'))
    except HTTPError as e:
      print('Error code: ', e.code)
    except URLError as e:
      print('Reason: ', e.reason)
    except Exception:
      print('good!')
  
  def crawlLinks(self):
    while not self.q.empty():
      link = self.q.get()
      if link not in self._old_links:
        self._old_links.append(link)
      self.getLinks(link)