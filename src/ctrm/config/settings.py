from typing import Any
from pydantic import EmailStr, validator
from pydantic_settings import BaseSettings
from functools import lru_cache
from fastapi_mail import ConnectionConfig


class Settings(BaseSettings):
    API_V1_STR: str
    PROJECT_NAME: str
    DATABASE_URL: str
    COLLECTION_NAME: str
    ACCESS_TOKEN_EXPIRE: int
    SECRET_KEY: str
    ALGORITHM: str

    SMTP_TLS: bool = True
    SMTP_PORT: int | None = None
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: EmailStr | None = None
    EMAILS_FROM_NAME: str | None = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: str | None, values: dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "src/ctrm/email-templates/build"
    EMAILS_ENABLED: bool | None = None

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore

    LOGGER_TOKEN: str

    class Config:
        env_file = ".env"


# @lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


class EmailSettings(ConnectionConfig):
    MAIL_USERNAME: str = settings.SMTP_USER
    MAIL_PASSWORD: str = settings.SMTP_PASSWORD
    MAIL_FROM: EmailStr = settings.EMAILS_FROM_EMAIL
    MAIL_PORT: int = settings.SMTP_PORT
    MAIL_SERVER: str = settings.SMTP_HOST
    MAIL_FROM_NAME: str = settings.EMAILS_FROM_NAME
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    TEMPLATE_FOLDER: str = settings.EMAIL_TEMPLATES_DIR
