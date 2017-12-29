from urllib2 import URLError
import sys

from WebScraper.basic_scraper import BasicScraper


"""Wrapper for BasicScraper class.
Implements functionality with specifics of site travelmaniacy.pl"""


class TravelManScraper(BasicScraper):
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
                threads = self._build_link_list('viewtopic')
                print threads
                print "pages : {0}".format(str(len(threads)))
                self.extract_content(threads)

                proceed = self._go_next_page()
            except URLError:
                print "Problem with connection"
                retry_count -= 1

    """Getting main topics as reference point to further processing"""
    def get_topics(self):
        return self._build_link_list("viewforum")

    """Builds list of link for desired param, using current soup context"""
    def _build_link_list(self, param):
        link_list = []
        for link in self.soup.find_all('a'):
            thread = link.get('href')
            # 'pid' links refer to 'recently added post. ommit them
            if param in thread and not 'pid' in thread:
                # This check refers to situation when that links :viewtopic.php?id=3241 viewtopic.php?id=3241&p=1
                # point to the same thread. To avoid double adding same link, below filtering is made
                if len(link_list):
                    prev_id, prev_page = self.get_link_page_attrs(link_list[-1])
                    cur_id, cur_page = self.get_link_page_attrs(thread)

                    if cur_id == prev_id and prev_page is None and cur_id is not None:
                        link_list = link_list[:-1]

                link_list.append(self.base_url + '/' + thread)
        return link_list

    """Obtains post content from current page. Iterates recursively over forum (sub-)threads"""
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

                for post in self.soup.find_all('div', {'class': 'postmsg'}):
                    post_nr += 1
                    print "post  nr : {0}".format(post_nr)

                    post_content = self.clean_html(post.text)
                    content.append(post_content)
                    # special char for posts separation and easier parsing
                    content.append("---------------------------------------------------")

                proceed = self._go_next_page()
                if proceed:
                    page_nr += 1
                    print "proceeding page_nr : {0} of thread...".format(page_nr)

    """Method responsible for possibly moving into next page of current soup context.
    Note - modifies that context !"""
    def _go_next_page(self):
        # get link to next page
        next_page_links = self._build_link_list('viewforum')
        # viewforum.php?id = 8 & p = 2

        for link in next_page_links:
            if '\&p=' in link:
                next_page_link = link
                proceed = True

                self.open_web(next_page_link)
                return proceed  # As soon as we get next_page link return to processing
            else:
                # last page of topic or single page of threads(no 'next' button)
                proceed = False
        return proceed

    def get_link_page_attrs(self, link):
        ID = None
        page = None
        full_id = link.split("id=")[1]
        if full_id is not None:
            if '&p=' in full_id:
                split_list = full_id.split('&p=')
                ID = split_list[0]
                page = split_list[1]
            else:
                ID = full_id
        return ID, page
