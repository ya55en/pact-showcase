"""TortoizeORM-based ORM model for the todo backend."""

from __future__ import annotations

from tortoise import fields
from tortoise.transactions import in_transaction

from todo.base import BaseModel


class TodoGroup(BaseModel):
    id = fields.IntField(primary_key=True)

    name = fields.TextField()
    comment = fields.TextField(null=True)


class TodoItem(BaseModel):
    id = fields.IntField(primary_key=True)

    group = fields.ForeignKeyField('models.TodoGroup', related_name='items', null=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)


async def seed_db() -> None:
    """Seed the database with initial data."""
    print('\n\n##### seed_db() called #####\n\n')

    if await TodoGroup.exists(name='Daily'):
        return

    print('\n\n##### Seeding database #####\n\n')

    async with in_transaction():
        group = await TodoGroup.create(name='Daily', comment='Daily todos')

        await TodoItem.create(
            title='Buy bread',
            description='Check how much is left and provide some',
            group=group,
        )
        await TodoItem.create(title='Check Signal', group=group)
        await TodoItem.create(title='Go to bed', description='Self-explanantory', group=group)
