import os

IS_DOCKER = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

uscis_database = "uscis"

uscis_table_name = "uscis_table"
error_table_name = "error_table"
test_uscis_table = f"test_{uscis_table_name}"

port_number = 5000
host = "db" if IS_DOCKER else "localhost"
pg_port_number = 5432
