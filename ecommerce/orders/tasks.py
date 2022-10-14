from . import mail
from celery import Celery
from ..config import settings


celery_app = Celery(
    'celery_app',
    broker=f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}",
    backend=f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}"
)


@celery_app.task
def send_email(email):
    return mail.order_notification(email)
