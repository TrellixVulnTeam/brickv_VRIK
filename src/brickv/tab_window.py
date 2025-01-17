# -*- coding: utf-8 -*-
"""
brickv (Brick Viewer)
Copyright (C) 2009-2012 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2014 Philipp Kroos <philipp.kroos@fh-bielefeld.de>

tab_window.py: Detachable container to be used in a TabBar (e.g. TabWidget)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QDialog, QAbstractButton, QTabBar, QVBoxLayout
from PyQt5.QtGui import QPainter, QIcon

from brickv import config
from brickv.load_pixmap import load_pixmap

class IconButton(QAbstractButton):
    clicked = pyqtSignal()

    def __init__(self, normal_icon, hover_icon, parent=None):
        super().__init__(parent)
        self.normal_icon = normal_icon
        self.hover_icon = hover_icon
        self.setIcon(normal_icon)
        self.setMouseTracking(True)
        self.setFixedSize(16, 16)

    def paintEvent(self, event):
        painter = QPainter(self)

        self.icon().paint(painter, event.rect())

    def sizeHint(self):
        return self.iconSize()

    def enterEvent(self, _event):
        self.set_hover_icon()

    def leaveEvent(self, _event):
        self.set_normal_icon()

    def mousePressEvent(self, _event):
        self.clicked.emit()

    def set_hover_icon(self):
        self.setIcon(self.hover_icon)

    def set_normal_icon(self):
        self.setIcon(self.normal_icon)

class ToplevelWindow(QWidget):
    def __init__(self, tab_window, name):
        super().__init__(None)
        super().setWindowTitle(name)
        self.tab_window = tab_window

    # overrides QWidget.closeEvent
    def closeEvent(self, event):
        self.tab_window.tab()
        event.accept()

class TabWindow(QWidget):
    """Detachable widget usable in a QTabWidget. The widget can be detached
    from the QTabWidget by calling untab(), added to it by calling tab().
    If tabbed, it has a clickable icon visualizing mouseOver events.
    Callbacks called after the tabbing and before the  untabbing events
    can be registered."""

    def __init__(self, tab_widget, name, parent=None):
        super().__init__(parent)

        self.tab_widget = tab_widget
        self.name = name
        self.untab_button = None # see tab()
        self.untab_button_icon_normal = QIcon(load_pixmap('untab-icon-normal.png'))
        self.untab_button_icon_hover = QIcon(load_pixmap('untab-icon-hover.png'))
        self.cb_pre_tab = {}
        self.cb_post_tab = {}
        self.cb_pre_untab = {}
        self.cb_post_untab = {}
        self.toplevel_window = None
        self.update_button = None
        self.tabbed = True

    def untab(self):
        index = self.tab_widget.indexOf(self)

        if index < 0:
            return

        for cb in self.cb_pre_untab.values():
            cb(self, index)

        self.tabbed = False

        # select setup tab before removal to avoid temporarily selecting tab at index - 1
        self.tab_widget.setCurrentIndex(0)

        # this stops the plugin as a side effect
        self.tab_widget.removeTab(index)

        self.toplevel_window = ToplevelWindow(self, self.name + " - " + "Brick Viewer " + config.BRICKV_VERSION)

        layout = QVBoxLayout(self.toplevel_window)
        layout.addWidget(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.toplevel_window.show()
        self.show()

        # start the plugin again after stopping it as a side effect of removing it from the QTabWidget
        self._info.plugin.start_plugin()

        for cb in self.cb_post_untab.values():
            cb(self)

    def tab(self):
        for cb in self.cb_pre_tab.values():
            cb(self)

        self._info.plugin.stop_plugin()

        index = self.tab_widget.addTab(self, self.name)

        self.tabbed = True

        # (re-)instantiating button here because the TabBar takes ownership and
        # destroys it when this TabWindow is untabbed
        self.untab_button = IconButton(self.untab_button_icon_normal, self.untab_button_icon_hover, parent=self)
        self.untab_button.setToolTip('Detach Tab from Brick Viewer')
        self.untab_button.clicked.connect(self.untab)

        self.tab_widget.tabBar().setTabButton(index, QTabBar.LeftSide, self.untab_button)

        for cb in self.cb_post_tab.values():
            cb(self, index)

    def add_callback_pre_tab(self, callback, key): # callback(tab_window)
        self.cb_pre_tab[key] = callback

    def add_callback_post_tab(self, callback, key): # callback(tab_window, tab_index)
        self.cb_post_tab[key] = callback

    def add_callback_pre_untab(self, callback, key): # callback(tab_window, tab_index)
        self.cb_pre_untab[key] = callback

    def add_callback_post_untab(self, callback, key): # callback(tab_window)
        self.cb_post_untab[key] = callback

    def show_update_tab_button(self, tool_tip, clicked_fn):
        if not self.tabbed:
            return

        self.update_button = IconButton(QIcon(load_pixmap('update-icon-normal.png')), QIcon(load_pixmap('update-icon-hover.png')))
        self.update_button.setToolTip(tool_tip)
        self.update_button.clicked.connect(clicked_fn)

        tab_idx = self.tab_widget.indexOf(self)

        self.tab_widget.tabBar().setTabButton(tab_idx, QTabBar.RightSide, self.update_button)

    def hide_update_tab_button(self):
        if not self.tabbed:
            return

        tab_idx = self.tab_widget.indexOf(self)
        tab_button = self.tab_widget.tabBar().tabButton(tab_idx, QTabBar.RightSide)

        if tab_button is None:
            return

        tab_button.hide()
        self.tab_widget.tabBar().setTabButton(tab_idx, QTabBar.RightSide, None)
