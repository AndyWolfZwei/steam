import requests
import json
url = 'http://steamcommunity.com/market/search/render/?query=&start=100&count=100&search_descriptions=0&sort_co' \
      'lumn=popular&sort_dir=desc&appid=570'
cont = requests.get(url)
dic = json.loads(cont.text)
print(type(dic))
print(dic['results_html'])
