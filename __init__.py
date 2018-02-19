# -*- coding: utf-8 -*-
"""
This script initializes the plugin, making it known to QGIS.
"""

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GiscubeAdmin class from file GiscubeAdmin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .giscube_admin import GiscubeAdmin
    return GiscubeAdmin(iface)
