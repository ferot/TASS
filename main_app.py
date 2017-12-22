from WebScraper.basic_scraper import BasicScraper

def main():
    bs = BasicScraper()
    soup = bs.open_web('http://e-gory.pl/forum')
    print bs.get_forum_links(soup)

if __name__ == "__main__":
    main()