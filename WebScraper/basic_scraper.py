from bs4 import BeautifulSoup
import urllib2

"""Class responsible for basic scrap operations"""
class BasicScraper:
    def __init__(self):
        pass

    """Opens provided url and returns soup object for further processing"""
    def open_web(self, url):
        ref = urllib2.urlopen(url).read()
        return BeautifulSoup(ref, "lxml")

    """Returns list of forum thread links"""
    def get_forum_links(self, soup):
        threads = []
        for link in soup.find_all('a'):
            cls = link.get('class')
            if cls is not None:
                    if cls[0] == 'forumtitle':
                        threads.append(link.get('href'))
        return threads
