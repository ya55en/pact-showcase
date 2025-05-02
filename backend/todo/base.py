"""Provide common functionality for all models.

By default, Tortoise ORM allows setting any attribute on a model instance,
even if it is not defined in the model and does not provide means to convert
model instances to dicts. We try to correct such issues here.
"""

from typing import Any

from tortoise.models import MODEL, Model
from tortoise.queryset import QuerySet


class _StrictModelMeta(type(Model)):
    """Provide a class-level attribute `fieldnames` containing all valid
    field names."""

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)

        if name != 'BaseModel':
            cls.fieldnames = set(cls._meta.fields_map.keys())
            cls.fieldnames.add('pk')  # Tortoise uses this internally

            cls.mandatory = set(
                field
                for field in cls._meta.fields_map.keys()
                if (
                    cls._meta.fields_map[field].required
                    and cls._meta.fields_map[field].default is None
                )
            )

        return cls


class BaseModel(Model, metaclass=_StrictModelMeta):
    class Meta:
        abstract = True  # do not instantiate

    @classmethod
    async def create(cls: type[MODEL], **kwargs: Any) -> MODEL:
        """Override the create method to check for invalid attributes."""
        cls._check_invalid(kwargs)
        cls._check_missing_mandatory(kwargs)

        return await super().create(**kwargs)

    @classmethod
    def _check_invalid(cls, kwargs):
        """Pass silently if no invalid attributes are passed; otherwise raise TypeError."""

        invalid = set(kwargs.keys()) - cls.fieldnames - {'pk'}

        if invalid:
            raise TypeError(f'{cls.__name__}: invalid attributes: {",".join(sorted(invalid))}')

    @classmethod
    def _check_missing_mandatory(cls, kwargs):
        """Pass silently if no mandatory attributes are missing; otherwise raise TypeError."""

        missing_mandatory = cls.mandatory - set(kwargs.keys())

        print('\n\n@@@@@@ class:', cls.__name__)
        print('@@@@@@ mandatory:', cls.mandatory)
        print('@@@@@@ missing_mandatory:', missing_mandatory)

        if missing_mandatory:
            raise TypeError(
                f'{cls.__name__}({kwargs}): missing mandatory attributes: '
                f'{",".join(sorted(missing_mandatory))}'
            )

    def __init__(self, **kwargs):
        self._check_invalid(kwargs)
        self._check_missing_mandatory(kwargs)

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

    def as_dict(self):
        """Return a dictionary representation of the model instance,
        excluding associations.
        """
        return {
            field: getattr(self, field)
            for field in self.fieldnames - {'pk'}
            if not isinstance(getattr(self, field), QuerySet)
        }

    def main_record_equal_to(self, other):
        """Compare two model instances, ignoring the primary key
        and associations.
        """
        if not isinstance(other, type(self)):
            return NotImplemented

        for field in self.fieldnames - {'pk', 'id'}:
            lhs, rhs = getattr(self, field), getattr(other, field)

            if isinstance(lhs, QuerySet) or isinstance(rhs, QuerySet):
                continue  # do not compare associations

            if lhs != rhs:
                return False

        return True
