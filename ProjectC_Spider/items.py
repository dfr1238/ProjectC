# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VscodeSshScrapyTestItem(scrapy.Item):
    keyword = scrapy.Field()
    title = scrapy.Field()
    time= scrapy.Field()
    author= scrapy.Field()
    content= scrapy.Field()
    source= scrapy.Field()
    url= scrapy.Field()
