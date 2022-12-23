#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import json
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, GLib, Gst

#
# DBUS interface
#
class GenericMonitor:
    """
    Class that manage DBUS communication with GNOME generic monitor addon.
    You have to subclass it
    """
    
    def setupMonitor(self):
        """ Setup DBUS stuff (equivalent to constructor) """ 
        self._activated = True
        self._encoder = json.JSONEncoder()
        self._dbus_interface = 'com.soutade.GenericMonitor'

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self._dbus = dbus.SessionBus()

        self.systray_proxy = self._dbus.get_object('org.gnome.Shell', '/com/soutade/GenericMonitor')

        self.add_signal_receiver(self.onClick,         'onClick')
        self.add_signal_receiver(self.onDblClick,      'onDblClick')
        self.add_signal_receiver(self.onRightClick,    'onRightClick')
        self.add_signal_receiver(self.onRightDblClick, 'onRightDblClick')
        self.add_signal_receiver(self.onScrollUp,      'onScrollUp')
        self.add_signal_receiver(self.onScrollDown,    'onScrollDown')
        self.add_signal_receiver(self.onEnter,         'onEnter')
        self.add_signal_receiver(self.onLeave,         'onLeave')

        self.add_signal_receiver(self.onActivate,      'onActivate')
        self.add_signal_receiver(self.onDeactivate,    'onDeactivate')

    def runMainLoop(self):
        """ Start infinite loop that allows to send and receive events and functions """ 
        self._mainLoop = GLib.MainLoop()
        self._mainLoop.run()

    def stopMainLoop(self):
        """ Stop infinite main loop """
        self._mainLoop.quit()

    # Generic Monitor functions
    def notify(self, group):
        """ Send notify() function 
        Parameters
        ----------
        group : GenericMonitorGroup
            group to notify
        """
        if self._activated:
            if type(group) == GenericMonitorGroup:
                group = group.getValues()
            self.systray_proxy.notify(self._encoder.encode(group), dbus_interface=self._dbus_interface)

    def deleteItems(self, items):
        """ Send deleteItems() function 
        Parameters
        ----------
        items : list of str (<itemName>@<groupName>)
            items to delete
        """
        if self._activated:
            items = {'items':items}
            self.systray_proxy.deleteItems(self._encoder.encode(items), dbus_interface=self._dbus_interface)

    def deleteGroups(self, groups):
        """ Send deleteGroups() function 
        Parameters
        ----------
        groups : list of str (<groupName>)
            groups to delete
        """
        if self._activated:
            groups = {'groups':groups}
            self.systray_proxy.deleteGroups(self._encoder.encode(groups), dbus_interface=self._dbus_interface)

    def openPopup(self, item):
        """ Send openPopup() function 
        Parameters
        ----------
        item : str (<itemName>@<groupName>)
            Open popup (if there is one) of item
        """
        if self._activated:
            item = {'item':item}
            self.systray_proxy.openPopup(self._encoder.encode(item), dbus_interface=self._dbus_interface)

    def closePopup(self, item):
        """ Send closePopup() function 
        Parameters
        ----------
        item : str (<itemName>@<groupName>)
            Close popup (if there is one) of item
        """
        if self._activated:
            item = {'item':item}
            self.systray_proxy.closePopup(self._encoder.encode(item), dbus_interface=self._dbus_interface)

    def togglePopup(self, item):
        """ Send togglePopup() function 
        Parameters
        ----------
        item : str (<itemName>@<groupName>)
            Toggle popup (if there is one) of item
        """
        if self._activated:
            item = {'item':item}
            self.systray_proxy.togglePopup(self._encoder.encode(item), dbus_interface=self._dbus_interface)

    # Generic Monitor signals
    def onClick(self, sender):
        """ onClick event 
        Parameters
        ----------
        sender : str (<itemName>@<groupName>)
            Sender which event has been raised
        """
        pass

    def onRightClick(self, sender):
        """ onRightClick event 
        Parameters
        ----------
        sender : str (<itemName>@<groupName>)
            Sender which event has been raised
        """
        pass
    
    def onDblClick(self, sender):
        """ onDblClick event 
        Parameters
        ----------
        sender : str (<itemName>@<groupName>)
            Sender which event has been raised
        """
        pass

    def onRightDblClick(self, sender):
        """ onRightDblClick event 
        Parameters
        ----------
        sender : str (<itemName>@<groupName>)
            Sender which event has been raised
        """
        pass

    def onEnter(self, sender):
        """ onEnter event (mouse enter in item)
        Parameters
        ----------
        sender : str (<itemName>@<groupName>)
            Sender which event has been raised
        """
        pass

    def onLeave(self, sender):
        """ onLeave event (mouse leave item)
        Parameters
        ----------
        sender : str (<itemName>@<groupName>)
            Sender which event has been raised
        """
        pass

    def onScrollUp(self, sender):
        """ onScrollUp event 
        Parameters
        ----------
        sender : str (<itemName>@<groupName>)
            Sender which event has been raised
        """
        pass
    
    def onScrollDown(self, sender):
        """ onScrollDown event 
        Parameters
        ----------
        sender : str (<itemName>@<groupName>)
            Sender which event has been raised
        """
        pass

    def onActivate(self):
        """ onActivate event (addon activated)
        """
        self._activated = True

    def onDeactivate(self):
        """ onDeactivate event (addon deactivated)
        """
        self._activated = False

    # DBUS method
        """ Add callback when DBUS signal is raised
        Parameters
        ----------
        callback : function
            Callback raised on DBUS signal
        signalName : str
            Name of DBUS signal
        interface : str
            Name of DBUS interface
        """
    def add_signal_receiver(self, callback, signalName, interface=None):
        if not interface:
            interface = self._dbus_interface
        self._dbus.add_signal_receiver(callback, signalName, interface)


