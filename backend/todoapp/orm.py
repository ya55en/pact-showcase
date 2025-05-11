"""TortoizeORM-based ORM model for the todo backend."""

from __future__ import annotations

from tortoise import fields
from tortoise.models import Model
from tortoise.transactions import in_transaction


class TodoGroup(Model):
    id = fields.IntField(primary_key=True)

    name = fields.TextField()
    comment = fields.TextField(null=True)


class TodoItem(Model):
    id = fields.IntField(primary_key=True)

    group = fields.ForeignKeyField('models.TodoGroup', related_name='items', null=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)


async def seed_db() -> None:
    """Seed the database with initial data."""
    if await TodoGroup.exists(name='Daily'):
        return  # already seeded

    async with in_transaction():
        group = await TodoGroup.create(name='Daily', comment='Daily todos')

        await TodoItem.create(
            title='Buy bread',
            description='Check how much is left and provide some',
            group=group,
        )
        await TodoItem.create(title='Check messages', group=group)
        await TodoItem.create(title='Go to Bed', description='Self-explanantory', group=group)
