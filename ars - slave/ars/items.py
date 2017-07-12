# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArsItem(scrapy.Item):
    # define the fields for your item here like:
    MarketName = scrapy.Field()
    MarketHashName = scrapy.Field()
    Game = scrapy.Field()
    Quality = scrapy.Field()
    Rarity = scrapy.Field()
    Type = scrapy.Field()
    Hero = scrapy.Field()
    Exterior = scrapy.Field()
    Description = scrapy.Field()
    InspectLink = scrapy.Field()
    Tournament = scrapy.Field()
    icon = scrapy.Field()
    url = scrapy.Field()
    pass
