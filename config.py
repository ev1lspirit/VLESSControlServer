# -*- coding: utf-8 -*-
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv



PROJECT_DIR = Path(__file__).parent


# Инициализация объекта Env и чтение конфигурации из файла .env
load_dotenv(Path('C://Users/11/PycharmProjects/SberParsingKBFU/deployments', '.env'))

@dataclass
class Config:
    VLESS_CONFIGURATION_PATH: str = os.environ.get("VLESS_CONFIGURATION_PATH")
    VLESS_CONFIGURATION_PUBLIC_KEY: str = os.environ.get("VLESS_CONFIGURATION_PUBLIC_KEY")
    VLESS_CONFIGURATION_PATH_WIN: str = os.environ.get("VLESS_CONFIGURATION_PATH_WIN")
    VLESS_HOST_IP: str = os.environ.get("VLESS_HOST_IP")

    LOGS_DIR = Path(PROJECT_DIR, "logs")
    APP_LOGS_FILE = Path(LOGS_DIR, "app.log")

    VLESS_LOG_DIR: str = os.environ.get("VLESS_LOG_DIR")
    VLESS_ACCESS_LOG_PATH: Path = Path(VLESS_LOG_DIR, "access.log")
    VLESS_ERROR_LOG_PATH: Path = Path(VLESS_LOG_DIR, "error.log")

    SERVER_ALIAS = os.environ.get("SERVER_ALIAS")
    SERVER_IP = os.environ.get("SERVER_IP")

    CONTROL_AUTH_LOGIN = os.environ.get("CONTROL_AUTH_LOGIN")
    CONTROL_AUTH_PASS_HASH = os.environ.get("CONTROL_AUTH_PASS_HASH")

    SESSION_LIFETIME_MIN = int(os.environ.get("SESSION_LIFETIME_MIN"))
    PRIVATE_KEY_FILE: Path = PROJECT_DIR.joinpath(os.environ.get("PRIVATE_KEY_FILE"))
    PUBLIC_KEY_FILE: Path = PROJECT_DIR.joinpath(os.environ.get("PUBLIC_KEY_FILE"))
    #PRIVATE_KEY: str = PRIVATE_KEY_FILE.read_text().strip()
    #PUBLIC_KEY: str = PUBLIC_KEY_FILE.read_text().strip()

    REDIS_HOST_ADDR: str = os.environ.get("REDIS_HOST_ADDR")
    REDIS_PORT: int = int(os.environ.get("REDIS_PORT"))
    REDIS_PASS: str = os.environ.get("REDIS_PASS")
    FASTAPI_PORT = 8000

    FASTAPI_WORKERS_COUNT: int = int(os.environ.get("FASTAPI_WORKERS_COUNT"))