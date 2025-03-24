from fastapi_mail import ConnectionConfig
from app.utils.settings import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_USERNAME,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_PORT=465,
    USE_CREDENTIALS=True,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
)