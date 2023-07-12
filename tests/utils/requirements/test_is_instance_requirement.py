import pytest
from typing import Any, Type

from macta.utils.requirements import IsInstanceRequirement


@pytest.mark.parametrize('cls, obj', [
    (bool, True),
    (bool, False),
    (int, 10),
    (int, -8),
    (int, 0),
    (float, -10.5),
    (float, 10.0),
    (float, 0.0),
    (complex, complex(10)),
    (complex, complex(10, 3)),
    (list, [0, 1, 2]),
    (list, []),
    (tuple, ()),
    (tuple, (0, 1)),
    (range, range(10)),
    (str, 'asdfasdf'),
    (str, ''),
    (bytes, b'12312a'),
    (bytes, b''),
    (set, set()),
    (set, {0, 1}),
    (frozenset, frozenset()),
    (frozenset, frozenset((0, 1, 2))),
    (dict, {}),
    (dict, {0: 'a', 1: 'b'}),
])
def test_is_instance_is_compatible_with_builtins_passes(cls: Type, obj: Any):
    result = IsInstanceRequirement(cls).is_compatible_with(obj)
    assert result and isinstance(result, bool)
