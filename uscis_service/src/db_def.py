from uscis_service.src.constants import uscis_table_name, error_table_name


table_to_specs = {
    uscis_table_name:
        "case_number text PRIMARY KEY, "
        "last_updated text, "
        "current_status text, "
        "current_args text, "
        "history text",
    error_table_name:
        "id serial PRIMARY KEY, "
        "title text, "
        "case_number text, "
        "message text ",
}
