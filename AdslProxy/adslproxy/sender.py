import re
import time
import requests
from requests.exceptions import ConnectionError, ReadTimeout
from adslproxy.db import RedisClient
import platform

# 测试URL
TEST_URL = 'http://www.baidu.com'
# 测试超时时间
TEST_TIMEOUT = 20
# 拨号间隔
ADSL_CYCLE = 100
# 拨号出错重试间隔
ADSL_ERROR_CYCLE = 5
# ADSL命令
ADSL_BASH = 'adsl-stop;adsl-start'
# 代理运行端口
PROXY_PORT = 8888
# 客户端唯一标识
CLIENT_NAME = 'adsl1'
# 拨号网卡
ADSL_IFNAME = 'ppp0'

# 判断python版本
if platform.python_version().startswith('2.'):
    import commands as subprocess
elif platform.python_version().startswith('3.'):
    import subprocess
else:
    raise ValueError('python版本必须为2或3')


class Sender():
    def get_ip(self, ifname=ADSL_IFNAME):
        """
        获取本机IP
        :param ifname: 网卡名称
        :return:
        """
        (status, output) = subprocess.getstatusoutput('ifconfig')
        if status == 0:
            pattern = re.compile(ifname + '.*?inet.*?(\d+\.\d+\.\d+\.\d+).*?netmask', re.S)
            result = re.search(pattern, output)
            if result:
                ip = result.group(1)
                return ip

    def test_proxy(self, proxy):
        """
        测试代理
        :param proxy: 代理
        :return: 测试结果
        """
        try:
            response = requests.get(TEST_URL, proxies={
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }, timeout=TEST_TIMEOUT)
            if response.status_code == 200:
                return True
        except (ConnectionError, ReadTimeout):
            return False

    def remove_proxy(self):
        """
        移除代理
        :return: None
        """
        self.redis = RedisClient()
        self.redis.remove(CLIENT_NAME)
        print('已移除该代理IP')

    def set_proxy(self, proxy):
        """
        设置代理
        :param proxy: 代理
        :return: None
        """
        self.redis = RedisClient()
        if self.redis.set(CLIENT_NAME, proxy):
            print('已设置代理IP', proxy)

    def adsl(self):
        """
        拨号主进程
        :return: None
        """
        while True:
            print('移除代理并开始ADSL拨号，请稍等...')
            self.remove_proxy()
            (status, output) = subprocess.getstatusoutput(ADSL_BASH)
            if status == 0:
                print('拨号成功')
                ip = self.get_ip()
                if ip:
                    print('现在的IP是', ip)
                    proxy = '{ip}:{port}'.format(ip=ip, port=PROXY_PORT)
                    if self.test_proxy(proxy):
                        print('代理IP{}可用'.format(proxy))
                        self.set_proxy(proxy)
                        print('已将代理IP更新到Redis，将在{}秒后重新拨号'.format(ADSL_CYCLE))
                        time.sleep(ADSL_CYCLE)
                    else:
                        print('代理IP{}不可用'.format(proxy))
                else:
                    print('获取IP失败，将在{}秒后重新拨号'.format(ADSL_CYCLE))
                    time.sleep(ADSL_ERROR_CYCLE)
            else:
                print('拨号失败，将在{}秒后重新拨号'.format(ADSL_CYCLE))
                time.sleep(ADSL_ERROR_CYCLE)


def run():
    sender = Sender()
    sender.adsl()


# if __name__ == '__main__':
#     run()
