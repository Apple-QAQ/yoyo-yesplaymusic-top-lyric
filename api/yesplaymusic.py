import requests


def lyric(_id):
    get = requests.get(f"http://0.0.0.0:27232/api/lyric?id={_id}").json()
    get_lyric = get['lrc']['lyric']
    return get_lyric


def play():
    get = requests.get("http://0.0.0.0:27232/player").json()
    get_current_track = get['currentTrack']
    get_id = get_current_track['id']
    get_time = get['progress']
    get_name = get_current_track['name']
    get_singer = get_current_track['ar'][0]['name']
    return [get_id, get_time, get_name, get_singer]
