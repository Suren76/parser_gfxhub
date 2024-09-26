import base64
from urllib.parse import unquote

import requests
import scrapy
from scrapy.http import Response

from gfxHUB_spider.gfxHUB_spider.items import PostItem, CategoryPostsListItem, AllDataItem
# from gfxHUB_spider.items import PostItem, CategoryPostsListItem, AllDataItem



class GfxHUBSpider(scrapy.Spider):
    name = 'scraper_gfxHUB'
    start_urls = ['https://gfx-hub.co']

    def parse(self, response: Response):
        category_tags = response.xpath("//*[@class='hidden-menu']//a[contains(@href, '3d-models')]")

        categories = [
            f"{category.xpath('.//@href').get()}"
            for category in category_tags
            # if category.xpath(".//text()").get() not in ['3D Collection', '3D-Print', '3D-Scenes', '3DSky', 'Dimensiva', 'Kitbash3D', 'Other 3D']
            # if category.xpath(".//text()").get() not in ["Full 3D-scenes", "COLLECTIONS", "3D-Print Models"]
            if category.xpath(".//text()").get() in ["3DSky"]
            # if category.xpath(".//text()").get() in ["3D-Scenes"]
        ]

        data: AllDataItem = AllDataItem()
        _category_items: list[CategoryPostsListItem] = []

        for category in categories:
            _request = scrapy.Request(category, self.parse_cards_by_category)

            _request.meta["all_data"] = data

            category_items = CategoryPostsListItem()
            category_items["category"] = list(filter(None, category.split("/")))[-1]
            category_items["posts"] = []
            _request.meta["category_items_list"] = category_items
            _category_items.append(category_items)

            yield _request

    def parse_cards_by_category(self, response: Response):
        items = response.xpath("//*[@class='navigation']//a/text()")

        last_index = items[-1].extract() if items else 1
        urls = (f'{str(response.url[:-1])}/page/{i}' for i in range(1, int(last_index)+1))

        for url in urls:
            _request = scrapy.Request(url, self.parse_page_cards_by_urls)
            yield _request

    def parse_page_cards_by_urls(self, response: Response):
        item_block_xpath = "//*[@class='main-news two three']"
        item_block_url_xpath = ".//h2//a/@href"

        for item_block in response.xpath(item_block_xpath):
            yield scrapy.Request(item_block.xpath(item_block_url_xpath).get(), self.parse_archive_download_urls_by_post_url)

    def parse_archive_download_urls_by_post_url(self, response: Response):
        post_title_xpath = "//*[@class='main-news-title']//*/text()"
        archive_link_xpath = "//*[@class='down-link-block']"
        category_text_xpath = "//*[@class='main-news-info-item']//*[contains(@*, '{}')]/text()"
        post_image_xpath = "//div[@class='full-news-content share-content']//img/@data-src"

        with_href_xpath = ".//a/@href"
        with_text_xpath = ".//text()"

        _category_from_link = list(filter(None, response.url.split("/")))[-2]

        download_links_elements = response.xpath(archive_link_xpath)
        download_links = {
            valid_url.split("//")[1].split("/")[0]: valid_url

            for valid_url in [
                base64.b64decode(unquote(url).split("url=")[1]).decode() if "do=go" in url or "/engine/" in url else url

                for url in [
                    element.xpath(with_href_xpath).get() if element.xpath(with_href_xpath) else element.xpath(with_text_xpath).get()
                    for element in download_links_elements
                ]
            ]
        }
        post_item = PostItem()

        post_item["title"] = response.xpath(post_title_xpath).get().strip()
        post_item["url"] = response.url
        post_item["category"] = response.xpath(category_text_xpath.format(_category_from_link)).get()
        post_item["download_links"] = download_links
        post_item["images"] = [f"{self.start_urls[0]}{image}" for image in response.xpath(post_image_xpath).extract()]

        size = 0

        if len(download_links) > 0:
            self.log(f"{download_links=}")
            size_request = scrapy.Request(download_links[list(download_links.keys())[0]], callback=self.get_size_of_archive)
            size_request.meta["item"] = post_item
            yield size_request
            # size = size_request

        # post_item["size"] = size

        # yield post_item

    def get_size_of_archive(self, response: Response):
        archive_size_xpath = "//*[@class='file-size']/text()"

        item = response.meta["item"]
        _size = response.xpath(archive_size_xpath).get()[1:-1]
        item["size"] = _size
        return item


