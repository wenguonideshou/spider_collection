import requests

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'http://www.baidu.com'

proxy = '96.9.90.90:8080'

proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy,
}

print(TEST_URL)
response = requests.get(TEST_URL, proxies=proxies, verify=False)
if response.status_code == 200:
    print('Successfully')

