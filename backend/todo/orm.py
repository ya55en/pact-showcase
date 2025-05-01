"""TortoizeORM-based ORM model for the todo backend."""

from __future__ import annotations

from tortoise import fields

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
