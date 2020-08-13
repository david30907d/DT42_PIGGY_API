"""
Define schema of Table
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL

URI = URL(
    drivername="mysql+pymysql",
    username=os.environ.get("MYSQL_USER", "root"),
    password=os.environ.get("MYSQL_PASSWORD", "mysql"),
    host=os.environ.get("MYSQL_SERVICE_HOST", "localhost"),
    port=os.environ.get("MYSQL_SERVICE_PORT", 3306),
    database=os.environ.get("MYSQL_DB", "mysql"),
)
ENGINE = create_engine(URI, pool_recycle=180, connect_args={"connect_timeout": 300})
SESSION = scoped_session(sessionmaker(bind=ENGINE))
