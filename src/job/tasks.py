from celery import Celery, schedules
from redbeat import RedBeatSchedulerEntry
from .worker import send_email_to_user, send_weekly_email_to_user

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    redbeat_redis_url="redis://localhost:6379/0",
    include=["job.tasks"],
    broker_connection_retry_on_startup=True,
)


def create_weekly_email_entry(user_id: str):
    """
    creates scheduling for task
    """
    interval = schedules.crontab(minute=0, hour=0, day_of_week=0)
    entry = RedBeatSchedulerEntry(
        "weekly email", "tasks.send_weekly_email", interval, args=[user_id], app=celery
    )
    entry.save()


@celery.task
def send_email(expense_id: str):
    """
    Send email
    """
    send_email_to_user(expense_id)


@celery.task
def send_weekly_email(user_id: str):
    """
    Send weekly email to users
    """
    send_weekly_email_to_user(user_id)
