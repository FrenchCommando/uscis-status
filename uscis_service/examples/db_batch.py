import asyncio
import sys
import time
import datetime
from gmail.gmail_functions import send
from src.update_functions import \
    refresh_error, delete_entries, smart_update_all, refresh_status, clear_uscis_table, refresh_selected_status


def refresh_error_function():
    asyncio.get_event_loop().run_until_complete(refresh_error())


def delete_entries_function(argv):
    clean_args = [argv] if isinstance(argv, str) else argv
    asyncio.get_event_loop().run_until_complete(delete_entries(clean_args))


def smart_update(argv):
    d = dict(
        prefix=argv[0],
        year_start=int(argv[1]),
        day_start=int(argv[2]),
        skip_recent_threshold=int(argv[3]),
        chunk_size=int(argv[4]),
    )
    asyncio.get_event_loop().run_until_complete(smart_update_all(**d))


def refresh_status_function(argv):
    asyncio.get_event_loop().run_until_complete(refresh_status(
        status=" ".join(argv[:-2]),
        skip_recent_threshold=int(argv[-2]),
        chunk_size=int(argv[-1]),
    ))


def refresh_selected_status_function(argv):
    asyncio.get_event_loop().run_until_complete(refresh_selected_status(
        filter_function=lambda x: 0 < x < int(argv[-2]),
        skip_recent_threshold=int(argv[-1]),
    ))


def clear_table():
    asyncio.get_event_loop().run_until_complete(clear_uscis_table())


def main(argv, retry=0, main_init_time=None, error_msg=None):
    init_time = datetime.datetime.now()
    main_init_time_val = init_time if main_init_time is None else main_init_time
    send(subject="db_batch is starting",
         body=f"{argv}\n"
              f"Retry number:\t{retry}\n"
              f"init time:\t{init_time}\n"
              f"main init time:\t{main_init_time_val}\n"
              f"errors:\t{error_msg}"
         )
    try:
        function_name = argv[0]
        if function_name == "delete":
            delete_entries_function(argv=argv[1:])
        elif function_name == "refresh_errors":
            refresh_error_function()
        elif function_name == "refresh_status":
            refresh_status_function(argv=argv[1:])
        elif function_name == "refresh_selected_status":
            refresh_selected_status_function(argv=argv[1:])
        elif function_name == "smart_update":
            smart_update(argv=argv[1:])
        elif function_name == "clear":
            clear_table()
        else:
            print(f"Function name did not match:\t{function_name}")
        end_time = datetime.datetime.now()
        send(subject="db_batch have run",
             body=f"{argv}\n"
                  f"Retry number:\t{retry}\n"
                  f"init time:\t{init_time}\n"
                  f"end time:\t{end_time}\n"
                  f"elapsed:\t{end_time - init_time}\n"
                  f"main elapsed:\t{end_time - main_init_time_val}\n"
             )
    except BaseException as e:
        if retry > 3:
            end_time = datetime.datetime.now()
            send(subject="db_batch - Aborted - Too many retries",
                 body=f"{argv}\n"
                      f"Retry number:\t{retry}\n"
                      f"init time:\t{init_time}\n"
                      f"end time:\t{end_time}\n"
                      f"elapsed:\t{end_time - init_time}\n"
                      f"main elapsed:\t{end_time - main_init_time_val}\n"
                      f"errors:\t{e}"
                 )
            return print(f"Error\tNot retrying - too many retries\t{argv}\t{__name__}{e}")
        n_secs = 30
        print(f"Error\trestarting in {n_secs}s\t{argv}\t{__name__}{e}")
        time.sleep(n_secs)
        print(f"Error\trestarting now\t{argv}\t{__name__}{e}")
        main(argv=argv, retry=retry + 1, main_init_time=main_init_time_val, error_msg=e)


if __name__ == "__main__":
    main(sys.argv[1:])
