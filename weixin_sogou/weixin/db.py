#encoding:utf-8
from redis import StrictRedis
from pickle import dumps, loads
from requests import Request


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = ''
REDIS_KEY = 'weixin'


class WeixinRequest(Request):
    def __init__(self, url, callback, method='GET', headers=None, need_proxy=False, fail_time=0, timeout=10):
        Request.__init__(self, method, url, headers)
        # super(WeixinRequest, self).__init__(method, url, headers)
        self.callback = callback
        self.need_proxy = need_proxy
        self.fail_time = fail_time
        self.timeout = timeout


class RedisQueue():
    def __init__(self):
        """
        初始化Redis
        """
        self.db = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    def add(self, request):
        """
        向队列添加序列化后的Request
        :param request: 请求对象
        :param fail_time: 失败次数
        :return: 添加结果
        """
        if isinstance(request, WeixinRequest):
            return self.db.rpush(REDIS_KEY, dumps(request))
        return False

    def pop(self):
        """
        取出下一个Request并反序列化
        :return: Request or None
        """
        if self.db.llen(REDIS_KEY):
            return loads(self.db.lpop(REDIS_KEY))
        else:
            return False

    def clear(self):
        self.db.delete(REDIS_KEY)

    def empty(self):
        return self.db.llen(REDIS_KEY) == 0


# if __name__ == '__main__':
#     db = RedisQueue()
#     start_url = 'http://weixin.sogou.com/weixin?type=2&query=python'
#     weixin_request = WeixinRequest(url=start_url, callback='hello', need_proxy=True)
#     db.add(weixin_request)
#     request = db.pop()
#     print(request)
#     print(request.callback, request.need_proxy)
