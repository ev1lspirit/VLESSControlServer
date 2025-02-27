import asyncio
import logging
import typing as tp
from dataclasses import dataclass
from functools import wraps, partial
from source.utils.redis_utils import get_redis_app


def handle_exception(function: tp.Optional[tp.Callable] = None,
                     exception_class: tp.Type[Exception] = None, logger: logging.Logger = None,
                     msg: str = None):
    if function is None:
        return partial(handle_exception, exception_class=exception_class, logger=logger, msg=msg)

    if not isinstance(logger, logging.Logger):
        raise TypeError(f"Logger must have logging.Logger type")

    if exception_class is None:
        exception_class = Exception
    cls_name = exception_class.__name__
    if not isinstance(msg, str):
        msg = "{cls_name}: An error occurred {str_exc}"
    else:
        msg = " ".join(("{cls_name}: ", msg))

    @wraps(function)
    async def wrapper(*args, **kwargs):
        try:
            if asyncio.iscoroutinefunction(function):
                return await function(*args, **kwargs)
            return function(*args, **kwargs)
        except exception_class as e:
            redis_app = get_redis_app()
            str_exc = str(e)
            error_msg = msg.format_map({"cls_name": cls_name, "str_exc": str_exc})
            logger.error(
                error_msg
            )
            await redis_app.notify_bot_via_redis(message=error_msg)
    return wrapper


@dataclass
class CommandResponse:
    execution_result_code: int
    details: str
