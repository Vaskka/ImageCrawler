# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb

from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi
from MySQLdb.cursors import DictCursor

from Image_Crawl import settings
from Image_Crawl.utils import utils

class ImageCrawlPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonExplorerPipeline(object):
    # 使用框架保存数据到json
    def __init__(self):
        self.file = open('table_img.json', 'wb')
        self.json_explorer = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.json_explorer.start_exporting()

    def process_item(self, item, spider):
        self.json_explorer.export_item(item)
        return item

    def spider_closed(self, spider):
        self.json_explorer.finish_exporting()
        self.file.close()


class MysqlTwistedPipeline(object):

    # 使用Twisted异步保存数据到mysql
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            db=settings['MYSQL_DBNAME'],
            charset='utf8',
            cursorclass=DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将item处理变成异步操作
        fullpath = settings.project_dir + "\\images\\" + item['img_file_path'].replace('/', "\\")
        item['img_base64'] = utils._from_path_to_base64(fullpath)

        pass

        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)
        pass

    def do_insert(self, cursor, item):
        # 具体插入操作
        SQL_insert, params = item.get_SQL()
        cursor.execute(SQL_insert, params)


class ImgPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        img_file_path = ""
        for (ok, value) in results:
            img_file_path = value['path']

        # 获得图片文件路径
        item['img_file_path'] = img_file_path

        return item
