from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_db: str  # Database name
    postgres_user: str  # Database user
    postgres_password: str  # Database password

    class Config:
        env_file = "./.env"  # Specify .env file for configuration


# Retrieve settings
settings = Settings()
