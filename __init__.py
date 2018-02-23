# -*- coding: utf-8 -*-
"""
This script installs, if needed, all the dependencies and then initializes the
plugin, making it known to QGIS.
"""
# Importing all the plugin
from os import path
from importlib import import_module

DEPENDENCIES = []

try:
    import pip
except:
    exec(open(path.join(path.dirname(__file__), 'get-pip.py').read()))
    import pip
    # just in case the included version is old
    pip.main(['install', '--upgrade', 'pip'])


def install_dependency(name):
    try:
        import_module(name)
    except:
        pip.main(['install', '--upgrade', name])


for name in DEPENDENCIES:
    install_dependency(name)


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GiscubeAdmin class from file GiscubeAdmin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .giscube_admin import GiscubeAdmin
    return GiscubeAdmin(iface)
