import logging
from dataclasses import dataclass
from pathlib import Path
from environs import Env

PROJECT_DIR = Path(__file__).parent


# Инициализация объекта Env и чтение конфигурации из файла .env
env = Env()
try:
    env.read_env(Path(PROJECT_DIR, r'deployments/.env'))
except OSError:
    pass


@dataclass
class Config:
    VLESS_CONFIGURATION_PATH: str = env("VLESS_CONFIGURATION_PATH")
    VLESS_CONFIGURATION_PUBLIC_KEY: str = env("VLESS_CONFIGURATION_PUBLIC_KEY")
    VLESS_CONFIGURATION_PATH_WIN: str = env("VLESS_CONFIGURATION_PATH_WIN")
    VLESS_HOST_IP: str = env("VLESS_HOST_IP")

    LOGS_DIR = Path(PROJECT_DIR, "logs")
    APP_LOGS_FILE = Path(LOGS_DIR, "app.log")

    VLESS_LOG_DIR: str = env("VLESS_LOG_DIR")
    VLESS_ACCESS_LOG_PATH: Path = Path(VLESS_LOG_DIR, "access.log")
    VLESS_ERROR_LOG_PATH: Path = Path(VLESS_LOG_DIR, "error.log")

    SERVER_ALIAS = env("SERVER_ALIAS")
    SERVER_IP = env("SERVER_IP")

    CONTROL_AUTH_LOGIN = env("CONTROL_AUTH_LOGIN")
    CONTROL_AUTH_PASS_HASH = env("CONTROL_AUTH_PASS_HASH")

    SESSION_LIFETIME_MIN = env.int("SESSION_LIFETIME_MIN")
    PRIVATE_KEY_FILE: Path = PROJECT_DIR.joinpath(env("PRIVATE_KEY_FILE"))
    PUBLIC_KEY_FILE: Path = PROJECT_DIR.joinpath(env("PUBLIC_KEY_FILE"))
    PRIVATE_KEY: str = PRIVATE_KEY_FILE.read_text().strip()
    PUBLIC_KEY: str = PUBLIC_KEY_FILE.read_text().strip()

    REDIS_HOST_ADDR: str = env("REDIS_HOST_ADDR")
    REDIS_PORT: int = env.int("REDIS_PORT")
    REDIS_PASS: str = env("REDIS_PASS")
    FASTAPI_PORT = 8000

    FASTAPI_WORKERS_COUNT: int = env.int("FASTAPI_WORKERS_COUNT")