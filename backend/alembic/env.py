from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models.base import Base
from app.models.user_orm import UserORM
from app.config.loader import ConfigLoader

# Load .env and resolve project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Alembic config object
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
target_metadata = Base.metadata

# Load DB URL dynamically
db_url = ConfigLoader().get_database_url()

def run_migrations_offline() -> None:
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        url=db_url,  # <-- Inject the dynamic DB URL here
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # detect column type changes
        )

        with context.begin_transaction():
            context.run_migrations()

# Run offline/online based on mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
