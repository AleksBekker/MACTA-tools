from macta.utils import is_collection
import pytest


@pytest.mark.parametrize("obj", [{}, frozenset(), [], range(10), set(), ()])
def test_builtin_collections_return_true(obj):
    assert is_collection(obj)


@pytest.mark.parametrize(
    "obj",
    [
        True,
        False,
        bytearray.fromhex("2Ef0 F1f2  "),
        b"Hello, world",
        complex(1, 2),
        3.14,
        42,
        memoryview(b"asdf"),
        "Hello, world!",
    ],
)
def test_builtin_noncollections_return_false(obj):
    assert not is_collection(obj)
