import pytest

import tortoise
from todo.orm import TodoGroup, TodoItem

pytestmark = pytest.mark.anyio  # avoid using @pytest.mark.asyncio on each async test


class TestTodoGroup:
    async def it_stores_itself_as_record_in_the_database(self):
        created = await TodoGroup.create(name='Group', comment='Comment')

        assert created.id is not None
        assert created.name == 'Group'
        assert created.comment == 'Comment'

        fetched = await TodoGroup.get(id=created.id)

        assert fetched == created
        assert fetched.name == 'Group'
        assert fetched.comment == 'Comment'

    async def it_updates_its_database_record(self):
        group = await TodoGroup.create(name='Original name', comment='For update')

        group.name = 'Updated name'
        await group.save()

        updated = await TodoGroup.get(id=group.id)
        assert updated.name == 'Updated name'

    async def test_it_deletes_its_database_record(self):
        group = await TodoGroup.create(name='Group to delete', comment='Delete me')

        await group.delete()

        with pytest.raises(tortoise.exceptions.DoesNotExist):
            await TodoGroup.get(id=group.id)

    async def it_can_have_no_comment(self):
        created = await TodoGroup.create(name='Group without comment')
        fetched = await TodoGroup.get(id=created.id)

        assert fetched.comment is None

    async def it_can_have_no_item(self):
        created = await TodoGroup.create(name='Group without any items')

        fetched = await TodoGroup.get(id=created.id)

        assert await fetched.items == []

    async def it_can_have_multiple_items(self):
        group = await TodoGroup.create(name='Group with items', comment='Comment')
        first_item = await TodoItem.create(title='First Item', group=group)
        second_item = await TodoItem.create(title='Second Item', group=group)

        assert first_item.group_id == group.id
        assert second_item.group_id == group.id

        fetched_group = await TodoGroup.get(id=group.id)
        fetched_items = await fetched_group.items

        assert len(fetched_items) == 2
        assert fetched_items[0].main_record_equal_to(first_item)
        assert fetched_items[1].main_record_equal_to(second_item)
        

class TestTodoItem:
    async def it_stores_itself_as_record_in_the_database(self):
        created = await TodoItem.create(title='Item', description='Description')

        assert isinstance(created.id, int)
        assert created.title == 'Item'
        assert created.description == 'Description'

        fetched = await TodoItem.get(id=created.id)

        assert fetched.main_record_equal_to(created)

    async def it_updates_its_record_in_the_database(self):
        item = await TodoItem.create(title='Original title', description='For update')

        item.title = 'Updated title'
        await item.save()

        updated = await TodoItem.get(id=item.id)
        assert updated.title == 'Updated title'

    async def test_it_deletes_its_database_record(self):
        item = await TodoItem.create(title='Item to delete')

        await item.delete()

        with pytest.raises(tortoise.exceptions.DoesNotExist):
            await TodoItem.get(id=item.id)

    async def it_can_associate_with_a_group(self):
        group = await TodoGroup.create(name='Group', comment='Comment')
        item = await TodoItem.create(title='Item', description='Description', group=group)

        fetched = await TodoItem.get(id=item.id)

        assert item.group_id == group.id
        assert fetched.group_id == group.id
        assert (await fetched.group).main_record_equal_to(group)
