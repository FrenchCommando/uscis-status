from apscheduler.schedulers.blocking import BlockingScheduler
from examples.db_batch import main as batch_main
import asyncio
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())


def refresh_job():
    batch_main(["refresh_errors"])


def case_status_job():
    batch_main(["refresh_status", "CASE", "STATUS", "0", "10"])


def smart_job():
    batch_main(["smart_update", "LIN", "20", "0", "18", "10"])


def smart_date_job():
    batch_main(["smart_update", "LIN", "20", "1", "18", "10"])


def main():
    scheduler = BlockingScheduler()
    scheduler.configure(job_defaults=dict(max_instances=5))
    scheduler.add_job(refresh_job, 'cron', hour='1-23/6', minute=30)
    scheduler.add_job(case_status_job, 'cron', day_of_week=1, hour=16)
    scheduler.add_job(smart_job, 'cron', day_of_week=3, hour=0)
    scheduler.add_job(smart_date_job, 'cron', day_of_week=5, hour=8)
    scheduler.start()


if __name__ == "__main__":
    main()
