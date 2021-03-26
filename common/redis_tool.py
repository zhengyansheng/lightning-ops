import redis
from django.conf import settings


class RedisTool(object):

    def __init__(self):
        pass

    @classmethod
    def get_redis_client(cls, db=0):
        redis_pool = redis.ConnectionPool(host=settings.REDIS_HOST,
                                          port=settings.REDIS_PORT,
                                          password=settings.REDIS_PASSWORD,
                                          db=db)

        redis_client = redis.Redis(connection_pool=redis_pool)
        return redis_client
