#!/usr/bin/env python
"""
Exceptions from the backend package.
"""


class BadCredentials(ConnectionError):
    """
    The credentials or the token used are wrong or have expired and cannot be
    refreshed.
    """
    pass
