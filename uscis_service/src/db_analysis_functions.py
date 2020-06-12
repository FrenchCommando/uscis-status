from collections import defaultdict
import datetime
from src.constants import uscis_database, uscis_table_name
from src.db_stuff import connect_to_database, get_all
from src.message_stuff import string_to_args


def find_strips(id_list, print_results=True):
    # Finds all consecutive sequences
    print(f"Number of elements:\t{len(id_list)}")
    # of course sorting solves the question
    # ignore trailing zeros issues

    def parsed_case():
        for case in sorted(id_list):
            yield case[:3], int(case[3:])

    def process(v_prefix, v_index, v_length):
        new_prefix, new_index = next(it)
        if new_prefix == v_prefix and new_index == v_index + v_length:
            v_length += 1
            return v_prefix, v_index, v_length
        else:
            records[f"{v_prefix}{v_index}"] = v_length
            return new_prefix, new_index, 1

    records = {}  # contains starting index, length of consecutive sequence
    it = parsed_case()

    prefix, index = next(it)
    length = 1

    try:
        while True:
            prefix, index, length = process(prefix, index, length)
    except StopIteration:
        records[f"{prefix}{index}"] = length
    if print_results:
        for k, v in records.items():
            print(k, v)
    print(f"Number of strips:\t{len(records)}")
    print(f"Longest strip:\t{max(records.values())}")
    print(f"Check Sum is consistent:\t{sum(records.values())} vs {len(id_list)}\n")
    return records


def prefix_buckets(id_list, print_results=True):
    print(f"Number of elements:\t{len(id_list)}")

    def parsed_case():
        for case in id_list:
            if case[5] == "9":
                yield case[:3], int(case[3:5]), 900, int(case[6:])
            else:
                yield case[:3], int(case[3:5]), int(case[5:8]), int(case[8:])

    records = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for prefix, year, date, index in parsed_case():
        records[prefix][year][date] += 1

    if print_results:
        i = 0
        for prefix, v in sorted(records.items()):
            i_prefix = 0
            for year, w in sorted(v.items()):
                i_year = 0
                for date, index in sorted(w.items()):
                    print(f"{prefix}\t{year}\t{date:03d}:\t{index:05d}")
                    i += index
                    i_prefix += index
                    i_year += index
                print(f"{prefix}\t{year}:\t{i_year}")
            print(f"{prefix}:\t{i_prefix}")
            print()
        print(f"Check Sum is consistent:\t{i} vs {len(id_list)}\n")
    return records


async def summary_analysis(custom_filter=lambda x: True, print_results=True, buckets_instead_of_strip=True):
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn:
            all_data = await get_all(conn=conn, table_name=uscis_table_name, ignore_null=True)
            all_data = [u for u in all_data if custom_filter(u)]
            all_cases = [row['case_number'] for row in all_data]

            if not buckets_instead_of_strip:
                find_strips(id_list=all_cases, print_results=print_results)
                # looks like there are some holes in the cheese
            else:
                prefix_buckets(id_list=all_cases, print_results=print_results)
    finally:
        await pool.close()


def filter_form(ref):
    def select_form(line):
        current_args = line["current_args"]
        d = string_to_args(s=current_args)
        form_name = d.get('form_long_name', "")
        return form_name == ref
    return select_form


def filter_status(ref):
    def select_status(line):
        current_status = line["current_status"]
        return current_status == ref
    return select_status


async def summary_analysis_form(ref_form, **kwargs):
    return await summary_analysis(custom_filter=filter_form(ref=ref_form), **kwargs)


async def summary_analysis_status(ref_status, **kwargs):
    return await summary_analysis(custom_filter=filter_status(ref=ref_status), **kwargs)


async def count_date_status_function(conn):
    records = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    all_data = await get_all(conn=conn, table_name=uscis_table_name, ignore_null=True)
    for line in all_data:
        current_status = line["current_status"]
        current_args = line["current_args"]
        d = string_to_args(s=current_args)
        if current_status == "Case Was Reopened":
            phrasing = " ".join([d.get('phrasing_1', ""), d.get('form_long_name', "")])
            real_form = phrasing.split("Form")[-1]
            form_name = f"Form{real_form}"
        else:
            form_name = d.get('form_long_name', "")
        # print(d['date'] if 'date' in d else "")
        # print(line)
        date = datetime.datetime.strptime(d['date'], "%B %d, %Y").date() if 'date' in d else ""
        records[form_name][current_status][date] += 1
    for form, v in records.items():
        print(f"{form}:\t")
        for status, w in sorted(v.items(), key=lambda ww: sum(ww[-1].values())):
            print(f"\t\t{status}:\t")
            for date, count in sorted(w.items()):
                print(f"\t\t\t{date}:\t{count}", end="\t")
            print()
    print()
    return records


async def count_date_status():
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn:
            await count_date_status_function(conn=conn)
    finally:
        await pool.close()
