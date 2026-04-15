from celery import Celery
import os

celery = Celery(
    "taskflow",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    include=["app.tasks.notifications"]
)

celery.conf.timezone = "UTC"