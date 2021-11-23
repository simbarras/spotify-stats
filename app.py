import time

SAMPLE = 1000

device_id = ''
secret_key = ''

song = {
    "track": [],
    "views": 0,
    "read": 0
}


def add_entry(track, views):
    if not song["track"].contains(track):
        song["track"].append(track)
        song["views"] = views

    song["read"] += 1


def initialize():
    global device_id, secret_key
    # Find playlist
    # Start listening
    # active round play

    # Get device, send resquest to spotify
    # parse json
    device_id = '... device found'

    # search secret key in a file
    secret_key = '... secret key found'


def run():
    for _ in range(SAMPLE):
        # off shuffle play
        # on shuffle play
        # next song
        # get current song
        track = '... track found'
        view = '... views of the track found'
        add_entry(track, view)

        time.sleep(1)

def publish_result():
    # publish result
    # do an excel file
    pass

def main():
    initialize()
    run()
    publish_result()

if __name__ == "__main__":
    main()
