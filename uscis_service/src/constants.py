import os

IS_DOCKER = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

uscis_database = "uscis"

uscis_table_name = "uscis_table"
error_table_name = "error_table"

host = "db" if IS_DOCKER else "localhost"
pg_port_number = 5432  # port of pg service

port_number = 5000  # port to host server
