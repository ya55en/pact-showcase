import pytest
from tortoise import fields

from todo.base import BaseModel


class TestABaseModelSubclass:
    """Test a sub-class of `BaseModel`."""

    class AModel(BaseModel):
        id = fields.IntField(primary_key=True)

        name = fields.TextField(max_length=30)
        age = fields.IntField(min_value=18, max_value=120)
        comment = fields.TextField(null=True)

    def it_does_not_accept_invalid_attributes_on_creation(self):
        with pytest.raises(TypeError):
            self.AModel(name='Name', age=17, invalid='Invalid')

    def it_is_almost_equal_to_same_type_having_same_data_and_different_id(self):
        first_model = self.AModel(id=1, name='Name', age=33)
        second_model = self.AModel(id=2, name='Name', age=33)

        assert first_model.main_record_equal_to(second_model)

    def it_differs_form_same_type_having_different_data(self):
        first_model = self.AModel(id=1, name='Name', age=20)
        second_model = self.AModel(id=1, name='Name', age=42)

        assert not first_model.main_record_equal_to(second_model)

    def it_raises_error_on_attempt_to_set_invalid_attribute(self):
        model = self.AModel(name='Name', age=33)

        with pytest.raises(AttributeError):
            model.invalid_attribute = 'some value'

    def it_allows_setting_underscored_attributes(self):
        model = self.AModel(name='Name', age=33)

        model._protected_attribute = 'some value'

        assert model._protected_attribute == 'some value'

    def it_fails_on_instantiation_when_mandatory_attributes_are_missing(self):
        with pytest.raises(TypeError, match='.*missing mandatory attributes: age,name'):
            self.AModel()

        with pytest.raises(TypeError, match='.*missing mandatory attributes: age'):
            self.AModel(name='Name')

    async def it_fails_on_creation_when_mandatory_attributes_are_missing(self):
        with pytest.raises(TypeError, match='.*missing mandatory attributes: age'):
            await self.AModel.create(name='Name')
