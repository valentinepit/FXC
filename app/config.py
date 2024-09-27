import logging

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    log_level: str = 'INFO'

    # ------ postgres settings ---------
    db_name: str = 'fxc'
    db_host: str = 'localhost'
    db_port: int = 5432
    db_user: str = 'user'
    db_password: str = 'password'

    # ------ rabbitmq settings ---------
    queue_name: str = 'incoming_transactions'
    rabbitmq_host: str = 'localhost'
    rabbitmq_port: int = 5672
    rabbitmq_user: str = 'user'
    rabbitmq_password: str = 'password'

    # ------ redis settings ---------
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: str = 'keydb'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.log_level.upper())