#
# Item stuff
#
class GenericMonitorGenericWidget:
    """ Generic widget class, parent of all widgets
    """
    def __init__(self, style='', name='', signals={}):
        """
        Parameters
        ----------
        name : str, optional
            Widget name
        signals : dictionary, optional
            Dictionary of signals and their action
        """
        self.valuesToMap = ['name', 'style']
        self.mapValues = {}
        self.mapName = ''
        self.style = style
        self.name = name
        self.signals = signals
        
    def setStyle(self, style):
        self.style = style

    def _toMap(self):
        """ Return dictionary of class elements to send to addon
        """
        self.mapValues = {}
        for p in self.valuesToMap:
            if self.__dict__[p]:
                self.mapValues[p] = self.__dict__[p]
        for (name, value) in self.signals.items():
            self.mapValues[name] = value
        return {self.mapName:self.mapValues}

class GenericMonitorTextWidget(GenericMonitorGenericWidget):
    """ Text widget
    """
    def __init__(self, text, style='', name='', signals={}):
        """
        Parameters
        ----------
        text : str
            Text to display
        style : str, optional
            CSS style
        name : str, optional
            Widget name
        signals : dictionary, optional
            Dictionary of signals and their action
        """
        super().__init__(style, name, signals)
        self.valuesToMap += ['text']
        self.mapName = 'text'

        self.text = text

    def setText(self, text):
        self.text = text
    
class GenericMonitorIconWidget(GenericMonitorGenericWidget):
    """ Icon widget
    """
    def __init__(self, path, style=''):
        """
        Parameters
        ----------
        path : str
            Icon path
        style : str, optional
            CSS style
        """
        super().__init__(style=style)
        self.valuesToMap += ['path']
        self.mapName = 'icon'

        self.path = path
        self.style = style

    def setPath(self, path):
        self.path = path


class GenericMonitorPictureWidget(GenericMonitorGenericWidget):
    """ Picture widget
    """
    def __init__(self, path, style='', width=-1, height=-1, name='', signals={}):
        """
        Parameters
        ----------
        path : str
            Picture path
        style : str, optional
            CSS style
        width : int, optional
            Width of displayed picture (-1 for default width)
        height : int, optional
            Width of displayed picture (-1 for default width)
        name : str, optional
            Widget name
        signals : dictionary, optional
            Dictionary of signals and their action
        """

        super().__init__(style, name, signals)
        self.valuesToMap += ['path', 'width', 'height']
        self.mapName = 'picture'
        self.path = path

        self.width = width
        self.height = height
        
    def setPath(self, path):
        self.path = path

    def setWidth(self, width):
        self.width = width
        
    def setHeight(self, height):
        self.height = height

class GenericMonitorPopup(GenericMonitorGenericWidget):
    """ Popup of current item
    """
    def __init__(self, items):
        """
        Parameters
        ----------
        items : list of GenericMonitorTextWidget and GenericMonitorPictureWidget
            List of items (text or picture)
        """
        self.valuesToMap = ('items',)
        self.mapName = 'popup'

        self.items = items

    def _toMap(self):
        self.mapValues = {}
        self.mapValues['items'] = []
        for item in self.items:
            self.mapValues['items'] += [item._toMap()]
        return {self.mapName:self.mapValues}

    def clear(self):
        """ Clear items list
        """
        self.items = []

    def setItems(self, items):
        self.items = items

