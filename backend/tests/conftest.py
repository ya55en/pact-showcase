import pytest
from tortoise.transactions import in_transaction

from todo import db, orm


@pytest.fixture
async def db_conn(db_setup):
    async with in_transaction() as conn:
        yield conn

        # isolate test cases with a rollback
        await conn.rollback()


@pytest.fixture(scope='session')
async def seed_db(db_setup) -> None:
    await orm.seed_db()


@pytest.fixture(scope='session')
async def db_setup():
    # Official recipe in https://tortoise.github.io/contrib/unittest.html#py-test
    # does NOT work currently: https://github.com/tortoise/tortoise-orm/issues/1110

    await db.init(db_url='sqlite://:memory:')

    yield

    await db.close()


@pytest.fixture(scope='session', autouse=True)
def anyio_backend() -> str:
    # See https://anyio.readthedocs.io/en/stable/testing.html

    return 'asyncio'
