import requests
import re
import pymysql

ip_url = 'http://vtp.daxiangdaili.com/ip/?tid=559683383645773&num=20&delay=3&filter=on'
test_url = 'http://1212.ip138.com/ic.asp'

user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1",
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11",
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6",
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6",
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1",
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5",
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5",
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3",
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3",
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3",
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3",
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3",
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3",
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3",
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3",
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3",
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24",
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24",
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
]


class IpPool:
    def __init__(self):
        self.ips = []
        self.ip_pool = []
        self.ip_num = 0
        try:
            self.con = pymysql.connect(host='127.0.0.1', user='root', passwd='3857036', db='ip', charset='utf8')
            self.cur = self.con.cursor()
            self.close_sql()
        except Exception as e:
            print('CONNECT FAILED:', e)

    def get_ip(self, i_url):
        cont = requests.get(i_url).text
        ips = cont.split('\r\n')
        [self.ips.append(i) for i in ips if i]
        return self.ips

    def test_ip(self, t_url):
        for ip in self.ips:
            proxy = "http://" + ip
            proxies = {"http": proxy}
            print(proxies)
            try:
                response = requests.get(t_url, proxies=proxies, timeout=20)
                msg = re.search('<center>(.*?)</center>', response.content.decode('gbk'))
                if response.status_code == 200:
                    print(msg.group(1))
                    self.ip_pool.append(ip)
            except Exception as e:
                print(e)
                continue                         # 测试ip有效性

    def conn_sql(self):                         # 连接数据库
        self.con = pymysql.connect(host='127.0.0.1', user='root', passwd='3857036', db='ip', charset='utf8')
        self.cur = self.con.cursor()

    def close_sql(self):                         # 关闭数据库
        self.cur.close()
        self.con.close()

    def write_to_sql(self, ip):                  # 写入ip
        w_sql = "INSERT INTO ip_sql(ip) VALUES (%s)"
        self.cur.execute(w_sql, ip)
        self.con.commit()

    def del_to_sql(self, ip):                     # 删除ip
        self.conn_sql()
        d_sql = "delete from ip_sql where ip='%s'" % ip
        self.cur.execute(d_sql)
        self.con.commit()
        self.close_sql()

    def get_sql_ip(self):                        # 获取sql中所有ip   要打开关闭
        g_sql = "select * from ip_sql"
        self.cur.execute(g_sql)
        self.con.commit()
        return self.cur.fetchall()

    def update_sql(self):                        # 更新数据库
        self.get_ip(ip_url)
        self.test_ip(test_url)
        self.conn_sql()
        for i in ippool.ip_pool:
            self.write_to_sql(i)
        self.close_sql()

    def clear_all(self):                        # 清空数据库
        self.conn_sql()
        c_sql = "truncate table ip_sql"
        self.cur.execute(c_sql)
        self.con.commit()
        self.close_sql()

if __name__ == '__main__':
    ippool = IpPool()
    ippool.get_ip(ip_url)
    ippool.test_ip(test_url)
    ippool.conn_sql()
    for i in ippool.ip_pool:
        ippool.write_to_sql(i)
    ippool.close_sql()
