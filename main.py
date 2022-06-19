from api import yesplaymusic  #, dbus_pull
import os
import time

lyric = {}
old_music_name = ""
music_name = ""

try:
    with open(os.path.dirname(os.path.abspath(__file__)) + "/yesplaymusic-toplyric.txt") as config:
        sleep_time = config.read()
except FileNotFoundError:
    with open(os.path.dirname(os.path.abspath(__file__)) + "/yesplaymusic-toplyric.txt", "w") as config:
        config.write("0.1")
    with open(os.path.dirname(os.path.abspath(__file__)) + "/yesplaymusic-toplyric.txt") as config:
        sleep_time = config.read()

def get_lyric():
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
            tmp_list = [[0, 0], f"{_play[2]}-{_play[3]} | 无滚动歌词"]
            music_time = tmp_list[0]  # 解决无滚动歌词
        lyric.update({str(music_time): tmp_list[1]})


while True:
    music_name = yesplaymusic.play()[2]
    if old_music_name != music_name:  # 切歌
        old_music_name = music_name
        lyric = {}
        get_lyric()
    tmp_now_time = yesplaymusic.play()[1]
    m = int(tmp_now_time // 60)
    s = int(tmp_now_time - m * 60)
    now_time = [m, s]
    try:
        # dbus_pull.sendLyrics(lyric[f"{now_time}"])
        print(lyric[f"{now_time}"])  # test plugin
    except KeyError:
        ...  # 等同于pass
    time.sleep(float(sleep_time))
