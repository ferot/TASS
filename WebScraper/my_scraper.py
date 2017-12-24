import random
import time

from WebScraper.basic_scraper import BasicScraper

"""Wrapper for BasicScraper class.
Implements functionality with specifics of site e-gory"""
class MyScraper(BasicScraper):
    def __init__(self,url):
        BasicScraper.__init__(self, url)

    def process_topics(self):
        # flag indicating if subsequent pages of topic should be processed
        # (ofc at least should be once)
        proceed = True

        while proceed:
            # do processing of topic's page
            # for each thread get link to next page
            form = self.soup.find_all('a', {'class': 'right-box right'})
            if len(form):
                next_link = self.base_url + form[0].get('href')[1:]
                proceed = True
                self.open_web(next_link)
                time.sleep(random.uniform(0, 2))
                print next_link
            else:
                proceed = False

    def get_topics(self):
        threads = []
        for link in self.soup.find_all('a', {'class': 'forumtitle'}):
            thread = link.get('href')[1:]
            threads.append(self.base_url + thread)
        return threads
