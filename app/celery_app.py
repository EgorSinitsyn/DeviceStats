import os
from celery import Celery

# REDIS_HOST = os.getenv("REDIS_HOST", "localhost") # локальный тест
REDIS_HOST = os.getenv("REDIS_HOST", "redis")  # docker-compose
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

celery_app = Celery(
    "device_stats",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    include=["tasks"] # при локальном тесте можно убрать, но в docker-compose нужно
)

