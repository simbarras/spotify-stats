import time
import json
import requests
from requests.structures import CaseInsensitiveDict
import sys

SAMPLE = 10000000
URL = 'https://api.spotify.com'
ENDPOINT = '/v1/me/'
GET_DEVICES = URL+ENDPOINT+"player/devices"
SET_ROUND = URL+ENDPOINT+"player/repeat?state=context&device_id="
SET_SHUFFLE_ON = URL+ENDPOINT+"player/shuffle?state=true&device_id="
SET_SHUFFLE_OFF = URL+ENDPOINT+"player/shuffle?state=false&device_id="
NEXT = URL+ENDPOINT+"player/next"
GET_SONG = URL+ENDPOINT+"player/currently-playing"

GET = 'GET'
POST = 'POST'
PUT = 'PUT'

device_id = ''
secret_key = ''
header: CaseInsensitiveDict

song = {
    "track": [],
    "popularity": [],
    "read": []
}


def request(path, method='GET'):
    if method == 'GET':
        resp = requests.get(path, headers=header)
    elif method == 'POST':
        resp = requests.post(path, headers=header)
    elif method == 'PUT':
        resp = requests.put(path, headers=header)

    if resp.status_code // 100 != 2:
        print(path)
        print(resp.status_code)
        print(resp.headers)
        print(resp.text)
        exit(1)
    return resp


def add_entry(track, popularity):
    try:
        index = song["track"].index(track)
    except ValueError:
        index = len(song["track"])
        song["track"].append(track)
        song["popularity"].append(popularity)
        song["read"].append(0)
    finally:
        song["read"][index] += 1
        song["popularity"][index] = popularity


def initialize(reload):
    global device_id, secret_key, header, song

    # reload previous data
    if reload:
        with open('result.json', 'r', encoding="utf-8") as json_file:
            song = json.load(json_file)

    # open token file
    # search secret key in a file
    with open('token.key', 'r') as f:
        secret_key = f.read()

    # create header
    header = CaseInsensitiveDict()
    header['Authorization'] = "Bearer " + secret_key
    header['Content-Type'] = 'application/json'
    header['Content-Type'] = 'application/json'

    # Get device, send resquest to spotify
    devices = request(GET_DEVICES).json()
    # parse json
    for device in devices['devices']:
        if device['is_active']:
            device_id = device['id']
    print(device_id)

    # active round play
    request(SET_ROUND+device_id, PUT)


def run():
    for i in range(SAMPLE):
        # off shuffle play
        request(SET_SHUFFLE_OFF+device_id, PUT)
        time.sleep(0.1)

        # on shuffle play
        request(SET_SHUFFLE_ON+device_id, PUT)
        time.sleep(0.1)

        # next song
        request(NEXT, POST)

        time.sleep(1)

        # get current song
        current_song = request(GET_SONG).json()

        # wait if song has not changed
        while 1000 > current_song['progress_ms'] or current_song['progress_ms'] > 2000:
            time.sleep(0.1)
            current_song = request(GET_SONG).json()
            print(current_song['progress_ms'])
            if current_song['progress_ms'] > 5000:
                print("Song has changed")
                break

        # get track info
        track = current_song['item']['artists'][0]['name'] + " - " + current_song['item']['name']
        popularity = int(current_song['item']['popularity'])

        # add entry
        add_entry(track, popularity)
        print(str(i) + ": " + track + " -> " + str(popularity))

        time.sleep(0.1)
        if i % 50 == 0:
            print("Saving result")
            publish_result()
            time.sleep(50)


def publish_result():
    print(song)
    with open('result.json', 'w', encoding="utf-8") as f:
        # f.write(u'\ufeff')
        json.dump(song, f)

    csv_lines = ["Track;Popularity;Read"]
    for i in range(len(song['track'])):
        csv_lines.append(song['track'][i]+";"+str(song['popularity'][i])+";"+str(song['read'][i]))

    with open('result.csv', 'w', encoding="utf-8") as csvfile:
        csvfile.write(u'\ufeff')
        for line in csv_lines:
            csvfile.write(line+"\n")


def main(reload=False):
    initialize(reload)
    try:
        run()
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    finally:
        publish_result()


if __name__ == "__main__":
    main(bool(sys.argv[1:]))
