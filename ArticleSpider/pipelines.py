# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import MySQLdb
import MySQLdb.cursors

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline(object):
    # 采用同步机制写入 MySQL
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='roottest',
            db='spider',
            charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = 'insert into article_spider (title, url, create_date, fav_count, url_object_id)' \
                     'VALUES (%s, %s, %s, %s, %s)'
        # 同步操作，非异步
        self.cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['fav_count'], item['url_object_id']))
        self.conn.commit()

class MysqlTwistedPipline(object):
    # mysql 插入 异步化, teisted 提供 异步容器
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        db_params = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )

        dbpool = adbapi.ConnectionPool('MySQLdb', **db_params)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用 twisted 将 MySQL 插入变成 异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)

        # 处理异常
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor,item):
        # 执行具体的插入
        insert_sql = 'insert into article_spider (title, url, create_date, fav_count, url_object_id)' \
                     'VALUES (%s, %s, %s, %s, %s)'

        cursor.execute(insert_sql,
                            (item['title'], item['url'], item['create_date'], item['fav_count'], item['url_object_id']))

class JsonWithEncodingPipeline(object):
    # 自定义 json 文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_close(self, spider):
         self.file.close()

class JsonExporterPipeline(object):
    # 调用 scrapy 提供的 json exporter 导出 json 文件
    def __init__(self):
        self.file = open('article_exporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'front_image_url' in item:
            for ok, value in results:
                image_file_path = value['path']
            # item['front_image_path'] = image_file_path


        return item