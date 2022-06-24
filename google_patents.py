import requests
import pandas as pd
import os
import random
import time
import emailbox

key_file = pd.read_csv('KEY_WORDS.csv')
base_url = "https://patents.google.com"

dirs = './google_patents'

if not os.path.exists(dirs):
    os.makedirs(dirs)



def send_error_email(message):
    import emailbox as emb
    Subject = '警告'
    # 显示发送人
    sender_show = 'dipan.tang@foxmail.com'
    # 显示收件人
    recipient_show = 'xxx'
    # 实际发给的收件人
    to_addrs = 'tararatang@icloud.com'
    emb.sendMail(message, Subject, sender_show, recipient_show, to_addrs)


key_words = []
for i in range(len(key_file['KEY_WORDS'])):
    key_words.append(key_file['KEY_WORDS'][i].strip())

date_list = []
for year in range(2022, 1990, -1):
    for month in range(12, 0, -1):
        if year == 2022 and month >= 6:
            continue
        date = str(year) + '0' + str(month) + '02-' + str(year) + '0' + str(
            month + 1) + '01'
        if month >= 10:
            date = str(year) + str(month) + '02-' + str(year) + str(month +
                                                                    1) + '01'
        if month == 9:
            date = str(year) + '0' + str(month) + '02-' + str(year) + str(
                month + 1) + '01'
        if month == 12:
            date = str(year - 1) + str(month) + '02-' + str(year) + '01' + '01'
        date_list.append(date)

file_name_list = []
for key_word in key_words:
    for date in date_list:
        file_name = key_word.replace(' ', '_') + '_' + date + '.csv'
        file_name_list.append(file_name)

url_list = []
for key_word in key_words:
    for date in date_list:
        date_0 = date.split('-')[0]
        date_1 = date.split('-')[1]
        href = '''/xhr/query?url=q%3D''' + key_word.replace(
            ' ', '%2B'
        ) + '''%26before%3Dpriority%3A''' + date_1 + '''%26after%3Dpriority%3A''' + date_0 + '''&exp=&download=true'''
        url_list.append(base_url + href)

# 随机user-agent池
user_agent_pool = [
    "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
]

f = open(r'test.txt', 'r')  #打开所保存的cookies内容文件
cookies_list = []

for line in f.readlines():
    cookies = {}
    for i in line.split(';'):  #按照字符：进行划分读取
        #其设置为1就会把字符串拆分成2份
        name, value = i.strip().split('=', 1)
        cookies[name] = value  #为字典cookies添加内容
    cookies_list.append(cookies)
    cookies_list.append([])

cookies_now = cookies_list[0]

for file_name in file_name_list:
    file_location = './google_patents/' + file_name
    if os.path.exists(file_location):
        continue
    url = url_list[file_name_list.index(file_name)]

    headers = {}
    headers['user_agent'] = user_agent_pool[random.randrange(
        0, len(user_agent_pool))]
    #clash翻墙端口
    proxies = {
        'http': 'http://localhost:7890',
        'https': 'http://localhost:7890'
    }
    print(proxies)
    print(file_name)
    try:
        r = requests.get(url,
                        headers=headers,
                        cookies=cookies_now)
    except:
        time.sleep(30)
    time.sleep(20)

    if r.status_code != requests.codes.ok:

        for cookies in cookies_list:
            if cookies != cookies_now:
                try:
                    r = requests.get(url,
                                    headers=headers,
                                    cookies=cookies)
                except:
                    time.sleep(30)
                time.sleep(20)
                if r.status_code == requests.codes.ok:
                    cookies_now = cookies
                    break

    if r.status_code != requests.codes.ok:
        send_error_email('爬虫停止')
        print('爬虫停止')
        break

    fo = open(file_location, 'wb')
    fo.write(r.content)
    fo.close()
    print(r)
    print(time.asctime(time.localtime(time.time())))
