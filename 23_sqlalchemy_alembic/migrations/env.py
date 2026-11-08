"""Alembic runs this file for every command. It connects to the database and
tells Alembic which models describe the target schema (for --autogenerate)."""
import sys
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # so `import models` works
from models import Base  # noqa: E402

config = context.config
target_metadata = Base.metadata          # autogenerate compares the DB with these models


def run_migrations() -> None:
    connectable = config.attributes.get("connection") or engine_from_config(
        config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.",
        poolclass=pool.NullPool)
    if hasattr(connectable, "connect"):
        with connectable.connect() as connection:
            _run(connection)
    else:
        _run(connectable)


def _run(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata,
                      render_as_batch=True)      # batch mode: needed for ALTER TABLE on SQLite
    with context.begin_transaction():
        context.run_migrations()


run_migrations()
