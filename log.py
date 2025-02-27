import logging
import os
from config import Config


def setup_logging(log_filename: str):
    """
    Настройка логирования с использованием dictConfig.
    :param log_filename: Имя файла для записи логов.
    """
    log_dir = Config.LOGS_DIR
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_path = os.path.join(log_dir, log_filename)

    # Словарь конфигурации логирования
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'generic': {
                'format': '{asctime} [{levelname}] [{name:^16}] {message}',
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'generic',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'maxBytes': 1024 * 1024,
                'backupCount': 20,
                'formatter': 'generic',
                'filename': log_path,
            },
        },
        'loggers': {
            'root': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
            },
            'sqlalchemy': {
                'level': 'WARNING',
                'handlers': ['console'],
                'qualname': 'sqlalchemy.engine',
            },
            'alembic': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'qualname': 'alembic',
            },
        },
    }
    logging.config.dictConfig(log_config)
