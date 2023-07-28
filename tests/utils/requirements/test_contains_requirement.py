import pytest
from itertools import permutations
from typing import Any, Collection, List, Tuple

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
def test_contains_requirement_is_compatible_with_passes(collection: Collection[Any], obj: Any) -> None:
    result = ContainsRequirement(collection).check(obj)
    assert result and isinstance(result, bool)


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
def test_contains_requirement_is_compatible_with_fails(collection: Collection[Any], obj: Any) -> None:
    result = not ContainsRequirement(collection).check(obj)
    assert result and isinstance(result, bool)


permutations_abc = list(permutations('abc'))
permutations_012 = list(permutations((0, 1, 2)))


@pytest.mark.parametrize('collection, perm', [
    *(('abc', perm) for perm in permutations_abc),
    *((('a', 'b', 'c'), perm) for perm in permutations_abc),
    *((['a', 'b', 'c'], perm) for perm in permutations_abc),
    *(({'a', 'b', 'c'}, perm) for perm in permutations_abc),
    *(({'a': 0, 'b': 1, 'c': 2}, perm) for perm in permutations_abc),
    *(((0, 1, 2), perm) for perm in permutations_012),
    *(([0, 1, 2], perm) for perm in permutations_012),
    *(({0, 1, 2}, perm) for perm in permutations_012),
    *(({0: 'a', 1: 'b', 2: 'c'}, perm) for perm in permutations_012),
])
def test_contains_requirement_check_permutations_passes(collection: Collection[Any], perm: List[Any]) -> None:
    result = ContainsRequirement(collection).check(*perm)
    assert result and isinstance(result, bool)


# TODO separate different types of issues here #13
@pytest.mark.parametrize('collection, objs', [
    ('abc', ['d']),
    ((0, 1, 2, 3), [4]),
    ([0, 1, 2, 3], [4]),
    ({0, 1, 2, 3}, [4]),
    ({0: 'a', 1: 'b', 2: 'c', 3: 'd'}, [4]),
    ({0: 'a', 1: 'b', 2: 'c', 3: 'd'}, ['a']),
    ('abc', ['a', 'c', 'b', 'a', 'd']),
    ('abc', ['d', 'a']),
    ((0, 1, 2, 3), [3, 3, 3, 3, 3, 4]),
    ((0, 1, 2, 3), [4, 1, 2, 3]),
    ([0, 1, 2, 3], [1, 3, 4]),
    ([0, 1, 2, 3], [4, 1, 1, 1]),
    ({0, 1, 2, 3}, [1, 1, 4, 1]),
    ({0, 1, 2, 3}, [4, 1, 2]),
    ({0: 'a', 1: 'b', 2: 'c', 3: 'd'}, [*(2 for _ in range(1000)), 4, 3, 1]),
    ({0: 'a', 1: 'b', 2: 'c', 3: 'd'}, [0, 1, 2, 'a', 'b']),
])
def test_contains_requirement_are_compatible_with_fails(collection: Collection[Any], objs: Tuple[Any]) -> None:
    result = not ContainsRequirement(collection).check(*objs)
    assert result and isinstance(result, bool)
