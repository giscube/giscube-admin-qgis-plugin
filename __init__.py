# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GiscubeAdmin
                                 A QGIS plugin
 A graphical Giscube administration tool
                             -------------------
        begin                : 2018-02-15
        copyright            : (C) 2018 by Martí Angelats i Ribera
        email                : marti.angelats@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
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
