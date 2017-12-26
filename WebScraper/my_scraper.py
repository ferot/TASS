import random
import time
from urllib2 import URLError

from WebScraper.basic_scraper import BasicScraper


"""Wrapper for BasicScraper class.
Implements functionality with specifics of site e-gory"""


class MyScraper(BasicScraper):
    def __init__(self, url):
        BasicScraper.__init__(self, url)

    """Method responsible for extracting posts content for each topic"""
    def process_topics(self):
        # flag indicating if subsequent pages of topic should be processed
        # (ofc at least should be once)
        proceed = True

        # max number of failures
        retry_count = 10

        while proceed and retry_count:
            try:
                # do processing of topic's page
                posts = self._build_link_list('topictitle')
                print self.get_post_content(posts)
                proceed = self.go_next_page()
            except URLError:
                print "Problem with connection"
                retry_count -= 1

    def get_topics(self):
        return self._build_link_list('forumtitle')

    """Builds list of link for desired param, using current soup context"""
    def _build_link_list(self, param):
        link_list = []
        for link in self.soup.find_all('a', {'class': param}):
            thread = link.get('href')[1:]
            link_list.append(self.base_url + thread)
        return link_list

    """Obtains post from current page"""
    def get_post_content(self, threads):
        content = []
        for thread in threads:
            self.open_web(thread)
            for post in self.soup.find_all('div', {'class': 'content'}):
                content.append(post)
        return content

    def go_next_page(self):
        # get link to next page
        form = self._build_link_list('right-box right')
        if len(form):
            next_page_link = form[0]
            proceed = True

            self.open_web(next_page_link)
        else:
            # last page of topic or single page of threads(no 'next' button)
            proceed = False
        return proceed
