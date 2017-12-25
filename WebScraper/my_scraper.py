import random
import time

from WebScraper.basic_scraper import BasicScraper


"""Wrapper for BasicScraper class.
Implements functionality with specifics of site e-gory"""


class MyScraper(BasicScraper):
    def __init__(self, url):
        BasicScraper.__init__(self, url)

    def process_topics(self):
        # flag indicating if subsequent pages of topic should be processed
        # (ofc at least should be once)
        proceed = True

        while proceed:
            # do processing of topic's page
            print self._build_link_list('topictitle')
            # get link to next page
            form = self._build_link_list('right-box right')
            if len(form):
                next_page_link = form[0]
                proceed = True

                self.open_web(next_page_link)
                time.sleep(random.uniform(0, 2))
            else:
                # last page of topic or single page of threads(no 'next' button)
                proceed = False

    def get_topics(self):
        return self._build_link_list('forumtitle')

    """Builds list of link for desired param, using current soup context"""
    def _build_link_list(self, param):
        link_list = []
        for link in self.soup.find_all('a', {'class': param}):
            thread = link.get('href')[1:]
            link_list.append(self.base_url + thread)
        return link_list
