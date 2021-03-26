import redis
from django.conf import settings

pool = redis.ConnectionPool(
    host=settings.GLOBAL_CONFIG.REDIS_HOST,
    password=settings.GLOBAL_CONFIG.REDIS_PASSWORD,
    port=settings.GLOBAL_CONFIG.REDIS_PORT,
    decode_responses=True,
)
redis_object = redis.Redis(connection_pool=pool)
