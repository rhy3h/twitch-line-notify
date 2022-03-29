import configparser
import requests
from time import sleep
from twich_live import isChannelLive

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    client_id = config['TWITCH']['client_id']
    client_secret = config['TWITCH']['client_secret']
    streamer_name = config['TWITCH']['streamer_name']
    line_api = config['LINE']['API']

    headers = {
        "Authorization": "Bearer " + line_api,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    live_status = False
    
    while True:
        channelStatus = isChannelLive(client_id, client_secret, streamer_name)
        if live_status == False:
            if len(channelStatus) == 1:
                live_status = True
                message = channelStatus[0]['user_name'] + '開台囉\n' + channelStatus[0]['title'] + '\nhttps://twitch.tv/' + channelStatus[0]['user_login']
                params = {
                    "message": message
                }
                r = requests.post(
                    "https://notify-api.line.me/api/notify",
                    headers = headers,
                    params = params
                )
                print(channelStatus[0]['user_name'] + "開台囉")
            else:
                print("離線中")
        if live_status == True:
            if len(channelStatus) == 1:
                print(channelStatus[0]['user_name'] + "持續開台中")
            else:
                print("離線中")
        sleep(5)