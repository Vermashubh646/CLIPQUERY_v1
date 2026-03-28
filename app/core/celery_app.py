from celery import Celery

from app.core.config import settings

celery_worker = Celery('clipquery', broker=settings.REDIS_URL, backend=settings.REDIS_URL)