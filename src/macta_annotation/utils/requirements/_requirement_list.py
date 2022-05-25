
import logging
from typing import Dict

from ._requirement import Requirement
from ._contains_requirement import ContainsRequirement
from ._is_instance_requirement import IsInstanceRequirement


class RequirementList:

    def __init__(self, requirements: Dict[str, Requirement]) -> None:
        """Initializes a `RequirementList` object.

        Arguments:
            rqs (Dict[str, Requirement]): a dictionary detailing multiple requirements that this object should check for
        """
        self.requirements = requirements

    # region Class Properties

    @property
    def requirements(self) -> Dict[str, Requirement]:
        return self.__requirements

    @requirements.setter
    def requirements(self, new_requirements: Dict[str, Requirement]) -> None:

        # Input Validation
        try:
            assert isinstance(new_requirements, dict)
            assert IsInstanceRequirement(str).are_compatible_with(*new_requirements.keys())
            assert IsInstanceRequirement(str).are_compatible_with(*new_requirements.values())
        except AssertionError as e:
            raise ValueError("self.requirements must be a Dictionary mapping `str` -> `Requirement`", e)

        self.__requirements = new_requirements

    # endregion

    def is_compatible_with(self, other_values: Dict[str, any]) -> bool:
        """Check if a set of other values is compatible with this RequirementList

        Arguments:
            other_values (Dict[str, any]): A dictionary of `requirement_name` -> `other_value`

        Returns:
            `True` if all of the `other_values` are compatible with this `RequirementList`'s requirements
        """

        # TODO: find out if some kind of `zip` or related function is possible with dictionaries
        return all(self.requirements[k].is_compatible(v) for k, v in other_values.items())
