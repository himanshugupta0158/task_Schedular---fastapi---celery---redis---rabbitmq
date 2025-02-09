# app/celery_app.py
from celery import Celery
from app.config import (
    RABBITMQ_HOST,
    RABBITMQ_DEFAULT_USER,
    RABBITMQ_DEFAULT_PASS,
    REDIS_HOST,
)

broker_url = f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOST}//"
result_backend = f"redis://{REDIS_HOST}:6379/0"

celery_app = Celery("tasks", broker=broker_url, backend=result_backend)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Import tasks so that they get registered.
import app.tasks
