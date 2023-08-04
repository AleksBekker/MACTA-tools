# from contextlib import suppress
# from typing import Dict

from macta.tools._cta_tool_interface import CTAToolInterface

# AVAILABLE: Dict[str, CTAToolInterface] = {}
__all__ = ['AVAILABLE', 'CTAToolInterface']


# with suppress(ImportError):
#     from macta.tools._celltypist_interface import CelltypistInterface
#     __all__.append('CelltypistInterface')
#     AVAILABLE['celltypist'] = CelltypistInterface()

# with suppress(ImportError):
#     from macta.tools._scanvi import ScanviInterface
#     __all__.append('ScanviInterface')
#     AVAILABLE['scanvi'] = ScanviInterface()
