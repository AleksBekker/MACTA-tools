import pytest

# Skip this file if this module cannot be used with the current MACTA installation
try:
    from macta.tools import ScanviInterface
except ImportError:
    pytest.skip(allow_module_level=True, msg='SCANVI-compatible extra not installed.')


class TestScanviRqlist:
    """Tests the `SCANVI` interface's requirements list."""

    interface = ScanviInterface()

    def test_rqlist_succeeds(self) -> None:
        assert self.interface.check_requirements(
            annot_type='ref',
            batch_col='batch_col',
            cell_type_col='cell_type_col',
        )

    def test_marker_annot_type_fails(self) -> None:
        assert not self.interface.check_requirements(
            annot_type='marker',
            batch_col='batch_col',
            cell_type_col='cell_type_col',
        )

    def test_no_batch_col_fails(self) -> None:
        assert not self.interface.check_requirements(
            annot_type='marker',
            cell_type_col='cell_type_col',
        )

    def test_no_cell_type_col_fails(self) -> None:
        assert not self.interface.check_requirements(
            annot_type='marker',
            batch_col='batch_col',
        )
