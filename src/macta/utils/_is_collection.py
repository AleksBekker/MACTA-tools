
from collections.abc import Sequence


def is_collection(obj) -> bool:
    '''Checks if an object is a collection. Credit to 
    https://www.reddit.com/r/learnpython/comments/485h1p/comment/d0hdjef/?utm_source=share&utm_medium=web2x&context=3

    Arguments:
        obj: the object in question

    Returns:
        `True` if `obj` is a collection, `False` otherwise
    '''
    return isinstance(obj, Sequence) and not isinstance(obj, (str, bytes, bytearray))
