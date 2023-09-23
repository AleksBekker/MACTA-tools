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

# TODO figure out how to turn each `with` into a function

with suppress(ModuleNotFoundError):
    from macta_tools.tools._celltypist_interface import CelltypistInterface
    __all__.append('CelltypistInterface')
    celltypist = CelltypistInterface()
    AVAILABLE[celltypist._name] = celltypist

with suppress(ModuleNotFoundError):
    from macta_tools.tools._scanvi import ScanviInterface
    __all__.append('ScanviInterface')
    scanvi = ScanviInterface()
    AVAILABLE[scanvi._name] = scanvi
