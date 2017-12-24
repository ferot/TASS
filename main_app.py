
from WebScraper.basic_scraper import BasicScraper
from WebScraper.my_scraper import MyScraper


def main():

    base_url = 'http://e-gory.pl/forum'
    
    ms = MyScraper(base_url)
    threads = ms.get_forum_links()
    ms.get_posts_content(threads)

if __name__ == "__main__":
    main()
