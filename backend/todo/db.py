from tortoise import Tortoise

import todo.orm


async def init(db_url, modules=None, generate_schemas=True) -> None:
    if modules is None:
        modules = {"models": [todo.orm]}

    await Tortoise.init(db_url=db_url, modules=modules)

    if generate_schemas:
        await Tortoise.generate_schemas()  # Creates tables (if not created yet)


async def close() -> None:
    await Tortoise.close_connections()
