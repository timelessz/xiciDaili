# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class MySQLStorePipeline(object):
    def __init__(self, conn):
        self.conn = conn

    # 从配置文件中读取数据
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dbargs = dict(
            host=settings.get('MYSQL_HOST'),
            port=3306,
            user=settings.get('MYSQL_USER'),
            password=settings.get('MYSQL_PASSWD'),
            db=settings.get('MYSQL_DBNAME'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
        )
        connection = pymysql.connect(**dbargs)
        return cls(connection)

    # pipeline默认调用
    # 如果 进入的 item[page] 为 1 而且是 编号也是1 的话 清空数据库中的 代理数据 每次都用最新的数据
    def process_item(self, item, spider):
        # pass
        # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


        # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        try:
            with self.conn.cursor()  as cursor:
                if item['NUM'] == 1 and item['PAGE'] == 1:
                    sql = 'TRUNCATE TABLE scrapy.sc_proxyip;'
                    cursor.execute(sql)
                    self.conn.commit()
                sql = 'insert into `sc_proxyip` (`ip`,`port`,`position`,`type`,`speed`,`lastchecktime`) values(%s,%s,%s,%s,%s,%s);'
                cursor.execute(sql, (
                    item['IP'], item['PORT'], item['POSITION'], item['TYPE'], item['SPEED'], item['LAST_CHECK_TIME']))
            self.conn.commit()
        except Exception as e:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print(e)
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            self.conn.rollback()
