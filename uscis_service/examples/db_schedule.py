from apscheduler.schedulers.blocking import BlockingScheduler
from examples.db_batch import main as batch_main
import asyncio
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())


def some_other_job():
    batch_main(["refresh_errors"])


def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(some_other_job, 'interval', seconds=5)
    scheduler.start()


if __name__ == "__main__":
    main()
