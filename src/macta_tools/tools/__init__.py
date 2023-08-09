import sys
import warnings
from contextlib import suppress
from typing import Dict

from numba.core.errors import NumbaDeprecationWarning

from macta_tools.tools._cta_tool_interface import CTAToolInterface

AVAILABLE: Dict[str, CTAToolInterface] = {}
__all__ = ['AVAILABLE', 'CTAToolInterface']

# TODO delete this when possible
if not sys.warnoptions:
    warnings.simplefilter('ignore', NumbaDeprecationWarning)

with suppress(ImportError):
    from macta_tools.tools._celltypist_interface import CelltypistInterface
    __all__.append('CelltypistInterface')
    AVAILABLE['celltypist'] = CelltypistInterface()

with suppress(ImportError):
    from macta_tools.tools._scanvi import ScanviInterface
    __all__.append('ScanviInterface')
    AVAILABLE['scanvi'] = ScanviInterface()
