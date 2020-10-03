import asyncio
import sys
from gmail.gmail_functions import send
from src.update_functions import refresh_error, delete_entries, smart_update_all, refresh_status, clear_uscis_table


def refresh_error_function():
    asyncio.get_event_loop().run_until_complete(refresh_error())


def delete_entries_function(argv):
    clean_args = [argv] if isinstance(argv, str) else argv
    asyncio.get_event_loop().run_until_complete(delete_entries(clean_args))


def smart_update(argv):
    d = dict(
        prefix=argv[0],
        date_start=int(argv[1]),
        index_start=int(argv[2]),
        skip_recent_threshold=int(argv[3])
    )
    asyncio.get_event_loop().run_until_complete(smart_update_all(**d))


def refresh_status_function(argv):
    asyncio.get_event_loop().run_until_complete(refresh_status(
        status=" ".join(argv[:-1]), skip_recent_threshold=int(argv[-1])))


def clear_table():
    asyncio.get_event_loop().run_until_complete(clear_uscis_table())


def main(argv, retry=0):
    try:
        send(subject="db_batch is starting", body=f"{argv}")
        function_name = argv[0]
        if function_name == "delete":
            delete_entries_function(argv=argv[1:])
        elif function_name == "refresh_errors":
            refresh_error_function()
        elif function_name == "refresh_status":
            refresh_status_function(argv=argv[1:])
        elif function_name == "smart_update":
            smart_update(argv=argv[1:])
        elif function_name == "clear":
            clear_table()
        else:
            print(f"Function name did not match:\t{function_name}")
        send(subject="db_batch have run", body=f"{argv}")
    except BaseException as e:
        if retry > 10:
            return print(f"Error\tNot retrying - too many retries\t{argv}\t{__name__}{e}")
        print(f"Error\trestarting in 100s\t{argv}\t{__name__}{e}")
        asyncio.sleep(100)
        print(f"Error\trestarting now\t{argv}\t{__name__}{e}")
        main(argv=argv, retry=retry + 1)


if __name__ == "__main__":
    main(sys.argv[1:])
