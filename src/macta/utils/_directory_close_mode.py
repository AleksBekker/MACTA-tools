"""Implementation of an enum for directory close behavior."""

import enum


class DirectoryCloseMode(enum.Enum):
    KEEP_ALL = enum.auto()
    DELETE_CONTENTS = enum.auto()
    DELETE_DIRECTORY = enum.auto()
