from typing import Any

from pydantic import field_validator

from macta_tools.utils.requirements._requirement import Requirement


class IsInstanceRequirement(Requirement):
    """Requirement that checks that an object is an instance of a specific type"""

    @field_validator('value')
    def value_is_type(cls, value: Any) -> type:
        """Validates that `self.value` is a `type`

        Raises:
            `ValueError` if `self.value` is not a `type`
        """
        if not isinstance(value, type):
            raise ValueError('IsInstanceRequirement requires self.value to be a `type`')
        return value

    def _checker(self, other_value: Any) -> bool:
        return isinstance(other_value, self.value)
