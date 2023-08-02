from typing import Any, Optional

from macta.utils.requirements import Requirement


class NotNoneRequirement(Requirement):
    """Requirement that verifies an object is not `None`."""

    def __init__(self) -> None:
        super().__init__(value=None)

    def _checker(self, to_check: Optional[Any]) -> bool:
        return to_check is not None
