import logging
from collections import deque
from functools import partial
from pathlib import Path
import aiofiles
from source.helpers import handle_exception

logger = logging.getLogger(__name__)
files_utils_handle_exception = partial(handle_exception, logger=logger)


@files_utils_handle_exception
@files_utils_handle_exception(exception_class=IOError)
@files_utils_handle_exception(exception_class=FileNotFoundError)
async def read_last_n_records(path: Path, tail_n: int) -> list[str] | None:
    async with aiofiles.open(path, mode='r', encoding='utf-8') as file:
        logs = list(deque(await file.readlines(), maxlen=tail_n))
    return logs
