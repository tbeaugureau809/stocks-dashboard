from apscheduler.schedulers.background import BackgroundScheduler
from app.services.history_service import backfill_history


scheduler = BackgroundScheduler()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            func=backfill_history,
            trigger="cron",
            hour=2,
            id="nightly_backfill",
            replace_existing=True,
    )

        scheduler.start()
