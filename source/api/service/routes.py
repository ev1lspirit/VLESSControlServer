import logging
from dataclasses import asdict
from functools import partial
from fastapi import APIRouter, Query, Depends
from starlette.responses import JSONResponse
from config import Config
from source.api.service.schema import XRayStatusResponse
from source.helpers import handle_exception, CommandResponse
from source.utils.console_utils import check_xray_status
from source.utils.files_utils import read_last_n_records

router = APIRouter(prefix="/service", tags=["Service"])
logger = logging.getLogger(__name__)

handle_exception = partial(handle_exception, logger=logger)


@router.get("/xray_server_healthcheck", response_model=XRayStatusResponse)
async def xray_server_healthcheck_handler(command_response: CommandResponse = Depends(check_xray_status)):
    if command_response is None:
        return XRayStatusResponse(execution_result_code=-1, details="An unexpected error occurred. Please check logs.")
    return XRayStatusResponse(**asdict(command_response))


@router.get("/export_app_logs")
async def export_app_logs_handler(tail_n: int = Query(..., ge=1)):
    logs = await read_last_n_records(path=Config.APP_LOGS_FILE, tail_n=tail_n)
    return JSONResponse({"response": logs})


