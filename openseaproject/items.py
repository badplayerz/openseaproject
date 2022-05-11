# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OpenseaprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rankNo = scrapy.Field()
    name = scrapy.Field()
    img = scrapy.Field()
    uri = scrapy.Field()
    volume = scrapy.Field()
    dd24h = scrapy.Field()
    dd7D = scrapy.Field()
    floorPrice = scrapy.Field()
    owners = scrapy.Field()


class OS_Otherside(scrapy.Item):
    address = scrapy.Field()
    rankNo = scrapy.Field()
