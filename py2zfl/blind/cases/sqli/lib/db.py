"""Connection helpers shared by the handlers in this package."""
import os
import sqlite3

import psycopg2
from sqlalchemy import create_engine

SQLITE_PATH = os.environ.get("APP_SQLITE_PATH", "app.db")
PG_DSN = os.environ.get("APP_PG_DSN", "dbname=app user=app host=localhost")

engine = create_engine(os.environ.get("APP_DATABASE_URL", "sqlite:///app.db"), future=True)


def get_connection():
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_pg():
    return psycopg2.connect(PG_DSN)
