#!/usr/bin/env python
"""
Package containing utility functions for the backend.
"""

import re


def urljoin(base, *parts):
    """
    Joins the base and the parts separating them with a slash. Removes
    duplicated slashes except if is part of the protocol (ie. https://).
    :param base: Base url.
    :type base: str
    """
    result = base
    for part in parts:
        result += '/'+part
    result = re.sub(
        r'(?<!/)(?<!:)/{2,}',
        '/',
        result)
    return result
