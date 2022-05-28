def is_collection(obj) -> bool:
    """Checks if an object is a collection.

    Arguments:
        obj: the object in question

    Returns:
        `True` if `obj` is a collection, `False` otherwise
    """
    return '__contains__' in dir(obj) and not isinstance(obj, (bytearray, bytes, str))
