from typing import Any, Iterable

from pydantic import field_validator

from macta.utils.requirements._requirement import Requirement


class ContainsRequirement(Requirement):
    """Class to represent a requirement for a value/values to be elements of a container"""

    @field_validator('value')
    def value_is_iterable(cls, value: Any) -> Iterable[Any]:
        """Validates that `self.value` is an `Iterable`

        Raises:
            `ValueError` if `self.value` is not an `Iterable`
        """
        if not isinstance(value, Iterable):
            raise ValueError('Contains Requirement requires self.value to be an `Iterable`')
        return value

    def _checker(self, other_value: Any) -> bool:
        return other_value in self.value
