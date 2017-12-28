import os
import random
import time
from urllib2 import URLError

import sys

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
        posts = []
        while proceed and retry_count:
            try:
                # do processing of topic's threads
                threads = self._build_link_list('topictitle')
                print "pages : {0}".format(str(len(threads)))
                posts.append(self.extract_content(threads))

                proceed = self.go_next_page()
            except URLError:
                print "Problem with connection"
                retry_count -= 1
        return posts

    def get_topics(self):
        return self._build_link_list('forumtitle')

    """Builds list of link for desired param, using current soup context"""
    def _build_link_list(self, param):
        link_list = []
        for link in self.soup.find_all('a', {'class': param}):
            thread = link.get('href')[1:]
            link_list.append(self.base_url + thread)
        return link_list

    """Obtains post content from current page"""
    def extract_content(self, threads):
        content = []
        print "in extract_content"
        for thread in threads:
            thread_nr = 0
            post_nr = 0
            page_nr = 1

            self.open_web(thread)
            print "attempt to open website : {0}".format(thread)

            thread_nr += 1
            # iterate over pages(if not single) and extract content.
            proceed = True
            while proceed:
                # WARNING this size is not truly content size it may be considered as SIZE OF REFERENCES to content
                # so threshold value is chosen arbitrarily ('real' content reffered - may be even much bigger!)
                if sys.getsizeof(content) > 1000:
                    print "sizeof content so far : {0} bytes. \n Chunking content...".format(str(sys.getsizeof(content)))

                    self.status_dict["thread_nr"] = thread_nr
                    self.status_dict["post_nr"] = post_nr

                    self._chunk_file(content, self._generate_chunk_name())
                    content = []

                for post in self.soup.find_all('div', {'class': 'content'}):
                    post_nr += 1
                    print "post  nr : {0}".format(post_nr)
                    content.append(post)
                proceed = self.go_next_page()
                if proceed:
                    page_nr += 1
                    print "proceeding page_nr : {0} of thread...".format(page_nr)

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

    @staticmethod
    def _chunk_file(item_list, chunk_name):
        directory = "./chunks/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        file = open(directory + chunk_name, 'w')
        for item in item_list:
            print >> file, item

    def _generate_chunk_name(self):
        iteration = self.status_dict["iteration"]
        thr_nr = self.status_dict["thread_nr"]
        post_nr = self.status_dict["post_nr"]

        name = "ch_i_" + str(iteration) + "_t_" + str(thr_nr) + "_p" + str(post_nr)
        return name
