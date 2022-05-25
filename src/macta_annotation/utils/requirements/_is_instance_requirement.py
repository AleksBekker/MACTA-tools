
from ._requirement import Requirement


class IsInstanceRequirement(Requirement):

    def is_compatible_with(self, other_value) -> bool:
        return isinstance(other_value, self.value)
