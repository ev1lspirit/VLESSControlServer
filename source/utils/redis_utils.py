import datetime
import logging
import aioredis
from aioredis import Redis
from config import Config

logger = logging.getLogger(__name__)


class RedisMeta(type):
    __instance = None

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
        return self.__instance


class RedisInstance(metaclass=RedisMeta):

    def __init__(self, redis_host: str = Config.REDIS_HOST_ADDR, redis_pass: str = Config.REDIS_PASS, redis_port: int =Config.REDIS_PORT,
        max_connections: int = Config.FASTAPI_WORKERS_COUNT):
        self.redis_host = redis_host
        self.redis_pass = redis_pass
        self.redis_port = redis_port
        self.max_connections = max_connections

    @property
    def redis_conn(self):
        return self.__redis_conn

    @redis_conn.setter
    def redis_conn(self, value):
        if not isinstance(value, (Redis, type(None))):
            raise TypeError("Instance must be Redis")
        self.__redis_conn = value

    async def startup(self):
        self.redis_conn = await aioredis.from_url("redis://:{redis_pass}@{redis_host}:{redis_port}".format(
            redis_host=self.redis_host, redis_pass=self.redis_pass, redis_port=self.redis_port),
            max_connections=self.max_connections)

    async def shutdown(self):
        await self.redis_conn.close()

    async def notify_bot_via_redis(self, message: str, ip_: str = Config.SERVER_IP):
        logger.info(f"Sending message {message} to Redis {ip_}_channel...")
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        message = f"{timestamp}:{Config.SERVER_ALIAS}:{message.strip()}"
        await self.redis_conn.publish(f"{ip_}_channel", message)


def get_redis_app(**kwargs):
    return RedisInstance(**kwargs)
