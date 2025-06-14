# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanprojectItem(scrapy.Item):
    title = scrapy.Field()  # 电影名字
    content = scrapy.Field()  # 电影信息
    infi = scrapy.Field()  # 电影简介
    score = scrapy.Field()  # 电影评分


