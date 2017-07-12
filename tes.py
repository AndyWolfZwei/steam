import requests

proxy = 'http://180.97.235.30:80'
proxies = {"http": proxy}

u = requests.get('http://1212.ip138.com/ic.asp',proxies=proxies)
print(u.status_code)