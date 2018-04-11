# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


def return_value(value):
    return value


def get_no(value):
    match_re = re.match("(\d+)", value)
    no = int(match_re.group(1))
    return no


class MovieItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()


class DoubansipiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    No = scrapy.Field(
        input_processor=MapCompose(get_no)
    )  # 排名
    graded = scrapy.Field()  # 评分
    comment = scrapy.Field()  # 评价
    director = scrapy.Field(
        output_processor=MapCompose(return_value)
    ) # 导演
    scriptwriter = scrapy.Field(
        output_processor=MapCompose(return_value)
    ) # 编剧
    protagonist = scrapy.Field(
        output_processor=MapCompose(return_value)
    ) # 主演
    movie_type = scrapy.Field(
        output_processor=MapCompose(return_value)
    ) # 电影类型
    region = scrapy.Field() # 地区
    language = scrapy.Field() # 语言
    release_data = scrapy.Field(
        output_processor=MapCompose(return_value)
    ) # 上映时间
    mins = scrapy.Field() # 片长
    alternate_name = scrapy.Field() # 又名
    synopsis = scrapy.Field(
        output_processor=MapCompose(return_value)
    ) # 简介
    url = scrapy.Field()