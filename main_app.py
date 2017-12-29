from WebScraper.egory_scraper import EgoryScraper


def main():

    base_url = 'http://e-gory.pl/forum'

    ms = EgoryScraper(base_url)
    threads = ms.get_forum_links()
    ms.get_posts_content(threads)

if __name__ == "__main__":
    main()
