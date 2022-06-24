import requests
import random
# 随机user-agent池
user_agent_pool = ["Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
"Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
"Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"]


url = 'https://patents.google.com/xhr/query?url=q%3Dpollution%2Btreatment%26before%3Dpriority%3A20040201%26after%3Dpriority%3A20040102&exp=&download=true'
#    url = 'https://en.ipip.net/'
#    url = 'http://baidu.com'
headers = {}
headers['user_agent'] = user_agent_pool[random.randrange(0,len(user_agent_pool))]
#clash翻墙的端口
proxies = {'http': 'http://localhost:7890', 'https': 'http://localhost:7890'}
print(proxies)
r = requests.get(url, stream=True,headers=headers,proxies=proxies)

print(r)