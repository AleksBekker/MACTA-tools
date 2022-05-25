"""Implementation of an enum for how to deal with a directory once it's no longer in use."""

import enum


class DirectoryCloseMode(enum.Enum):
    KEEP_ALL = enum.auto()
    DELETE_CONTENTS = enum.auto()
    DELETE_DIRECTORY = enum.auto()
