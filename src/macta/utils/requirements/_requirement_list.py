from typing import Dict, Optional

from ._requirement import Requirement
from ._is_instance_requirement import IsInstanceRequirement


# TODO: make this inherit from `dict` and use its methods to store data
class RequirementList:
    def __init__(self, requirements: Optional[Dict[str, Requirement]] = None, **kwargs) -> None:
        """Initializes a `RequirementList` object.

        Arguments:
            requirements (Dict[str, Requirement]): a dictionary detailing multiple
            requirements that this object should check for
        """
        if requirements is None:
            requirements = {}
        self.requirements = {**requirements, **kwargs}

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
            assert IsInstanceRequirement(Requirement).are_compatible_with(*new_requirements.values())
        except AssertionError as e:
            raise ValueError('`new_requirements` must be a dict mapping `str` -> `Requirement`') from e

        self.__requirements = new_requirements

    # endregion

    def is_compatible_with(self, **kwargs) -> bool:
        """Check if a set of other values is compatible with this `RequirementList`

        Arguments:
            **kwargs: requirements to be tested

        Returns:
            `True` if all of the `other_values` are compatible with this `RequirementList`'s requirements
        """

        # TODO: find out if some kind of `zip` or related function is possible with dictionaries
        return all(self.requirements[k].is_compatible_with(v) for k, v in kwargs.items())
