import base64
from urllib.parse import unquote

import scrapy
from scrapy.http import Response

from gfxHUB_spider.items import PostItem, CategoryPostsListItem, AllDataItem



class TestScraperSpider(scrapy.Spider):
    name = 'scraper_yo_2'
    start_urls = ['https://gfx-hub.cc']

    def parse(self, response: Response):
        category_tags = response.xpath("//div[@class='hidden-menu']//a[contains(@href, '3d-models')]")

        categories = [
            f"{self.start_urls[0]}{category.xpath('.//@href').get()}"
            for category in category_tags
            # if category.xpath(".//text()").get() not in ["Full 3D-scenes","Architecture","Exterior","Plants","Furniture","Electronics","Bathroom","Kitchen Equipment","Interior, decor","Light Fixture","Human, Character","Food, drink","Aircraft","Watercraft","Vehicle, transport","Military, weapon","Animals","Hospital-medical","Holiday, gifts","Musical equipment","Office equipment","Service equipment","Sports, entertainment","Clothing, shoes","Cosmetics, Beauty","Industrial design","Toys, childrens","Jewelry","Other"]
            if category.xpath(".//text()").get() in ["Aircraft"]
            # if category.xpath(".//text()").get() not in ["Full 3D-scenes", "COLLECTIONS", "3D-Print Models"]
        ]

        data: AllDataItem = AllDataItem()
        _category_items: list[CategoryPostsListItem] = []
        # print(categories)

        for category in categories:
            _request = scrapy.Request(category, self.parse_cards_by_category)
            # _category_items = _request.meta["category_items_list"]

            _request.meta["all_data"] = data

            category_items = CategoryPostsListItem()
            category_items["category"] = list(filter(None, category.split("/")))[-1]
            category_items["posts"] = []

            _category_items.append(category_items)

            _request.meta["category_items_list"] = category_items

            yield _request

    def parse_cards_by_category(self, response: Response):
        items = response.xpath("//*[@class='navigation']//a/text()")

        last_index = items[-1].extract() if items else 1
        urls = (f'{str(response.url[:-1])}/page/{i}' for i in range(1, int(last_index)+1))

        # data = response.meta["all_data"]
        posts_list_item = response.meta["category_items_list"]

        for url in urls:
            _request = scrapy.Request(url, self.parse_page_cards_by_urls)

            _request.meta["items"] = posts_list_item
            # print(f"{posts_list_item=}")
            # _request.meta["all_data"] = data
            yield _request
            print(f'{_request.meta["items"]=}')
            print(f'{len(_request.meta["items"]["posts"])=}')
            # posts_list_item = _request.meta["items"]
            # print(f"{posts_list_item=}")
            # print("_"*13)

        yield posts_list_item

    def parse_page_cards_by_urls(self, response: Response):
        item_block_xpath = "//*[@class='shotstory-3d-block-new']"
        item_block_title_xpath = ".//*[@class='shotstory-3d-text-block']/text()"
        item_block_url_xpath = ".//a/@href"

        # data = response.meta["all_data"]
        post_list_item: CategoryPostsListItem = response.meta["items"]
        _posts = post_list_item["posts"]

        # print(f"{post_list_item=}")

        for item_block in response.xpath(item_block_xpath):
            _item = PostItem()

            _item["title"] = item_block.xpath(item_block_title_xpath).get().replace("\n", "")
            _item["url"] = item_block.xpath(item_block_url_xpath).get()
            _item["download_links"] = [f"https://site.net/download/{i}" for i in range(1)]

            # print(f"{len(_posts)=}")
            _posts.append(_item)

            # yield _item
            # yield scrapy.Request(item_block.xpath(item_block_url_xpath).get(), self.parse_archive_download_urls_by_post_url)

        post_list_item["posts"] = _posts
        response.meta["items"] = post_list_item
        # yield post_list_item

    def parse_archive_download_urls_by_post_url(self, response: Response):
        post_title_xpath = "//*[@class='main-news-title']//*/text()"
        archive_link_xpath = "//*[@class='down-link-block']"
        category_text_xpath = "//*[@class='main-news-info-item']//*[contains(@*, 'aircraft')]/text()"

        with_href_xpath = ".//a/@href"
        with_text_xpath = ".//text()"

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

        # hitfile_download_link = [link for link in download_links if "hit" in link]
        # hot4share_download_link = [link for link in download_links if "hot4share" in link]

        # items: CategoryPostsListItem = response.meta["items"]
        post_item = PostItem()

        post_item["title"] = response.xpath(post_title_xpath).get()
        post_item["url"] = response.url
        post_item["category"] = response.xpath(category_text_xpath).get()
        post_item["download_links"] = download_links
        yield post_item
        # items.posts.append(post_item)
        # yield items
        # yield {
        #     "title": response.xpath(post_title_xpath).get(),
        #     "url": response.url,
        #     "download_links": download_links,
        # }

