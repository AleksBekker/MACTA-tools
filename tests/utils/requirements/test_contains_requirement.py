import pytest
from typing import Any, Collection

from macta.utils.requirements import ContainsRequirement


@pytest.mark.parametrize('collection, obj', [
    ('abc', 'a'),
    ((0, 1, 2, 3), 0),
    ([0, 1, 2, 3], 2),
    ({0, 1, 2, 3}, 1),
    ({0: 'a', 1: 'b', 2: 'c', 3: 'd'}, 3),
],
    ids=['str', 'tuple', 'list', 'set', 'dict']
)
def test_contains_requirement_is_compatible_with_passes(collection: Collection[Any], obj: Any):
    assert ContainsRequirement(collection).is_compatible_with(obj)


@pytest.mark.parametrize('collection, obj', [
    ('abc', 'd'),
    ((0, 1, 2, 3), 4),
    ([0, 1, 2, 3], 4),
    ({0, 1, 2, 3}, 4),
    ({0: 'a', 1: 'b', 2: 'c', 3: 'd'}, 4),
    ({0: 'a', 1: 'b', 2: 'c', 3: 'd'}, 'a'),
],
    ids=['str', 'tuple', 'list', 'set', 'dict_key', 'dict_value']
)
def test_contains_requirement_is_compatible_with_fails(collection: Collection[Any], obj: Any):
    assert not ContainsRequirement(collection).is_compatible_with(obj)
