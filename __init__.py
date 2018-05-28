# -*- coding: utf-8 -*-
"""
This script initializes the plugin, making it known to QGIS.
"""

# from geoserverexplorer plugin for QGIS 2.x
import sys
import os
import site

base_path = os.path.abspath(os.path.dirname(__file__))

site.addsitedir(
    os.path.join(base_path, 'ext-libs')
)
if sys.platform == 'win32':
    site.addsitedir(
        os.path.join(base_path, 'ext-libs-win32')
    )


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GiscubeAdmin class from file GiscubeAdmin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .giscube_admin import GiscubeAdmin
    return GiscubeAdmin(iface)
