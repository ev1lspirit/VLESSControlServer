import logging
import subprocess
from functools import wraps, partial
from source.helpers import CommandResponse, handle_exception

logger = logging.getLogger(__name__)
console_utils_handle_exception = partial(handle_exception, logger=logger)


@console_utils_handle_exception
@console_utils_handle_exception(exception_class=FileNotFoundError,
                                msg="systemctl is not available on this system.")
def restart_xray() -> CommandResponse:
    run_status = subprocess.run(
        ["systemctl", "restart", "xray"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if run_status.returncode == 0:
        return CommandResponse(execution_result_code=run_status.returncode,
                               details=run_status.stdout)

    # TODO: Notify admin if something went wrong
    return CommandResponse(execution_result_code=run_status.returncode,
                           details=run_status.stderr)


def always_restart_xray(coroutine):
    @wraps(coroutine)
    async def wrapper(*args, **kwargs):
        result = await coroutine(*args, **kwargs)
        restart_xray()
        return result
    return wrapper


@console_utils_handle_exception
@console_utils_handle_exception(exception_class=FileNotFoundError,
                                msg="systemctl is not available on this system.")
def check_xray_status() -> CommandResponse:
    xray_status = subprocess.run(
        ["systemctl", "status", "xray"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if xray_status.returncode == 0:
        return CommandResponse(execution_result_code=xray_status.returncode,
                               details=xray_status.stdout)
    return CommandResponse(execution_result_code=xray_status.returncode,
                           details=xray_status.stderr)
