from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    db_host: str = 'db'
    db_user: str = 'vstorozhenko'
    db_password: str = 'strongpassword'
    db_name: str = 'vstorozhenko'
    test_db_name: str = 'vstorozhenko'
    redis_host: str = os.getenv('DOCKER_REDIS_HOST', 'localhost')
    redis_port: str = '6379'
    redis_db: str = '0'


settings = Settings()
