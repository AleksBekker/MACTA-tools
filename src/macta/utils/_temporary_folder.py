"""Implementation of a context manager for a temporary folder."""

from ._directory_close_mode import DirectoryCloseMode
import os
import shutil


class TemporaryFolder:
    """Context manager for a temporary folder."""

    def __init__(
        self,
        path: str,
        close_mode: DirectoryCloseMode = DirectoryCloseMode.DELETE_DIRECTORY,
    ):
        """Initialize temp folder context manager.

        Arguments:
            path (str): path to location of temporary folder
            to_delete (DirectoryClosemode): determines the action performed to the 
            directory once the context manager is closed
        """
        self._path: str = path
        self._close_mode: DirectoryCloseMode = close_mode

    def __enter__(self) -> None:
        """Enters context manager."""
        try:
            os.mkdir(self._path)
        except FileExistsError:
            pass

    def __exit__(self, exc_type, exc_val, traceback) -> None:
        """Exits context manager."""
        if self._close_mode in {
            DirectoryCloseMode.DELETE_CONTENTS,
            DirectoryCloseMode.DELETE_DIRECTORY,
        }:
            shutil.rmtree(self._path)

        if self._close_mode == DirectoryCloseMode.DELETE_CONTENTS:
            os.mkdir(self._path)
