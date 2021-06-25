from decouple import config
from flask_caching import Cache

from app.main.model.log import ApiLogger


class Config:
    DEBUG = False
    CACHE_TIMEOUT = config("CACHE_DEFAULT_TIMEOUT", cast=int)  # 3 minutes and 13 seconds caching
    CACHE_TYPE = "SimpleCache"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

cache = Cache()
logger = ApiLogger(
    logger_name=config("API_LOGGER_NAME"),
    record_log=config("API_LOGGER_RECORD_LOG", cast=bool),
    log_file_path=config("API_LOGGER_FILE_PATH")
)
