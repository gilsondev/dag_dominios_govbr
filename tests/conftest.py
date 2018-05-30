"""
Database fixture configuration based on the gist:

https://gist.github.com/kissgyorgy/e2365f25a213de44b9a2
"""
import os
import pytest

from sqlalchemy.orm import sessionmaker, Session

from dag_dominios_govbr.core.database import (
    Base,
    database_connect,
    create_tables,
    drop_tables
)


@pytest.fixture(scope='session')
def engine():
    db_url = 'sqlite:///:memory:'
    engine = database_connect(
        database_url=os.getenv('DATABASE_URL', db_url)
    )
    return engine


@pytest.yield_fixture(scope='session')
def tables(engine):
    create_tables(engine)
    yield
    drop_tables(engine)


@pytest.yield_fixture
def session(engine, tables):

    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
