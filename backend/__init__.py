#!/usr/bin/env python
"""
Backend package of giscube-admin-qgis-plugin. Contains a Giscube API client,
custom exceptions and internal utilities (for this package).
"""
from .giscube import Giscube
from .exceptions import Unauthorized

__all__ = ["Giscube", "Unauthorized"]
