import logging
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def suppress_logging() -> Iterator[None]:
    state = logging.getLogger().getEffectiveLevel()
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(state)
