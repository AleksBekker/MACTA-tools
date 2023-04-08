import pytest
from functools import lru_cache
from itertools import permutations
from typing import Any, Collection, Iterable, List, Tuple

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
    result = ContainsRequirement(collection).is_compatible_with(obj)
    return result and isinstance(result, bool)


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
    result = not ContainsRequirement(collection).is_compatible_with(obj)
    return result and isinstance(result, bool)


@lru_cache
def perms(iterable: Iterable[Any]) -> List[Tuple[Any]]:
    return list(permutations(iterable))


@pytest.mark.parametrize('collection, objs', [
    *(('abc', perm) for perm in perms('abc')),
    *((('a', 'b', 'c'), perm) for perm in perms('abc')),
    *((['a', 'b', 'c'], perm) for perm in perms('abc')),
    *(({'a', 'b', 'c'}, perm) for perm in perms('abc')),
    *(({'a': 0, 'b': 1, 'c': 2}, perm) for perm in perms('abc')),
    *(((0, 1, 2), perm) for perm in perms((0, 1, 2))),
    *(([0, 1, 2], perm) for perm in perms((0, 1, 2))),
    *(({0, 1, 2}, perm) for perm in perms((0, 1, 2))),
    *(({0: 'a', 1: 'b', 2: 'c'}, perm) for perm in perms((0, 1, 2))),
])
def test_contains_requirement_are_compatible_with_passes(collection: Collection[Any], objs: Tuple[Any]):
    result = ContainsRequirement(collection).are_compatible_with(*objs)
    return result and isinstance(result, bool)


@pytest.mark.parametrize('collection, objs', [
    ('abc', ['d']),
    ((0, 1, 2, 3), [4]),
    ([0, 1, 2, 3], [4]),
    ({0, 1, 2, 3}, [4]),
    ({0: 'a', 1: 'b', 2: 'c', 3: 'd'}, [4]),
    ({0: 'a', 1: 'b', 2: 'c', 3: 'd'}, ['a']),
], ids=['str_single', 'tuple_single', 'list_single', 'set_single', 'dict_key_single', 'dict_value_single'])
def test_contains_requirement_are_compatible_with_fails(collection: Collection[Any], objs: Tuple[Any]):
    result = not ContainsRequirement(collection).are_compatible_with(*objs)
    assert result and isinstance(result, bool)
