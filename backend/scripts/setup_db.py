import os
import sys
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
    schema = db_config.get("schema", "master")

    print(f"Checking database '{dbname}' and schema '{schema}'...")

    # Step 1: Connect to default 'postgres' DB to check/create target DB
    default_conn = psycopg2.connect(
        dbname='postgres',
        user=user,
        password=password,
        host=host,
        port=port
    )
    default_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = default_conn.cursor()

    # Step 2: Check/create DB
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
    if cursor.fetchone() is None:
        print(f"✅ Creating database '{dbname}'...")
        cursor.execute(f'CREATE DATABASE "{dbname}"')
    else:
        print(f"ℹ️  Database '{dbname}' already exists.")

    cursor.close()
    default_conn.close()

    # Step 3: Connect to the target DB to check/create schema
    db_conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    db_cursor = db_conn.cursor()

    db_cursor.execute("SELECT 1 FROM information_schema.schemata WHERE schema_name = %s", (schema,))
    if db_cursor.fetchone() is None:
        print(f"✅ Creating schema '{schema}'...")
        db_cursor.execute(f'CREATE SCHEMA "{schema}"')  # Removed AUTHORIZATION clause
    else:
        print(f"ℹ️  Schema '{schema}' already exists.")

    db_conn.commit()
    db_cursor.close()
    db_conn.close()

    print("✅ Database and schema setup complete.")


if __name__ == "__main__":
    create_database_if_not_exists()
