from celery import Celery

from src.config import settings

celery_instance = Celery(
    main="tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL, include=["src.tasks.tasks"]
)

celery_instance.conf.beat_schedule = {
    "luboe-nazvanie": {
        "task": "booking_today_checkin",
        "schedule": 5,  # sec or crotab syntax
    }
}
