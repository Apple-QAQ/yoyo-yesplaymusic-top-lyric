import dbus


def send_lyrics(text):
    bus = dbus.SessionBus()
    lyrics = bus.get_object('com.yoyo.Statusbar', '/Statusbar/Lyrics')
    iface = dbus.Interface(lyrics, dbus_interface='com.yoyo.Statusbar')
    m = iface.get_dbus_method("send_lyrics", dbus_interface=None)
    m(text)
