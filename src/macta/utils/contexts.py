import logging
import typing
from contextlib import contextmanager


@typing.no_type_check
@contextmanager
def suppress_logging() -> None:
    state = logging.getLogger().getEffectiveLevel()
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(state)
