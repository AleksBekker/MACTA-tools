
from macta.utils import is_collection


class TestIsCollection:

    # region Test that is_collection([collection]) -> True

    def test_dict_is_collection(self):
        assert is_collection({})

    def test_frozenset_is_collection(self):
        assert is_collection(frozenset())

    def test_list_is_collection(self):
        assert is_collection([])

    def test_range_is_collection(self):
        assert is_collection(range(10))

    def test_set_is_collection(self):
        assert is_collection(set())

    def test_tuple_is_collection(self):
        assert is_collection(())

    # endregion

    # region Test that is_collection([non-collection]) -> False

    def test_bool_is_not_collection(self):
        assert not is_collection(True)
        assert not is_collection(False)

    def test_bytearray_is_not_collection(self):
        assert not is_collection(bytearray.fromhex('2Ef0 F1f2  '))

    def test_bytes_is_not_collection(self):
        assert not is_collection(b'Hello, world')

    def test_complex_is_not_collection(self):
        assert not is_collection(complex(1, 2))

    def test_float_is_not_collection(self):
        assert not is_collection(3.14)

    def test_int_is_not_collection(self):
        assert not is_collection(42)

    def test_memoryview_is_not_collection(self):
        assert not is_collection(memoryview(b'abcefg'))

    def test_str_is_not_collection(self):
        assert not is_collection("Hello, world!")

    # endregion
