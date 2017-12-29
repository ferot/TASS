from WebScraper.egory_scraper import EgoryScraper
from WebScraper.travelman_scraper import TravelManScraper


def main():

    egory = False
    travelman = True

    if egory:
        base_url = 'http://e-gory.pl/forum'

        ms = EgoryScraper(base_url)
        threads = ms.get_forum_links()
        ms.get_posts_content(threads)
    if travelman:
        base_url = 'http://travelmaniacy.pl/forum'

        ms = TravelManScraper(base_url)
        threads = ms.get_forum_links()
        # print threads
        ms.get_posts_content(threads)

if __name__ == "__main__":
    main()
