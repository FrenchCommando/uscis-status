from apscheduler.schedulers.blocking import BlockingScheduler
from examples.db_batch import refresh_error


scheduler = BlockingScheduler()


def main():
    i = 0

    def some_job():
        global i
        print("Decorated job")
        print(i)
        i += 1

    j = 0

    def some_other_job():
        print(j)
        j += 1

    scheduler.add_job(some_job, 'interval', minutes=1)
    scheduler.add_job(some_other_job, 'interval', minutes=1)
    scheduler.start()


if __name__ == '__main__':
    main()