class GenericMonitorItem:
    """ Addon item that will be displayed in status bar
    """
    def __init__(self, name, items=[], signals={}, popup=None, box='center'):
        """
        Parameters
        ----------
        name : str
            Item name
        items : list of GenericMonitorTextWidget and GenericMonitorIconWidget, optional
            List of items (text or icon)
        signals : dictionary, optional
            Dictionary of signals and their action
            "on-click"          : ["signal"|"delete"|"open-popup"|"close-popup"|"toggle-popup"]
            "on-dblclick"       : ["signal"|"delete"|"open-popup"|"close-popup"|"toggle-popup"]
            "on-rightclick"     : ["signal"|"delete"|"open-popup"|"close-popup"|"toggle-popup"]
            "on-rightdblclick"  : ["signal"|"delete"|"open-popup"|"close-popup"|"toggle-popup"]
            "on-click"          : ["signal"|"delete"|"open-popup"|"close-popup"|"toggle-popup"]
            "on-enter"          : ["signal"|"delete"|"open-popup"|"close-popup"|"toggle-popup"]
            "on-leave"          : ["signal"|"delete"|"open-popup"|"close-popup"|"toggle-popup"]
            "on-scroll"         : ["signal"|"delete"|"open-popup"|"close-popup"|"toggle-popup"]
        popup : GenericMonitorPopup, optional
            Popup to be displayed
        box : str, optional
            Box were to put items : left, center (default), or right
        """
        self.name = name
        self.items = items
        self.signals = signals
        self.popup = popup
        self.box = box
        self.group = ''
        
        self._checkValues()

    def _checkValues(self):
        if not self.name:
            raise ValueError('Need a name')
        if len(self.items) > 2:
            raise ValueError('Maximum 2 items can be displayed')
        for (name, value) in self.signals.items():
            if not name in ('on-click', 'on-dblclick', 'on-rightclick', 'on-rightdblclick',
                            'on-enter', 'on-leave', 'on-scroll'): 
                raise ValueError('Invalid signal name ' + name)
            if not value in ('signal', 'delete', 'open-popup', 'close-popup', 'toggle-popup'):
                raise ValueError('Invalid signal value ' + value)
        for item in self.items:
            if not isinstance(item, GenericMonitorGenericWidget):
                raise ValueError('Invalid item ' + item)
        if self.popup and not isinstance(self.popup, GenericMonitorPopup):
            raise ValueError('Invalid popup object')
        if self.box and not self.box in ('left', 'center', 'right'):
            raise ValueError('Invalid box value')

    def setGroup(self, group):
        """ Set current group (automatically done when added in a group)
        Parameters
        ----------
        group : str
            Group name
        """
        self.group = group

    def getName(self):
        return self.name

    def getFullName(self):
        """ return full name used by addon
        """
        return '%s@%s' % (self.name, self.group)
    
    def _toMap(self):
        myMap = {}
        for p in ('name', 'box'):
            if self.__dict__[p]:
                myMap[p] = self.__dict__[p]
        for item in self.items:
            item._toMap()
            myMap[item.mapName] = item.mapValues
        if self.popup:
            self.popup._toMap()
            myMap['popup'] = self.popup.mapValues
        for (name, value) in self.signals.items():
            myMap[name] = value
        return [myMap]

class GenericMonitorGroup:
    """ Group of items
    """
    def __init__(self, name, items=[]):
        """
        Parameters
        ----------
        name : str
            Group name
        items : list of GenericMonitorItem, optional
            List of items
        """
        self.name = name
        self.items = []
        if type(items) != list:
            self.addItem(items)
        else:
            self.addItems(items)

    def addItem(self, item):
        """ Add item into the groupw
        Parameters
        ----------
        item : GenericMonitorItem
            Item to add
        """
        item.setGroup(self.name)
        self.items.append(item)

    def addItems(self, items):
        """ Add items into the group
        Parameters
        ----------
        items : list of GenericMonitorItem
            Items to add
        """
        for item in items:
            self.addItem(item)

    def clear(self):
        """ Clear items list
        """
        for item in items:
            item.setGroup('')
        self.items = []
        
    def getValues(self):
        """ Returns group and its items in addon format
        """
        res = {'group': self.name, 'items':[]}
        for item in self.items:
            res['items'] += item._toMap()
        return res

    def __str__(self):
        return str(self.getValues())
