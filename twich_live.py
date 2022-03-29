import requests
import configparser

def isChannelLive(client_id, client_secret, streamer_name):
    body = {
        'client_id': client_id,
        'client_secret': client_secret,
        "grant_type": 'client_credentials'
    }
    r = requests.post(
        'https://id.twitch.tv/oauth2/token',
        body
    )

    keys = r.json()

    headers = {
        'Client-ID': client_id,
        'Authorization': 'Bearer ' + keys['access_token']
    }

    stream = requests.get(
        'https://api.twitch.tv/helix/streams?user_login=' + streamer_name,
        headers = headers
    )

    stream_data = stream.json()

    return stream_data['data']