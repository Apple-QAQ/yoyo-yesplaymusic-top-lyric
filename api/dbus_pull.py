import dbus


def sendLyrics(text):
    bus = dbus.SessionBus()
    lyrics = bus.get_object('com.yoyo.Statusbar', '/Statusbar/Lyrics')
    iface = dbus.Interface(lyrics, dbus_interface='com.yoyo.Statusbar')
    m = iface.get_dbus_method("sendLyrics", dbus_interface=None)
    m(text)
