from abc import ABC, abstractmethod
from typing import Any


class Requirement(ABC):
    """Class to represent a requirement.

    This class is meant to store a requirement and validate if other values fit this requirement.

    Attributes:
        __value (Any): the value that is being used to validate other values.
        __necessary (bool): represents if this requirement must be used in a RequirementList. If this is True, then
            trying to run a RequirementList validation without checking this Requirement will return False.

    Note:
        #21 the self.__necessary parameter should be stored in RequirementList, not here
    """

    def __init__(self, value: Any, necessary: bool = False):
        self.__value = value
        self.__necessary = necessary

    # region Properties

    @property
    def value(self):
        return self.__value

    @property
    def necessary(self):
        return self.__necessary

    # endregion

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

        return all(self.is_compatible_with(arg) for arg in args)
