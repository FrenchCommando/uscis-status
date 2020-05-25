from src.constants import uscis_table_name, status_table_name, user_table_name, form_table_name


table_to_specs = {
    # form_table_name: "form_number text PRIMARY KEY, form_message text",
    # status_table_name: "status_type text PRIMARY KEY, status_message text",
    uscis_table_name:
        "case_number text PRIMARY KEY, "
        "last_updated text, "
        "current_status text, "
        "current_args text, "
        "history text",
    # user_table_name: "email text, case_watched text",
}
