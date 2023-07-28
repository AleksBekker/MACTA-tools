import pydantic
from pydantic import validator
from typing import Any, Dict, Optional

from macta.utils.requirements._requirement import Requirement
from macta.utils.requirements._is_instance_requirement import IsInstanceRequirement


# TODO: make this inherit from `dict` and use its methods to store data
class RequirementList(pydantic.BaseModel):
    requirements: Dict[str, Requirement]

    def __init__(self, requirements: Optional[Dict[str, Requirement]] = None, **kwargs: Any):
        if not requirements:
            requirements = {}
        super().__init__(requirements={**requirements, **kwargs})

    @validator('requirements')
    def requirements_correct_dict(cls, requirements: Optional[Dict[str, Requirement]], **kwargs: Any) -> Dict[str, Requirement]:

        # Input Validation
        if not isinstance(requirements, dict) or not IsInstanceRequirement(str).check(*requirements.keys()) \
                or not IsInstanceRequirement(Requirement).check(*requirements.values()):
            raise ValueError('`new_requirements` must be a dict mapping `str` -> `Requirement`')

        return requirements

    def check(self, **kwargs: Dict[str, Any]) -> bool:
        """Check if a set of other values is compatible with this `RequirementList`

        Arguments:
            **kwargs: values to be tested against requirements

        Returns:
            `True` if all of the `other_values` are compatible with this `RequirementList`'s requirements
        """

        return all(self.requirements[k].check(v) for k, v in kwargs.items())
