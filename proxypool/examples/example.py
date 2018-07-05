import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'bid=rxkp-KmiZyE; _vwo_uuid_v2=DF87AF712B324634879F3A2D5D31ED9E5|81b137b3579567293c8840ba6a0a0055; gr_user_id=caf846ce-442b-4aed-8256-fff7b1d045a7; Hm_lvt_ba7c84ce230944c13900faeba642b2b4=1527556940; ll="118172"; __utmv=30149280.176; viewed="26869212_27177839_2297146_30175598_26999123_30217266_6424904_30172800_26320485_26387975"; __utmz=30149280.1529380621.33.10.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=30149280.1099494689.1525846315.1529380621.1530776612.34; __utmc=30149280; __utmt=1; __utmb=30149280.1.10.1530776612; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1530776816%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1972088575.1527556940.1527556940.1530776816.2; __utmb=223695111.0.10.1530776816; __utmc=223695111; __utmz=223695111.1530776816.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=f7f1bf5b611e94fb.1527556940.2.1530776943.1527556953.',
    'Host': 'movie.douban.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.3',
}


# 从API随机获取代理
def get_proxy():
    try:
        response = requests.get('http://localhost:5555/random')
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


count = 0


# 使用代理爬取目标网站
def main(url):
    global count
    proxy = get_proxy()
    proxies = {'http': proxy}
    r = requests.get(url, proxies=proxies, headers=headers)
    for x in r.json():
        print('第{}个数据'.format(count), x.get('title'), x.get('rating'), x.get('rank'), x.get('score'),
              x.get('cover_url'), x.get('types'),
              x.get('regions'), x.get('url'), x.get('release_date'), x.get('actor_count'), x.get('vote_count'),
              x.get('actors'))
        count += 1


if __name__ == '__main__':
    for type in range(1, 32):
        for x in range(1000):
            main(
                'https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start={}&limit=20'.format(
                    type, 20 * x))
