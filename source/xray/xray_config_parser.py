import json
from contextlib import asynccontextmanager
from functools import partial

import aiofiles
from pydantic import ValidationError
import typing as tp
from config import Config
import logging

from source.api.server.schema import AddClientToConfigBody
from source.helpers import handle_exception
from source.utils.console_utils import always_restart_xray, restart_xray
from source.xray.models import XrayConfigurationModel, LoadedXrayConfigurationOutput, ClientModel

logger = logging.getLogger(__name__)
conf_parser_handle_exception = partial(handle_exception, logger=logger)


def vless_url(**kwargs):
    return ("vless://{uuid}@{host}:{port}?security=reality&sni={SNI}&alpn={alpn}"
            "&fp=chrome&pbk={pbk}&sid={SID}&type=tcp&flow=xtls-rprx-vision&encry"
            "ption=none#VLESS VPN (TG:@sweeetferrero)".format_map(kwargs))


class VlessConfigurationParser:

    def __init__(self, configuration: dict):
        self.configuration = configuration

    @property
    def configuration(self) -> tp.Optional[XrayConfigurationModel]:
        return self.__loaded_configuration

    @configuration.setter
    @conf_parser_handle_exception(exception_class=ValidationError, msg="Validation error occurred; Couldn't load XRay configuration: {str_exc}")
    def configuration(self, config_json: dict | None) -> None:
        if config_json is None:
            self.__loaded_configuration = None
            return
        self.__loaded_configuration = XrayConfigurationModel(**config_json)

    def add_user_to_configuration(self, client_model: AddClientToConfigBody) -> None:
        clients = self.configuration.inbounds[0].settings.clients
        client_model = ClientModel(**(client_model.model_dump()))
        clients.append(client_model)

    def delete_user_from_configuration(self, client_id: str) -> None:
        clients = self.configuration.inbounds[0].settings.clients
        records = list(filter(lambda client: client.id != client_id, clients))
        self.configuration.inbounds[0].settings.clients = records

    def get_client(self, client_id: str) -> ClientModel | None:
        clients = self.configuration.inbounds[0].settings.clients
        return next(filter(lambda client: client.id == client_id, clients), None)

    @conf_parser_handle_exception(exception_class=ValidationError, msg="Validation error occurred while getting server credentials: {str_exc}")
    def get_server_credentials(self) -> tp.Optional[LoadedXrayConfigurationOutput]:
        if self.configuration is None:
            raise ValueError("Can't parse credentials. Use context manager to load credentials")

        reality_settings = self.configuration.inbounds[0].streamSettings.realitySettings
        sni, _ = reality_settings.dest.split(':')
        response_model = LoadedXrayConfigurationOutput(
            SNI=sni,
            SID=reality_settings.shortIds[0],
            pbk=Config.VLESS_CONFIGURATION_PUBLIC_KEY,
            port=self.configuration.inbounds[0].port
        )
        return response_model


@asynccontextmanager
async def get_configuration_parser() -> tp.AsyncGenerator[VlessConfigurationParser, None, None]:
    try:
        async with aiofiles.open(Config.VLESS_CONFIGURATION_PATH_WIN) as file:
            try:
                configuration_json = json.loads(await file.read())
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON from {Config.VLESS_CONFIGURATION_PATH_WIN}: {e}")
            except IOError as e:
                logger.error(f"Error reading from file: {str(e)}")
                raise IOError(f"Error reading from file: {str(e)}")

        conf_parser = VlessConfigurationParser(configuration_json)
        yield conf_parser

        async with aiofiles.open(Config.VLESS_CONFIGURATION_PATH_WIN, mode="w", encoding="utf-8") as file:
            try:
                configuration_json = conf_parser.configuration
                await file.write(configuration_json.model_dump_json(indent=4))
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON from {Config.VLESS_CONFIGURATION_PATH_WIN}: {e}")
                raise ValueError(f"Error parsing JSON from {Config.VLESS_CONFIGURATION_PATH_WIN}: {e}")
            except IOError as e:
                logger.error(f"Error writing to file {Config.VLESS_CONFIGURATION_PATH_WIN}: {str(e)}")
        restart_xray()

    except Exception as e:
        logger.error(f"An error occurred in the configuration context manager: {str(e)}")
        raise  # Re-raise the exception after handling
