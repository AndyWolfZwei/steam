import requests
import re
from bs4 import BeautifulSoup
from scrapy import Request
from ars.items import ArsItem
import json
import urllib.parse
import time
from scrapy_redis.spiders import RedisSpider
import redis
from ..settings import REDIS_URL
from scrapy_redis.utils import bytes_to_str

class AnnualrsSpider(RedisSpider):
    rar_l = ['消费级', '军规级', '工业级', '受限', '保密', '隐秘', '普通级', '高级', '奇异', '非凡', '卓越', '违禁']
    qua_l = ['普通', '纪念品', 'StatTrak™', '★ StatTrak™', '★']
    name = 'annualrs1'
    allowed_domains = ['steamcommunity.com']
    redis_key = 'annualrs0:items'

    # def parse(self, response):
    #     dic = json.loads(response.body)
    #     soup = BeautifulSoup(dic['results_html'], 'html.parser')
    #     arts = soup.find_all('a', class_=re.compile('market_listing_row_link'))
    #     for art in arts:
    #         print(art['href'])
    #         request = Request(url=art['href'], callback=self.get_info1)
    #         request.meta['PhantomJS'] = True
    #         yield request

    def make_request_from_data(self, data):    # 改变redis_key 中获取的url
        url = bytes_to_str(data, self.redis_encoding)
        return self.make_requests_from_url(eval(url)['url'])

    def parse(self, response):
        item = ArsItem()
        ext = ' '
        descri = ' '
        flag = 1
        js = re.search('var g_rgAssets = (.*?}}});', response.text)
        dic = json.loads(js.group(1))
        t = dic['730']['2'][list(dic['730']['2'].keys())[0]]
        mes = []
        [mes.append(i['value']) for i in t['descriptions'] if
         not re.findall('统计将被重置|数聚™', i['value']) and i['value'].strip() and 'color'not in i]
        for me in mes:
            if '外观' in me:
                ext = me.split('：')[-1]
            if len(me) > 30 and flag == 1:
                descri = re.sub('\n|</?\w+>', '', me)
                flag = 0

        item['MarketName'] = re.sub('\(.+\)', '', t['market_name'])

        item['MarketHashName'] = urllib.parse.unquote(response.url.split('/')[-1])

        item['Game'] = 730

        item['Quality'] = ' '
        item['Rarity'] = ' '
        for i in t['type'].split(' '):
            if i in self.qua_l:
                item['Quality'] = i
            if i in self.rar_l:
                item['Rarity'] = i
        else:
            item['Type'] = t['type'].split(' ')[-1]

        item['Hero'] = ' '

        item['Exterior'] = ext

        item['Description'] = descri

        try:
            item['InspectLink'] = t['market_actions'][0]['link']
        except:
            item['InspectLink'] = ' '

        item['Tournament'] = ' '

        try:
            item['icon'] = t['icon_url_large']
        except KeyError:
            item['icon'] = ' '

        item['url'] = response.url
        yield item
