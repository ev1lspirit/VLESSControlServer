import logging

from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from starlette.responses import JSONResponse

from config import Config
from source.api.server.schema import GetConnectionLinkBody, AddClientToConfigBody, DeleteClientFromConfigBody
from source.utils.auth_utils import check_jwt_auth
from source.xray.models import LoadedXrayConfigurationOutput
from source.xray.xray_config_parser import get_configuration_parser, VlessConfigurationParser, vless_url

router = APIRouter(prefix="/xray", tags=["XRay"], dependencies=[Depends(check_jwt_auth)])
logger = logging.getLogger(__name__)


@router.post("/get_connection_link")
async def load_conf_handler(body: GetConnectionLinkBody) -> JSONResponse:
      conf_parser: VlessConfigurationParser
      async with get_configuration_parser() as conf_parser:
            if not conf_parser.get_client(body.id):
                  raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail="User with such uuid not found"
                  )
            credentials_model: LoadedXrayConfigurationOutput = conf_parser.get_server_credentials()

      fields = {"uuid": body.id, "host": Config.VLESS_HOST_IP}
      fields.update(credentials_model.model_dump())
      return JSONResponse(content={"response": vless_url(**fields)})


@router.post("/add_user")
async def add_user_to_configuration_handler(body: AddClientToConfigBody) -> JSONResponse:
      conf_parser: VlessConfigurationParser
      async with get_configuration_parser() as conf_parser:
            if conf_parser.get_client(body.id) is not None:
                  raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="User with this id already exists"
                  )
            conf_parser.add_user_to_configuration(
                  client_model=body
            )
      logger.info("User with id = {id} and email = {email} has been added.".format_map(body.model_dump()))
      return JSONResponse(content={"response": body.model_dump()})


@router.post("/delete_user")
async def add_user_to_configuration_handler(body: DeleteClientFromConfigBody) -> JSONResponse:
      conf_parser: VlessConfigurationParser
      async with get_configuration_parser() as conf_parser:
            if conf_parser.get_client(body.id) is None:
                  raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail="User with such uuid not found"
                  )
            conf_parser.delete_user_from_configuration(
                  client_id=body.id
            )
      logger.info(f"Client with id {body.id} has been deleted.")
      return JSONResponse(content={"response": f"Client with id {body.id} has been deleted."})

