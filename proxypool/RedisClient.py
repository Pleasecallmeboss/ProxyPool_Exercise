
import imp
import redis

from proxypool.setting import *
from proxypool.Proxy import Proxy
from proxypool.utils import *
from loguru import logger
from random import choice
from proxypool.exception import PoolEmptyException
from typing import List

class RedisClient(object):
    '''
    与redis数据库的沟通
    '''
    def __init__(self,host=HOST,port = PORT,password = PASSWORD,db = DB) -> None:
        self.pool = redis.ConnectionPool(host=host,port=port,password=password,db=db,decode_responses=True)
        self.db = redis.Redis(connection_pool=self.pool)

    def exists(self, proxy: Proxy) -> bool:
        """
        if proxy exists
        :param proxy: proxy
        :return: if exists, bool
        """
        return not self.db.zscore(REDIS_KEY, proxy.string()) is None

    def add(self,proxy:Proxy, score=PROXY_SCORE_INIT):
        if not is_valid_proxy(proxy.string()):
            logger.info(f'invalid proxy {proxy.string()},throw it')
            return
        elif(not self.exists(proxy)):
            return self.db.zadd(REDIS_KEY,{proxy.string(): score})

    
    def decrease(self, proxy: Proxy) -> int:
        """
        decrease score of proxy, if small than PROXY_SCORE_MIN, delete it
        :param proxy: proxy
        :return: new score
        """

        self.db.zincrby(REDIS_KEY, -1, proxy.string())
        score = self.db.zscore(REDIS_KEY, proxy.string())
        logger.info(f'{proxy.string()} score decrease 1, current {score}')
        if score <= PROXY_SCORE_MIN:
            logger.info(f'{proxy.string()} current score {score}, remove')
            self.db.zrem(REDIS_KEY, proxy.string())

    def max(self, proxy: Proxy) -> int:
        """
        set proxy to max score
        :param proxy: proxy
        :return: new score
        """
        logger.info(f'{proxy.string()} is available, set to {PROXY_SCORE_MAX}')
        return self.db.zadd(REDIS_KEY, {proxy.string(): PROXY_SCORE_MAX})

    def count(self) -> int:
        """
        get count of proxies
        :return: count, int
        """
        return self.db.zcard(REDIS_KEY)

    def random(self) -> Proxy:
        """
        get random proxy
        firstly try to get proxy with max score
        if not exists, try to get proxy by rank
        if not exists, raise error
        :return: proxy, like 8.8.8.8:8
        """
        # try to get proxy with max score
        proxies = self.db.zrangebyscore(
            REDIS_KEY, PROXY_SCORE_MAX, PROXY_SCORE_MAX)
        if len(proxies):
            return convert_proxy_or_proxies(choice(proxies))
        # else get proxy by rank
        proxies = self.db.zrevrange(
            REDIS_KEY, PROXY_SCORE_MIN, PROXY_SCORE_MAX)
        if len(proxies):
            return convert_proxy_or_proxies(choice(proxies))
        # else raise error
        raise PoolEmptyException

    def random_with_score(self) -> Proxy:
        """
        get random proxy
        firstly try to get proxy with max score
        if not exists, try to get proxy by rank
        if not exists, raise error
        :return: proxy, like 8.8.8.8:8
        """
        # try to get proxy with max score
        proxies = self.db.zrangebyscore(
            REDIS_KEY, PROXY_SCORE_MAX, PROXY_SCORE_MAX,withscores=True)
        if len(proxies):
            return convert_proxy_or_proxies_withscore(choice(proxies))
        # else get proxy by rank
        proxies = self.db.zrevrange(
            REDIS_KEY, PROXY_SCORE_MIN, PROXY_SCORE_MAX,withscores=True)
        if len(proxies):
            return convert_proxy_or_proxies_withscore(choice(proxies))
        # else raise error
        raise PoolEmptyException



    def all(self) -> List[Proxy]:
        """
        get all proxies
        :return: list of proxies
        """
        return convert_proxy_or_proxies(self.db.zrevrangebyscore(REDIS_KEY, PROXY_SCORE_MAX, PROXY_SCORE_MIN))
    
    def all_withscore(self) -> List[Proxy]:
        """
        get all proxies
        :return: list of proxies
        """
        return convert_proxy_or_proxies_withscore(self.db.zrevrangebyscore(REDIS_KEY, PROXY_SCORE_MAX, PROXY_SCORE_MIN,withscores=True))

    def count(self) -> int:
        """
        get count of proxies
        :return: count, int
        """
        return self.db.zcard(REDIS_KEY)
    
    def batch(self, cursor, count) -> List[Proxy]:
        """
        get batch of proxies
        :param cursor: scan cursor
        :param count: scan count
        :return: list of proxies
        """
        cursor, proxies = self.db.zscan(REDIS_KEY, cursor, count=count)
        return cursor, convert_proxy_or_proxies([i[0] for i in proxies])


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.random()
    print(result)
