import typing
from contextlib import contextmanager


@typing.no_type_check
@contextmanager
def suppress_logging() -> None:
    import logging
    state = logging.getLogger().getEffectiveLevel()
    logging.disable(logging.CRITICAL)
    try:
        yield
    finally:
        logging.disable(state)
