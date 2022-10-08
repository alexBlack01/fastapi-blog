from pydantic import BaseSettings, Field, HttpUrl, RedisDsn


class InfrastructureConfig(BaseSettings):
    postgres_dsn = 'postgresql://fastapi_blog:fastapi_blog@database_blog:5432'
    postgres_db_name: str = 'fastapi_blog'


infrastructure_config = InfrastructureConfig()
