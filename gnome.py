#!/usr/bin/python3

from api import yesplaymusic
import os
import time
from threading import Thread
from signal import signal, SIGINT
import sys
from genericmonitor import *

class TimerThread(Thread,GenericMonitor):
    lyric = {}
    old_music_name = ""
    music_name = ""
    def get_lyric(self):
        _play = yesplaymusic.play()
        music_lrc = yesplaymusic.lyric(_id=_play[0])
        music_lrc = music_lrc.strip()
        music_line = music_lrc.splitlines()

        for line in music_line:
            try:
                tmp_list = line.strip().split("]")
                tmp_time = tmp_list[0].replace("[", '').split(":")
                minute = tmp_time[0]
                time_sec = tmp_time[1].split(".")[0]
                music_time = [int(minute)] + [int(time_sec)]
            except:
                tmp_list = [0, f"{_play[2]}-{_play[3]} | 无滚动歌词"]
                music_time = [0, 0]  # 解决无滚动歌词
            self.lyric.update({str(music_time): tmp_list[1]})
    def _displayLyricValue(self):
            self.music_name = yesplaymusic.play()[2]
            if self.old_music_name != self.music_name:  # 切歌
                self.old_music_name = self.music_name
                self.lyric = {}
                self.get_lyric()
            tmp_now_time = int("%.0f" % (yesplaymusic.play()[1] - 0.1))  # 四舍五入
            m = int(tmp_now_time // 60)
            s = int(tmp_now_time - m * 60)
            now_time = [m, s]
            try:
                text =  self.lyric[f"{now_time}"]
                self.textWidget.setText(text)
                print(self.lyric[f"{now_time}"])
            except KeyError:
                ...
            style = 'color:white'

            self.textWidget.setStyle(style)
            
            self.notify(self.monitorGroup)

    def run(self):
        self.setupMonitor()
        try:
            with open(os.path.dirname(os.path.abspath(__file__)) + "/yesplaymusic-toplyric.txt") as config:
                sleep_time = config.read()
        except FileNotFoundError:
            with open(os.path.dirname(os.path.abspath(__file__)) + "/yesplaymusic-toplyric.txt", "w") as config:
                config.write("0.09")
            with open(os.path.dirname(os.path.abspath(__file__)) + "/yesplaymusic-toplyric.txt") as config:
                sleep_time = config.read()
        self.timers = [0, 0]
        self._stopLoop = False
        
        self.textWidget = GenericMonitorTextWidget('')
        signals = {}
        self.monitorItem = GenericMonitorItem('lyric', [self.textWidget], signals, box='left')
        self.monitorGroup = GenericMonitorGroup('Lyric', self.monitorItem)
        while True:
            time.sleep(1)
            self._displayLyricValue()

    def _forMe(self, sender):
        return sender == self.monitorItem.getFullName()

    def onActivate(self):
        super().onActivate()
        self._displayLyricValue()
    
def signalHandler(signal_received, frame):
    timerThread.stop()
    timerThread.join()
    groups = ['Lyric']
    timerThread.deleteGroups(groups)
    sys.exit(0)

timerThread = TimerThread()
timerThread.start()

signal(SIGINT, signalHandler)

timerThread.runMainLoop()
