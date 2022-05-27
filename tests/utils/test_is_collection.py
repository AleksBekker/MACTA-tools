from macta.utils import is_collection
import pytest


@pytest.mark.parametrize(
    "obj",
    [{}, frozenset(), [], range(10), set(), ()],
    ids=["dict", "forzenset", "list", "range", "set", "tuple"],
)
def test_builtin_collections_return_true(obj):
    assert is_collection(obj)


@pytest.mark.parametrize(
    "obj",
    [
        False,
        True,
        bytearray.fromhex("2Ef0 F1f2  "),
        b"Hello, world",
        complex(1, 2),
        3.14,
        42,
        memoryview(b"asdf"),
        "Hello, world!",
    ],
    ids=[
        "bool-False",
        "bool-True",
        "bytearray",
        "bytes",
        "complex",
        "float",
        "int",
        "memoryview",
        "str",
    ],
)
def test_builtin_noncollections_return_false(obj):
    assert not is_collection(obj)
