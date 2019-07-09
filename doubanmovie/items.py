# -*- coding: utf-8 -*-
import scrapy


class DoubanmovieItem(scrapy.Item):
    name = scrapy.Field()
    rate = scrapy.Field()
    tag = scrapy.Field()
