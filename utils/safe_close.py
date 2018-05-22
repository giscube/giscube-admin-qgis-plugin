# -*- coding: utf-8 -*-
from qgis.core import QgsProject


def safe_close(iface, callback):
    """
    Make sure the project is saved before is closed. If it closes successfully,
    call the callback.
    """
    iface.newProject(True)
    project = QgsProject.instance()
    if not project.isDirty():
        callback()
