#!/usr/bin/env python
"""
Package containing utility functions for the backend.
"""

import re
from urllib.parse import urlparse


def urljoin(base, *parts):
    """
    Joins the base and the parts separating them with a slash. Removes
    duplicated slashes except if is part of the protocol (ie. https://).
    :param base: Base url.
    :type base: str
    """
    result = str(base)+'/'
    for part in parts:
        result += str(part)+'/'
    result = re.sub(
        r'(?<!/)(?<!:)/{2,}',
        '/',
        result)
    return result


def is_url_valid(url, allowed_schemes):
    parsed = urlparse(url)
    is_valid = (parsed.scheme in allowed_schemes)
    return is_valid
