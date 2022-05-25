
from ._requirement import Requirement


class ContainsRequirement(Requirement):
    """Class to represent a requirement for a value/values to be elements of a container"""

    def is_compatible_with(self, other_value) -> bool:
        return other_value in self.value
