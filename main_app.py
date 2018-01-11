import threading
import sys
import Common
from WebScraper.egory_scraper import EgoryScraper
from WebScraper.travelman_scraper import TravelManScraper
from DataEngine.processing_engine import ProcessingEngine

# Number of threads for multithreading support.
# Note : for current version didn't observe any sync issues,
# but it's recommended to take it into account if any bug occurs.
thread_nr = 4


def web_scrape(scraper_type, url):
    scraper_instance = scraper_type(url)

    threads = scraper_instance.get_forum_links()
    scraper_instance.get_posts_content(threads)


class ScrapeThread (threading.Thread):
    def __init__(self, scraper_type, url):
        self.scraper = scraper_type
        self.url = url
        self.callback = web_scrape
        threading.Thread.__init__ (self)

    def run(self):
        print "Starting " + self.name
        self.callback(self.scraper, self.url)


def main():

    webscraping_enabled = ""
    if len(sys.argv) > 1:
        webscraping_enabled = sys.argv[1]

    Common.init()
    egory = True
    travelman = True

    egory_url = 'http://e-gory.pl/forum'
    travelman_url = 'http://travelmaniacy.pl/forum'

    if "ws" in webscraping_enabled:
        print "Starting webscraping..."
        if thread_nr > 1:
            print "Multithreading support enabled..."

            if egory:
                eg_thr = ScrapeThread(EgoryScraper, egory_url)
                eg_thr.start()
            if travelman:
                trv_thr = ScrapeThread(TravelManScraper, travelman_url)
                trv_thr.start()

            eg_thr.join()
            trv_thr.join()

        else:
            web_scrape(EgoryScraper, egory_url)
            web_scrape(TravelManScraper, travelman_url)

        print "Finished scraping..."
    else:
        print "Skipping webscraping..."

    pe = ProcessingEngine('chunks/*/ch_*', thread_nr)
    pe.start_processing()

    print "Exitting main app..."



if __name__ == "__main__":
    main()
