from bs4 import BeautifulSoup
import urllib2
import time
import random

"""Class responsible for basic scrap operations.
As interface class it implements all behaviours essential for web scraping such as:
loading page, dumping outputs to file etc.
In order to provide full scraping functionality. Implementation function handlers such as
process_topics_handler
should be provided by user with specific for target-site.

Implementation of this interface demands that callback signature should use object
of this class("self") as reference for state.
"""
class BasicScraper:
    def __init__(self, url, process_topics_handler=None, get_topics_handler=None):
        self.base_url = url
        self.soup = None

        if process_topics_handler is not None:
            self.process_topics = process_topics_handler
        if get_topics_handler is not None:
            self.get_topics = get_topics_handler

        self.open_web(self.base_url)
        if self.soup is None:
            print "Couldn't init scraper!"

    """Stub for dump_tracks_to_file. Must be implemented by user."""
    def dump_tracks_to_file(self):
        pass

    """Stub for process_topics. Must be implemented by user."""
    def process_topics(self):
        pass

    """Stub for get_topics_handler. Must be implemented by user."""
    def get_topics(self):
        pass

    """Opens provided url and returns soup object for further processing.
    Note: method changes soup context."""
    def open_web(self, url):
        try:
            ref = urllib2.urlopen(url).read()
            self.soup = BeautifulSoup(ref, "lxml")  # lxml param to suppress interpreter warnings
        except urllib2.URLError:
            "Problem with connection to address : {0}".format(url)
            raise

    """Returns list of main forum topic links"""
    def get_forum_links(self):
        threads = []
        if self.soup:
            threads = self.get_topics()
        return threads

    """Extracts and returns content of posts for each of thread provided as input param"""
    def get_posts_content(self, topics):
        print "Number of topics to process : " + str(len(topics))
        iter = 0
        for topic in topics:
            iter+=1
            print "iteration nr : " + str(iter)
            # for each forum-topic we have new soup context
            self.open_web(topic)
            if self.process_topics is not None:
                self.process_topics()  # trigger processing handler

            # sleep to avoid server overloading
            time.sleep(random.uniform(0, 2))
