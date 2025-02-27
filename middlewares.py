import logging
import time
from fastapi import Request, Response


logger = logging.getLogger(__name__)


async def access_log_middleware(request: Request, call_next):
    """
    Middleware для логирования запросов к серверу.
    Выводит время, затраченное на выполнение запроса, метод запроса,
    URL, по которому сделан запрос, и статус результата выполнения запроса.
    """
    t = time.monotonic()
    status = None
    try:
        response: Response = await call_next(request)
        status = response.status_code
        return response
    except Exception:
        status = 500
        raise
    finally:
        t2 = time.monotonic()
        logger.info(
            "%.3f %s %s %s", t2 - t, request.method, request.url, status
        )
