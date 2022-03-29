import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

client_id = config['TWITCH']['client_id']
client_secret = config['TWITCH']['client_secret']
streamer_name = config['TWITCH']['streamer_name']

body = {
    'client_id': client_id,
    'client_secret': client_secret,
    "grant_type": 'client_credentials'
}
r = requests.post('https://id.twitch.tv/oauth2/token', body)

keys = r.json()

headers = {
    'Client-ID': client_id,
    'Authorization': 'Bearer ' + keys['access_token']
}

stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name, headers=headers)

stream_data = stream.json()

if len(stream_data['data']) == 1:
    print(streamer_name + ' is live: ' + stream_data['data'][0]['title'] + ' playing ' + stream_data['data'][0]['game_name'])
else:
    print(streamer_name + ' is not live')