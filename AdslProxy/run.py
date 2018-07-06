from adslproxy.api import server
from adslproxy.db import RedisClient
from adslproxy.sender import run

if __name__ == '__main__':
    redis = RedisClient(host='', password='')
    server(redis=redis)
    run()
