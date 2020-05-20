from src.constants import uscis_table_name, status_table_name, user_table_name
table_to_specs = {
    uscis_table_name:
        "id serial PRIMARY KEY, case_number text, timestamp text, response_title text, response_content text",
    status_table_name: "status_type text, status_message text",
    user_table_name: "email text, case_watched text",
}
