# -*- coding: utf-8 -*-


def str2int(s):
    """
    Converts str to int. If it is not str, return the same object.
    """
    if isinstance(s, str):
        return int(s)
    else:
        return s
