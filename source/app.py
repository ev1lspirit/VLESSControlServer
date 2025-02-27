from functools import partial
import aioredis
import uvicorn
from fastapi import FastAPI
from config import Config
from log import setup_logging
from middlewares import access_log_middleware
from source.api import include_routers
import logging
from contextlib import asynccontextmanager

from source.utils.redis_utils import get_redis_app

setup_logging("app.log")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def app_lifespan(_: FastAPI):
    redis_app = get_redis_app()
    await redis_app.startup()
    logger.info(f"Redis connection created: {Config.REDIS_HOST_ADDR}:{Config.REDIS_PORT}")
    yield
    logger.info("Redis connection closed.")
    await redis_app.shutdown()


app = FastAPI(lifespan=app_lifespan)
include_routers(app)
app.middleware("http")(access_log_middleware)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        app="source.app:app",
        host="127.0.0.1",
        port=Config.FASTAPI_PORT,
        access_log=False,
        reload=True,
        workers=Config.FASTAPI_WORKERS_COUNT,
    )