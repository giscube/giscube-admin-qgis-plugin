# -*- coding: utf-8 -*-
"""
This script installs, if needed, all the dependencies and then initializes the
plugin, making it known to QGIS.
"""
# Importing all the plugin
from os import path
from importlib import import_module

# List of dependencies
DEPENDENCIES = []

# Import pip. If it is not installed, install it
try:
    import pip
except:
    exec(open(path.join(path.dirname(__file__), 'get-pip.py').read()))
    import pip
    # just in case the included version is old
    pip.main(['install', '--upgrade', 'pip'])


def install_dependency(name):
    """Test that a dependency can be loaded. If not, it installs it.

    :param name: Name of the dependent module to check and install
    :type name: str or unicode
    """
    try:
        import_module(name)
    except:
        pip.main(['install', name])


# Install all dependencies
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
