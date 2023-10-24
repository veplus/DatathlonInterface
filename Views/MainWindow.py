# coding:utf-8
import os.path
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QStackedWidget, QHBoxLayout, QLabel

from Views.fluentLib import (NavigationInterface, NavigationItemPosition, MessageBox,
                             isDarkTheme, NavigationAvatarWidget)
from Views.fluentLib import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True, collapsible=True)
        self.stackWidget = QStackedWidget(self)

        # create sub interface
        self.searchInterface = Widget('Recherche Interface', self)
        self.sujetInterface = Widget('Sujet Interface', self)
        self.statInterface = Widget('Statistiques Interface', self)
        self.folderInterface = Widget('Historique Interface', self)
        self.settingInterface = Widget('Page des parametres', self)
        self.phoneInterface = Widget('Appels - Tous', self)
        self.phoneIndusInterface = Widget('Appels - Industrie', self)
        self.phoneConsoInterface = Widget('Appels - Consomateur', self)
        # self.albumInterface1_1 = Widget('Section1', self)

        # initialize layout
        self.init_layout()

        # add items to navigation interface
        self.init_navigation()

        self.init_window()

        # self.navigationInterface.panel.displayMode = NavigationDisplayMode.MINIMAL
        # self.navigationInterface.panel.toggle()

    def init_layout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def init_navigation(self):
        # enable acrylic effect
        # self.navigationInterface.setAcrylicEnabled(True)

        self.add_sub_interface(self.searchInterface, FIF.SEARCH, 'Recherche')
        self.add_sub_interface(self.sujetInterface, FIF.MARKET, 'Sujets')
        self.add_sub_interface(self.statInterface, FIF.LAYOUT, 'Statistiques')

        self.navigationInterface.addSeparator()

        self.add_sub_interface(self.phoneInterface, FIF.PHONE, 'Appels', NavigationItemPosition.SCROLL)
        self.add_sub_interface(self.phoneConsoInterface, FIF.PHONE, 'Consommateurs', parent=self.phoneInterface)
        # self.add_sub_interface(self.albumInterface1_1, FIF.PHONE, 'Live', parent=self.albumInterface1)
        # self.add_sub_interface(self.albumInterface1_1, FIF.PHONE, 'En attente', parent=self.albumInterface1)
        self.add_sub_interface(self.phoneIndusInterface, FIF.PHONE, 'Industrie', parent=self.phoneInterface)

        # add navigation items to scroll area
        self.add_sub_interface(self.folderInterface, FIF.FOLDER, 'Archives', NavigationItemPosition.SCROLL)

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('Fred', os.path.join(os.path.dirname(__file__), 'resource/shoko.png')),
            onClick=self.show_message_box,
            position=NavigationItemPosition.BOTTOM,
        )

        self.add_sub_interface(self.settingInterface, FIF.SETTING, 'Parametres', NavigationItemPosition.BOTTOM)

        self.stackWidget.currentChanged.connect(self.on_current_interface_changed)
        self.stackWidget.setCurrentIndex(1)

        # always expand
        # self.navigationInterface.setCollapsible(False)

    def init_window(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'resource/Logo-small.png')))
        self.setWindowTitle('AMF - Centre d\'Information')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.set_qss()

    def add_sub_interface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, parent=None):
        """ add sub interface """
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switch_to(interface),
            position=position,
            tooltip=text,
            parentRouteKey=parent.objectName() if parent else None
        )

    def set_qss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(os.path.join(os.path.dirname(__file__), f'resource/{color}/demo.qss'), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switch_to(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def on_current_interface_changed(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())

    def show_message_box(self):
        w = MessageBox(
            'Pret pour le show?',
            'AMF DATATHON Préparation',
            self
        )
        w.yesButton.setText('Oui')
        w.cancelButton.setText('Non')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://www.google.com"))
