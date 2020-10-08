from apscheduler.schedulers.blocking import BlockingScheduler
import asyncio
from examples.db_batch import refresh_error


scheduler = BlockingScheduler()


def main():
    i = 0

    def some_job():
        global i
        print("Decorated job")
        print(i)
        i += 1

    def some_other_job():
        print(i, "the other one")
        asyncio.get_event_loop().run_until_complete(refresh_error())

    scheduler.add_job(some_job, 'interval', minutes=1)
    scheduler.add_job(some_other_job, 'interval', minutes=1)
    scheduler.start()


if __name__ == '__main__':
    main()
