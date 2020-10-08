from apscheduler.schedulers.blocking import BlockingScheduler
from examples.db_batch import refresh_error
scheduler = BlockingScheduler()


i = 0


def main():
    def some_job():
        global i
        print("Decorated job")
        print(i)
        i += 1

    scheduler.add_job(some_job, 'interval', minutes=1)
    scheduler.add_job(refresh_error, 'interval', minutes=1)
    scheduler.start()


if __name__ == '__main__':
    main()
