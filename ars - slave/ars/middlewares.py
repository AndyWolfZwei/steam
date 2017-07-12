# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import redis
from scrapy import signals
import random

from scrapy.core.downloader import DownloaderMiddlewareManager
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import time
from ars.settings import REDIS_URL
from .ip import user_agent_list, ip_url, test_url
from .ip import IpPool


class ArsSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # print('process_spider_input',response)
        # Called for each response that goes through the spider
        # middleware and into the spider.
        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
        if response.status != 200:
            print(":::ERROR:::" + str(response.url).strip() + " 链接响应错误!!!!!! http状态码为:" + str(response.status).strip())
            print('当前代理是：',response.meta["proxy"])
            self.add_url_to_redis({'url': response.url})
            time.sleep(1)
        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    @staticmethod
    def add_url_to_redis(url):
        reds = redis.Redis.from_url(REDIS_URL, db=0, decode_responses=True)
        reds.lpush('annualrs0:items', url)

    @staticmethod
    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.
        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    @staticmethod
    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.
        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RotateUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        ua = random.choice(user_agent_list)
        if ua:
            # 显示当前使用的useragent
            # print("********Current UserAgent:%s************" % ua)
            # 记录
            request.headers.setdefault('User-Agent', ua)


class HttpProxyMiddleware(IpPool):
    def __init__(self):
        """
        new_ip :  从数据库取出ip来使用
        ip_pool : 当代理不满足需求 从网上获取新ip  自动放到ip_pool 然后手动导入数据库
        """

        super(HttpProxyMiddleware, self).__init__()
        # self.clear_all()
        # self.get_ip(ip_url)
        # self.test_ip(test_url)
        self.conn_sql()
        self.new_ip = self.get_sql_ip()    # 从数据拿上次的ip
        self.num = len(self.new_ip)        # 保存 ip_pool的初始数量
        # for ip in self.ip_pool:
        #     self.write_to_sql(ip)
        self.close_sql()

    def process_request(self, request, spider):
        if len(self.new_ip) >= 10:
            now_ip = random.choice(self.new_ip)
            print('当前IP is:', now_ip[0])
            request.meta["proxy"] = "http://" + now_ip[0]
        else:
            self.ip_pool.clear()   # 先清空ip_pool的数据
            self.get_ip(ip_url)
            self.test_ip(test_url)
            self.conn_sql()
            for ip in self.ip_pool:
                self.write_to_sql(ip)
            self.new_ip = self.get_sql_ip()
            self.close_sql()
            return self.process_request(request, spider)

    def process_exception(self, request, exception, spider):
        print('the invailed prox is:', request.meta["proxy"])
        ArsSpiderMiddleware.add_url_to_redis({'url': request.url})
        self.del_to_sql(request.meta["proxy"].replace('http://', ''))
        try:
            temp_ip = []
            [temp_ip.append(i[0]) for i in self.new_ip]
            temp_ip.remove(request.meta["proxy"].replace('http://', ''))    # 由于new_ip 是tuple 所以先转list 再remove
            self.new_ip = tuple([(i,) for i in temp_ip])
        except Exception as e:
            print(e, self.new_ip, 'and:', request.meta["proxy"])
        print(exception)
