"""Provide common functionality for all models."""

from tortoise.models import Model
from tortoise.queryset import QuerySet


class _StrictModelMeta(type(Model)):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)

        if name != 'BaseModel':
          cls.fieldnames = set(cls._meta.fields_map.keys())
          cls.fieldnames.add('pk')  # Tortoise uses this internally

        return cls


class BaseModel(Model, metaclass=_StrictModelMeta):
    class Meta:
        abstract = True

    def __init__(self, **kwargs):
        invalid_attributes = set(kwargs.keys()) - self.fieldnames - {'pk'}

        if invalid_attributes:
            raise TypeError(
                f'{type(self).__name__}: invalid attributes: {",".join(invalid_attributes)}'
            )

        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        def eligible_for_setting(name):
            return name in self.fieldnames or name.startswith('_') or name.endswith('_id')

        if not eligible_for_setting(name):
            raise AttributeError(f"Cannot set '{name}' on {type(self).__name__}")

        super().__setattr__(name, value)

    def __str__(self):
        field_values = ','.join(
            f'{field}={getattr(self, field, None)!r}' for field in self.fieldnames
        )

        return f'{type(self).__name__}({field_values})'

    __repr__ = __str__

    def main_record_equal_to(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        for field in self.fieldnames - {'pk', 'id'}:
            lhs = getattr(self, field)
            rhs = getattr(other, field)

            if isinstance(lhs, QuerySet) or isinstance(rhs, QuerySet):
                continue  # do not compare associations

            if lhs != rhs:
                return False

        return True
