import requests


def lyric(_id):
    get = requests.get(f"http://0.0.0.0:27232/api/lyric?id={_id}").json()
    get_lyric = get['lrc']['lyric']
    return get_lyric


def play():
    get = requests.get("http://0.0.0.0:27232/player").json()
    get_id = get['currentTrack']['id']
    get_time = get['progress']
    get_name = get['currentTrack']['name']
    get_singer = get['currentTrack']['ar'][0]['name']
    return [get_id, get_time, get_name, get_singer]
