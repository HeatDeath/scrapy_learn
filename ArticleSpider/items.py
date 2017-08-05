# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def add_jobbole(value):
    return value + '-bobby'


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, '%Y/%m/%d').date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date

def get_number(value):
    match_pattern = '.*?(\d+).*'
    value = re.match(match_pattern, value)
    return value

def return_value(value):
    return value

class ArticleItemLoader(ItemLoader):
    # 自定义 ItemLoader
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        # 输入值预处理
        # input_processor=MapCompose(lambda x:x+'-jobbole', add_jobbole),
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()

    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )

    front_image_path = scrapy.Field()
    # praise_count = scrapy.Field()
    comment_count = scrapy.Field(
        input_processor=MapCompose(get_number)
    )
    fav_count = scrapy.Field(
        input_processor=MapCompose(get_number)
    )
    category_tag = scrapy.Field()
    article_content = scrapy.Field()