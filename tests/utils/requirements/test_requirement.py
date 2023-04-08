import pytest

from macta.utils.requirements import Requirement


def test_requirement_is_abstract_class():
    with pytest.raises(TypeError):
        Requirement('test')
