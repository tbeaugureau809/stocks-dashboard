from apscheduler.schedulers.background import BackgroundScheduler
from app.services.history_service import backfill_history
import time

scheduler = BackgroundScheduler()

def ping():
    print(f"[{time.strftime('%X')}] Scheduler alive")

def start_scheduler():
    scheduler.add_job(
        func=ping,
        trigger="interval",
        seconds=30,
        id="ping_job",
        replace_existing=True,
    )

    scheduler.add_job(
        func=backfill_history,
        trigger="cron",
        hour=2,
        id="nightly_backfill",
        replace_existing=True,
    )

scheduler.start()
