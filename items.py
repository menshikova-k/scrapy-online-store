# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AkplitkaItem(scrapy.Item):

    name = scrapy.Field()
    factory = scrapy.Field()
    link = scrapy.Field()
    pass
