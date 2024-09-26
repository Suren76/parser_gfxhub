from pathlib import Path

from scrapy.crawler import CrawlerProcess

from .gfxHUB_spider.spiders.gfxHub2_spider import GfxHUBSpider
# from gfxHUB_spider.spiders.gfxHub2_spider import GfxHUBSpider


def run_parser(_path_to_file: Path):
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                str(_path_to_file): {"format": "json"},
            },
        }
    )

    process.crawl(GfxHUBSpider)
    process.start()

    # from scrapy.cmdline import execute
    # execute("scrapy crawl scraper_yo_3 -o result_scraper_yo_3__6_empty.json".split())

# if __name__ == '__main__':
#     run_parser("/home/suren/Projects/upwork/maroz/parser_gfxHub/resources/items_1.json")