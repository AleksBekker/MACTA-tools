
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .. import is_collection


@dataclass
class Requirement(ABC):
    """Class to represent a requirement"""

    value: any
    necessary: bool = False

    @abstractmethod
    def is_compatible_with(self, other_value) -> bool:
        """Determines if the `other_value` is compatible with this requirement.

        Arguments:
            other_value: the value to which this requirement is compared to

        Returns:
            `True` if `other_value` is compatible, `False` otherwise
        """

    def are_compatible_with(self, *args) -> bool:
        """Determines if multiple values are compatible with this requirement.

        Arguments:
            *args: the values to which this requirement is compared to

        Returns:
            `True` if all values in `args` are compatible with this requirement or if `args` is empty, `False` otherwise
        """

        if len(args) == 1 and is_collection(args[0]):
            args = args[0]

        return all(self.is_compatible_with(arg) for arg in args)
