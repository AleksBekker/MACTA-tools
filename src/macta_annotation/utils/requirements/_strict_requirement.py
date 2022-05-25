
from ._requirement import Requirement


class StrictRequirement(Requirement):
    """Class to represent a requirement that a value be exactly equal to a specific value."""

    def is_compatible_with(self, other_value) -> bool:
        return self.value == other_value
