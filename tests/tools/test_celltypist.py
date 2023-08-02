import pytest

# Skip this file if this module cannot be used with the current MACTA installation
try:
    from macta.tools import CelltypistInterface
except ImportError:
    pytest.skip(allow_module_level=True, msg='Celltypist-compatible extra not installed.')


class TestCelltypistRqlist():
    """Test that the `CelltypistInterface`'s `RequirementsList` works as intended"""

    def test_celltypist_annot_type(self) -> None:
        """Test that the interface works when annot_type is exclusively `'ref'`."""
        interface = CelltypistInterface()
        assert interface.check_requirements(annot_type='ref')
        assert not interface.check_requirements(annot_type='marker')
