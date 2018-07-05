from tools.db import RedisClient
from tools.getter import Scheduler
conn = RedisClient()


def set(proxy):
    result = conn.add(proxy)
    print(proxy+'录入成功' if result else proxy+'录入失败')


# 手动添加代理
def scan():
    print('请输入代理, 输入exit退出读入')
    while True:
        proxy = input()
        if proxy == 'exit':
            break
        set(proxy)


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
