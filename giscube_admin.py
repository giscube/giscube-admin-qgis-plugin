# -*- coding: utf-8 -*-
"""
This script contains GiscubeAdmin: the plugin's main class.
"""

import os.path
import time

from PyQt5.QtCore import QSettings, QDir, Qt, \
                         QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from qgis.core import Qgis, QgsProject
from qgis.gui import QgsMessageBar

from .backend import Giscube

from .settings import Settings

# Import the GUI classes
from .ui.giscube_admin_dockwidget import GiscubeAdminDockWidget
from .ui.server_item import ServerItem
from .ui.project_item import ProjectItem
from .ui.new_server_dialog import NewServerDialog
from .ui.new_project_dialog import NewProjectDialog

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

        def load():
            if self.settings.is_open:
                self.open_action.trigger()

        iface.initializationCompleted.connect(load)

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
        self.open_action = self.add_action(
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

        self.settings.is_open = False
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

        if self.dockwidget is not None:
            self.dockwidget.hide()
            self.iface.removeDockWidget(self.dockwidget)
            del self.dockwidget
            self.dockwidget = None

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True
            self.settings.is_open = True

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

        for name in ServerItem.saved_servers.childGroups():
            conn = Giscube(
                ServerItem.saved_servers.value(name+'/url'),
                self.CLIENT_ID,
                False,
                name,
            )
            ServerItem(conn, self.servers, self)



    def new_server_popup(self):
        #ha d'apareixer la cerca, no l'arbre que ja tenim

        import requests
        import json
        from PyQt5.QtWidgets import QTreeWidgetItem
        from qgis.core import QgsProject, QgsRasterLayer, QgsVectorLayer, QgsCoordinateReferenceSystem, QgsCoordinateTransform
        from qgis.core import QgsField, QgsPoint, QgsPointXY, QgsFeature, QgsGeometry
        from qgis.PyQt.QtCore import QVariant
        import qgis.utils
        from qgis.utils import iface


        ##CERCA

        #url de la cerca
        #s = requests.get('https://mapes.salt.cat/apps/cercador/cercar/?q=industrials')

        url = 'https://mapes.salt.cat/apps/cercador/cercar/?q=industrials'
        #url = 'https://mapes.salt.cat/apps/giscube-admin/geoportal/search/?q=Ortofoto+Salt+2013'

        s = requests.get(url)
        search = s.json() #diccionari

        count = search.get('count')
        results = search.get('results') #llista amb diccionaris dins ¿?


        items = []
        list = [] #sera una llista de diccionaris


        #definim el tipus
        if count is not None:
            type = 'GeoJSON'
            nom = 'cerca: ' + url[47:]

        else:
            type = 'TMS'
            child = results[0].get('children')
            url = child[0].get('url')
            title = results[0].get('title')



        #carreguem el TMS layer
        def __loadLayerTMS(url, title):
            # create QGIS raster layer & add to map
            urlWithParams = 'type=xyz&url=' + str(url)
            urlWithParams += '&zmax=22&zmin=0'

            rlayer = QgsRasterLayer(urlWithParams, title, 'wms')
            print(rlayer.isValid())

            if rlayer.isValid():
                QgsProject.instance().addMapLayer(rlayer)



        def create_items(list, results):
            #crear l'item per afegir a l'arbre
            for item in results: # item és cada diccionari dins la llista
                g = item.get('geojson')
                #print(type(g))
                geo = g.get('geometry')
                #print(geo)

                coord = geo.get('coordinates')

                x = coord[0]
                #print('x:', x)
                y = coord[1]

                name = [item.get('title') + str(',  ') + item.get('address')]

                #cada item ha de ser un WidgetItem per posar a l'arbre
                item['widget'] = QTreeWidgetItem(None, name)
                item['widget'].setData(2, QtCore.Qt.EditRole, item) # 2 data

                items.append(item['widget']) #llista de diccionaris

                address = item.get('address')
                title = item.get('title')
                print(title)

                layer = {
                    'x': x,
                    'y': y,
                    'address': address,
                    'title': title
                }

                list.append(layer)



        def create_layer(list, nom):
            #creem el layer
            vl = QgsVectorLayer("Point", nom , "memory")
            QgsProject.instance().addMapLayer(vl)


            #afegir els atributs al layer
            for i in list:
            #passar cada adreça, cada titol i cada parell de coordenades
                address = i['address']
                title = i['title']
                x = i['x']
                y = i['y']

                print('dades:', address, title, x, y)

                #print(address, '', title)
                pr = vl.dataProvider()
                pr.addAttributes([QgsField("address", QVariant.String),
                                  QgsField("title", QVariant.String)])
                vl.updateFields()

                f = QgsFeature()
                f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(x, y)))
                f.setAttributes([address, title])
                pr.addFeature(f)
                vl.updateExtents()



        #zoom quan fem click
        def setCenter(x, y, zoom):
            #center
            center_point_in = QgsPointXY(x, y)
            # convert coordinates
            crsSrc = QgsCoordinateReferenceSystem(4326)  # WGS84
            crsDest = QgsCoordinateReferenceSystem(QgsProject.instance().crs())
            xform = QgsCoordinateTransform(crsSrc, crsDest, QgsProject.instance())
            # forward transformation: src -> dest
            center_point = xform.transform(center_point_in)
            iface.mapCanvas().setCenter(center_point)

            # zoom
            if zoom is not None:
                # transform the zoom level to scale
                scale_value = 591657550.5 / 2 ** (zoom - -10)
                iface.mapCanvas().zoomScale(scale_value)



        def onItemClicked(it, col): #quan fem click
            data = it.data(2, QtCore.Qt.EditRole)

            geojson = data.get('geojson')
            coord = geojson.get('geometry').get('coordinates')

            x = coord[0]
            y = coord[1]

            zoom = None
            setCenter(x, y, zoom)



        def create_tree():
            #construir l'arbre
            treeWidget = self.servers
            treeWidget.setColumnCount(1)

            treeWidget.clear()
            treeWidget.insertTopLevelItems(0, items)
            treeWidget.itemClicked.connect(onItemClicked)



        #afegir el layer de json amb les coordenades
        def __loadLayerGeoJSON(self, list):

            create_items(list, results)
            create_layer(list, nom)
            create_tree()



        if type is 'TMS':
            print('done')
            __loadLayerTMS(url, title) #la url ha de ser la del children
        elif type is 'GeoJSON':
            __loadLayerGeoJSON(self, list)


        '''
        #########
        CATÀLEG
        #########

        '''

        #url del catàleg
        r = requests.get('https://mapes.salt.cat/apps/giscube-admin/geoportal/category/catalog/')
        data = r.json()

        all_nodes = {}
        tree = []



        def __loadLayerTMS(self, layer, url):
            #agafem la url
            urlWithParams = 'type=xyz&url=' + str(url)
            urlWithParams += '&zmax=22&zmin=0'

            print(urlWithParams)

            # create QGIS raster layer & add to map
            rlayer = QgsRasterLayer(urlWithParams, layer['title'], 'wms')
            print(rlayer.isValid())

            if rlayer.isValid():
                QgsProject.instance().addMapLayer(rlayer)

        '''
        # ***FALTA***
        '''

        def __loadLayerWMS(self, layer, url): #FALTA

            print('h')
            #agafem la url

            #wms_url = 'crs=EPSG:3857&type=xyz&zmin=0&zmax=19&url=' + str(url)

            # *** {a|b|c} + str(url) ***

            wms_url = "type=xyz&url=" + str(url)
            """
            wms_url = 'url=' + str(url)
            wms_url += 'jpeg&crs=EPSG:4326'

            """


            '''
            urlWithParams_wms = 'type=xyz&url=' + str(url)
            urlWithParams_wms += '&zmax=22&zmin=0'

            '''

            #'@EPSG:900913@jpg/{z}/{x}/{y}.jpg'

            # create QGIS raster layer & add to map
            rlayer = QgsRasterLayer(wms_url, layer['title'], 'wms')
            print(rlayer.isValid())

            if rlayer.isValid():
                QgsProject.instance().addMapLayer(rlayer)



        def __loadLayerGeoJSON(self, layer, url):
            print('...')
            #url
            json_url = str(url) + "?access_token="
            print('url:', json_url)

            # create layer
            vlayer = QgsVectorLayer(json_url, layer['title'],"ogr")
            print(vlayer.isValid())

            # define projection
            crs = vlayer.crs()
            crs.createFromId(long(layer["children"][0]["projection"]))
            vlayer.setCrs(crs)

            # load to QGIS
            if vlayer.isValid():
                print('valid')
                QgsProject.instance().addMapLayer(vlayer)



        def add_layer_type(type, data, url): #afegir la capa en funció del tipus
            if type == 'WMS':
                print('----')
                __loadLayerWMS(self, data, url)

            elif type == 'TMS':
                __loadLayerTMS(self, data, url)

            elif type == 'GeoJSON':
                __loadLayerGeoJSON(self, data, url)




        def layer_type(dict_children, data, url): #obtenim el type de les dades
            type = dict_children['type']
            print('tipus:', type)

            add_layer_type(type, data, url)  #afegir la capa en funció del tipus




        def add_wms_layer(data): #afegir el layer
            #obtenim la url necessaria
            child = data['children']
            dict_children = child[0]
            url = dict_children['url']

            layer_type(dict_children, data, url) #cridem funció que dirà el type i farà una cosa o una altra




        def onItemClicked(it, col): #quan fem click
            data = it.data(2, QtCore.Qt.EditRole) #accedim a les dades de 'it'

            add_wms_layer(data) #afegir el layer



        def processar_children(content_row):
            if content_row.get('children') is not None:
                parent_widget = content_row.get('widget')
                content_row['widget'] = QTreeWidgetItem(parent_widget, [content_row.get('description')])



        def processar_content(row):
            if row.get('content') is not None:
                content = row.get('content')

                for content_row in content:
                    #print("***", content_row)
                    parent_widget = row.get('widget')

                    #print("parent widget:", parent_widget)
                    #print("titol:", content_row.get('title'))
                    content_row['widget'] = QTreeWidgetItem(parent_widget, [content_row.get('title')])

                    #layerNode = QTreeWidgetItem(currentNode, ['Name'])
                    #layerNode.setData(0, QtCore.Qt.EditRole, layer['title']) # 0 Text
                    #layerNode.setData(1, QtCore.Qt.EditRole, id) # 1 id
                    content_row['widget'].setData(2, QtCore.Qt.EditRole, content_row) # 2 data

                    #prova
                    data = content_row['widget'].data(2, QtCore.Qt.EditRole)

                    """
                    children = data['children']
                    dict_children = children[0]
                    print(dict_children['url'])

                    """

                    processar_children(content_row)


        #arbre
        for row in data:
           row['children'] = []
           all_nodes[row.get('id')] = row


           if row.get('parent') is None:
               row ['widget'] = (QTreeWidgetItem(None, [row.get('name')]))
               processar_content(row)
               tree.append(row)

           else:
               #print("...", row.get('name'))
               parent = all_nodes[row.get('parent')]

               parent_widget = parent.get('widget')
               row['widget'] = (QTreeWidgetItem(parent_widget, [row.get('name')]))

               processar_content(row)
               parent.get('children').append(row)

        """
        treeWidget = self.servers
        treeWidget.setColumnCount(1)
        items = []
        for row in tree:
            #recuperar widget creat
            items.append(row['widget'])

        treeWidget.clear()
        treeWidget.insertTopLevelItems(0, items)

        treeWidget.itemClicked.connect(onItemClicked)

        """






    def new_server_popup_original(self):
        """
        Opens a new server dialog.
        """
        dialog = NewServerDialog(self.dockwidget)
        if dialog.exec_():
            result = dialog.values()
            if result['name'] in ServerItem.saved_servers.childGroups():
                self.iface.messageBar().pushMessage(
                    "A server must have a unique name.",
                    Qgis.Critical
                )
                return
            new_conn = Giscube(
                result['url'],
                self.CLIENT_ID,
                False,
                result['name'],
            )
            si = ServerItem(
                new_conn,
                self.dockwidget.servers,
                self,
            )

            # try logging in
            user = result['username']
            pw = result['password']
            if (
                (user is not None and user != '')
                or
                (pw is not None and pw != '')
            ):
                r = si._try_login(user, pw, result['save_tokens'])
                if not r['finished']:
                    si._login_popup(True)

    def new_project_popup(self, default_server=None):
        dialog = NewProjectDialog(self, default_server)
        if dialog.exec_():
            project = QgsProject.instance()

            if project.write():
                path = project.fileInfo().absoluteFilePath()
            else:
                t = '{:.0f}'.format(time.time())
                path = QDir.tempPath() + ('/qgis-admin-project-'+t+'.qgs')
                if not project.write(path):
                    self.iface.messageBar().pushMessage(
                        "Error",
                        "No s'ha pogut guardar el projecte",
                        QgsMessageBar.ERROR
                    )

            server_name = dialog.servers.currentText()
            server_names = self.server_names()
            server_index = server_names.index(server_name)
            # TODO Add ValueError check and handeling (only can happen in
            #        multithreded enviroments)

            server = self.servers.topLevelItem(server_index)

            project_name = dialog.name.text()
            project_id = server.giscube.qgis_server.upload_project(
                None,
                project_name,
                path)

            project = ProjectItem(project_id, project_name, server)
            project.open()
