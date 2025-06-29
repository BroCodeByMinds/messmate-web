import os
import sys
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config.loader import ConfigLoader


def create_database_if_not_exists():
    # Load DB config
    db_config = ConfigLoader().get_database_config()
    print("db_config", db_config)
    dbname = db_config["name"]
    user = db_config["user"]
    password = db_config["password"]
    host = db_config["host"]
    port = db_config["port"]
    schema = db_config.get("schema", "public")

    # Connect to default DB to create target DB
    default_conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    default_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = default_conn.cursor()

    # Check if DB exists
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
    exists = cursor.fetchone()

    if not exists:
        print(f"Creating database '{dbname}'...")
        cursor.execute(f"CREATE DATABASE {dbname}")
    else:
        print(f"Database '{dbname}' already exists.")

    cursor.close()
    default_conn.close()

    # Connect to the target DB to create schema
    db_conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    db_cursor = db_conn.cursor()

    db_cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", (schema,))
    schema_exists = db_cursor.fetchone()

    if not schema_exists:
        print(f"Creating schema '{schema}'...")
        db_cursor.execute(f"CREATE SCHEMA {schema}")
    else:
        print(f"Schema '{schema}' already exists.")

    db_conn.commit()
    db_cursor.close()
    db_conn.close()

if __name__ == "__main__":
    create_database_if_not_exists()
