# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class PostItem(scrapy.Item):
    title = Field()
    url = Field()
    category = Field()
    download_links = Field()
    images = Field()
    size = Field()


class CategoryPostsListItem(scrapy.Item):
    category = Field()
    posts: list[PostItem] = Field()


class AllDataItem(scrapy.Item):
    data = Field()
