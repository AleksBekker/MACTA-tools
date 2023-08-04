from typing import Any, Container

import pytest

from macta.utils.requirements import NotNoneRequirement


def test_not_none_requirement_catches_none() -> None:
    """Tests that `NoneRequirement.check` returns false when passed `None`."""
    assert not NotNoneRequirement().check(None)


@pytest.mark.parametrize('value', [0, 0., False, 0 + 0j, '', b'', r''],
                         ids=['int', 'float', 'bool', 'complex', 'str', 'byte', 'rawstr'])
def test_not_none_requirement_validates_zerolike(value: Any) -> None:
    """Tests that `NotNoneRequirements.check` returns true when passed zero-like data."""
    assert NotNoneRequirement().check(value)


@pytest.mark.parametrize('container', [[], (), {}, set()], ids=['list', 'tuple', 'dict', 'set'])
def test_not_none_requirement_validates_empty(container: Container[Any]) -> None:
    """Tests that `NotNoneRequirement.check` returns true when passed an empty container."""
    assert NotNoneRequirement().check(container)
