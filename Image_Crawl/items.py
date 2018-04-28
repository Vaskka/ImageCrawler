# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst





class ImageCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ImageItem(scrapy.Item):
    def get_SQL(self):

        SQL_insert = """
            insert into table_image(img_url, img_title, img_size, img_upload_time, img_file_path, img_base64)
            VALUES (%s, %s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE img_url=VALUES(img_url), img_title=VALUES(img_title), img_size=VALUES(img_size),
            img_upload_time=VALUES(img_upload_time), img_file_path=VALUES(img_file_path), img_base64=VALUES(img_base64)
        """

        params = (self['img_url'],
                  self['img_title'],
                  self['img_size'],
                  self['img_upload_time'],
                  self['img_file_path'],
                  self['img_base64'])

        return SQL_insert, params


    # 下一张图片的url
    next_url = scrapy.Field(
        output_processor=TakeFirst()
    )

    # 图片url
    img_url = scrapy.Field()

    # 图片关键字
    img_title = scrapy.Field(
        output_processor=TakeFirst()
    )

    # 图片尺寸
    img_size = scrapy.Field(
        output_processor=TakeFirst()
    )

    # 图片上传时间
    img_upload_time = scrapy.Field(
        output_processor=TakeFirst()
    )

    # 本地图片路径
    img_file_path = scrapy.Field(
        output_processor=TakeFirst()
    )

    # 图片文件编码结果
    img_base64 = scrapy.Field()

    pass