from pydantic_settings import BaseSettings
from decouple import config
import os

class Settings(BaseSettings):
    PORT: int = config("PORT", cast=int)
    CLIENT_URL: str = config("CLIENT_URL")
    PASSWORD_RESET_SECRET: str = config("PASSWORD_RESET_SECRET")

    """Database Settings"""
    DB_URL: str = config("DB_URL")

    """JWT Settings"""
    JWT_SECRET: str = config("JWT_SECRET")
    ALGORITHM: str = config("ALGORITHM")

    """Email Settings"""
    MAIL_USERNAME: str = config("MAIL_USERNAME")
    MAIL_PASSWORD: str = config("MAIL_USERNAME")
    MAIL_FROM: str = config("MAIL_USERNAME")
    MAIL_PORT: int = config("MAIL_PORT", cast=int)
    MAIL_SERVER: str = config("MAIL_SERVER")

    """Cloudinary Settings"""
    CLOUDINARY_CLOUD_NAME: str = config("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY: str = config("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET: str = config("CLOUDINARY_API_SECRET")



settings = Settings()