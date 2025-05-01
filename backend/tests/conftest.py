import pytest

from todo import db
from tortoise.transactions import in_transaction


@pytest.fixture
async def db_conn(db_setup):
    async with in_transaction() as conn:
        yield conn

        # isolate test cases with a rollback
        await conn.rollback()


@pytest.fixture(scope="session", autouse=True)
async def db_setup():
    # Official recipe in https://tortoise.github.io/contrib/unittest.html#py-test
    # does NOT work: https://github.com/tortoise/tortoise-orm/issues/1110

    await db.init(db_url="sqlite://:memory:")

    yield

    await db.close()


@pytest.fixture(scope="session", autouse=True)
def anyio_backend() -> str:
    # See https://anyio.readthedocs.io/en/stable/testing.html

    return "asyncio"
