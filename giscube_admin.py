# -*- coding: utf-8 -*-
"""
This script contains GiscubeAdmin: the plugin's main class.
"""

import os.path

from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from .backend import Giscube

from .settings import Settings
from .connections_saver import ConnectionsSaver

# Import the GUI classes
from .server_item import ServerItem
from .giscube_admin_dockwidget import GiscubeAdminDockWidget
from .giscube_admin_login_dialog import GiscubeAdminLoginDialog

# Initialize Qt resources from file resources.py
from .resources import *  # NOQA


class GiscubeAdmin:
    """QGIS Plugin Implementation."""

    # Plugin's client ID
    CLIENT_ID = 'omBayn3JMTuFBuErZWPA4o2NgeJlqlCa6cP4dxxY'

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """

        self.servers = None
        self.servers_saver = ConnectionsSaver()

        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize and load settings
        self.settings = Settings()

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GiscubeAdmin_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Giscube Admin')
        self.toolbar = self.iface.pluginToolBar()
        self.toolbar.setObjectName(u'GiscubeAdmin')

        self.pluginIsActive = False
        self.dockwidget = None

    def server_names(self):
        """
        Names of the currently connected servers.
        """
        r = []
        for i in range(self.servers.topLevelItemCount()):
            r.append(self.servers.topLevelItem(i).name)
        return r

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GiscubeAdmin', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/GiscubeAdmin/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Open Giscube Admin'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.add_action(
            icon_path,
            text=self.tr(u'Configure Giscube Admin'),
            callback=self.settings.edit_popup,
            parent=self.iface.mainWindow(),
            add_to_toolbar=False)

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Giscube Admin'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget is None:
                self.make_dockwidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()

    def make_dockwidget(self):
        """
        Makes and configures the plugin to make the dockwidget.
        """
        # Create the dockwidget (after translation) and keep reference
        self.dockwidget = GiscubeAdminDockWidget(self)

        self.servers = self.dockwidget.servers

        for conn in self.servers_saver.connections:
            name, url = conn
            giscube = Giscube(
                url,
                self.CLIENT_ID,
                name=name,
                save_tokens=self.settings.save_connections)

            if giscube.has_access_token:
                server = ServerItem(name, giscube, self.servers)
                self.servers.addTopLevelItem(server)
                server.setupUI()

    def new_server_popup(self):
        """
        Opens a new server dialog.
        """
        dialog = GiscubeAdminLoginDialog(self, parent=self.dockwidget)
        if dialog.exec_() and self.settings.save_connections:
            self.__save_connections()

    def __save_connections(self):
        """
        Saves the connections to the different servers.
        """
        conns = []
        for i in range(self.servers.topLevelItemCount()):
            conn = self.servers.topLevelItem(i).giscube_conn
            conns.append((conn.name, conn.server_url))
        self.servers_saver.connections = conns
