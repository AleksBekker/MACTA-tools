from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Sequence, Union


@dataclass(frozen=True)
class Requirement(ABC):
    value: Any

    @abstractmethod
    def _checker(self, checked: Any) -> bool:
        """Abstract method that checks if a certain value upholds this requirement

        Arguments:
            checked (Any): the value that is checked against this requirement

        Returns:
            True if this requirement is upheld, False otherwise
        """

    def check(self, *args: Union[Sequence[Any], Any]) -> bool:
        """Checks if values uphold this requirement

        Arguments:
            *args (Sequence[Any]): any amount of values to test against this requirement

        Returns:
            True if every value in args passes, False otherwise
        """
        return all(self._checker(arg) for arg in args)
