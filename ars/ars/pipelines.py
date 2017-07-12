# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class ArsPipeline(object):
    def process_item(self, item, spider):
        con = pymysql.connect(host='127.0.0.1', user='root', passwd='3857036', db='ars', charset='utf8')
        cur = con.cursor()
        sql = ("INSERT INTO ars_info_go(MarketName,MarketHashName,Game,Quality,Rarity,Type,Hero,Exterior,Description,"
               "InspectLink,Tournament,icon,url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        lis = (item['MarketName'], item['MarketHashName'], item['Game'], item['Quality'],
               item['Rarity'], item['Type'], item['Hero'], item['Exterior'], item['Description'],
               item['InspectLink'], item['Tournament'], item['icon'], item['url'])
        cur.execute(sql, lis)
        con.commit()
        cur.close()
        con.close()
        return item
