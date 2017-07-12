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


class AnnualrsSpider(RedisSpider):
    rar_l = ['消费级', '军规级', '工业级', '受限', '保密', '隐秘', '普通级', '高级', '奇异', '非凡', '卓越', '违禁']
    qua_l = ['普通', '纪念品', 'StatTrak™', '★ StatTrak™', '★']
    name = 'annualrs0'
    allowed_domains = ['steamcommunity.com']
    redis_key = 'steam:start_urls'
    start_urls = []
    for i in range(0, 9400, 100):
        start_urls.append('http://steamcommunity.com/market/search/render/?query=&start=%s&count=100&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730' % i)

    def start_requests(self):    # 重写scrapy redis的 start_requests
        for url in self.start_urls:
            time.sleep(2)
            print(url)
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        dic = json.loads(response.body)
        print(response)
        soup = BeautifulSoup(dic['results_html'], 'html.parser')
        arts = soup.find_all('a', class_=re.compile('market_listing_row_link'))
        for art in arts:
            # print(art['href'])
            # request = Request(url=art['href'], callback=self.get_info1)
            yield {'url': art['href']}


    # def get_info1(self, response):
            #         if response.status != 200:

        # print(":::ERROR:::" + str(response.url).strip() + " 链接响应错误!!!!!! http状态码为:" + str(response.status).strip())
        #     time.sleep(10)
        #     self.add_url_to_redis(str(response.url).strip())
        # else:
        #     item = ArsItem()
        #     ext = ' '
        #     descri = ' '
        #     flag = 1
        #     js = re.search('var g_rgAssets = (.*?}}});', response.text)
        #     dic = json.loads(js.group(1))
        #     t = dic['730']['2'][list(dic['730']['2'].keys())[0]]
        #     mes = []
        #     [mes.append(i['value']) for i in t['descriptions'] if
        #      not re.findall('统计将被重置|数聚™', i['value']) and i['value'].strip() and 'color'not in i]
        #     for me in mes:
        #         if '外观' in me:
        #             ext = me.split('：')[-1]
        #         if len(me) > 30 and flag == 1:
        #             descri = re.sub('\n|</?\w+>', '', me)
        #             flag = 0
        #
        #     item['MarketName'] = re.sub('\(.+\)', '', t['market_name'])
        #
        #     item['MarketHashName'] = urllib.parse.unquote(response.url.split('/')[-1])
        #
        #     item['Game'] = 730
        #
        #     item['Quality'] = ' '
        #     item['Rarity'] = ' '
        #     for i in t['type'].split(' '):
        #         if i in self.qua_l:
        #             item['Quality'] = i
        #         if i in self.rar_l:
        #             item['Rarity'] = i
        #     else:
        #         item['Type'] = t['type'].split(' ')[-1]
        #
        #     item['Hero'] = ' '
        #
        #     item['Exterior'] = ext
        #
        #     item['Description'] = descri
        #
        #     try:
        #         item['InspectLink'] = t['market_actions'][0]['link']
        #     except:
        #         item['InspectLink'] = ' '
        #
        #     item['Tournament'] = ' '
        #
        #     try:
        #         item['icon'] = t['icon_url_large']
        #     except KeyError:
        #         item['icon'] = ' '
        #
        #     item['url'] = response.url
        #     yield item
        pass