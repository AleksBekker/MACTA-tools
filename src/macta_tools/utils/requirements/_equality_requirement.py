from typing import Any, cast

from macta_tools.utils.requirements._requirement import Requirement


class EqualityRequirement(Requirement):
    """Class to represent a requirement that a value be exactly equal to a specific value."""

    def _checker(self, other_value: Any) -> bool:
        return cast(bool, self.value == other_value)
