from cookiespool.scheduler import Scheduler
from cookiespool.db import RedisClient

conn = RedisClient('accounts', 'weibo')


def main():
    s = Scheduler()
    s.run()


if __name__ == '__main__':
    main()
