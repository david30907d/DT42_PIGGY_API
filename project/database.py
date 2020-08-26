"""
Define schema of Table
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL

URI = URL(
    drivername="postgresql",
    username=os.environ.get("POSTGRES_USER", "postgres"),
    password=os.environ.get("POSTGRES_PASSWORD", "postgres"),
    host=os.environ.get("POSTGRES_SERVICE_HOST", "postgres"),
    port=os.environ.get("POSTGRES_SERVICE_PORT", 5432),
    database=os.environ.get("POSTGRES_DB", "postgres"),
)
ENGINE = create_engine(URI, pool_recycle=180, connect_args={"connect_timeout": 300})
SESSION = scoped_session(sessionmaker(bind=ENGINE))
