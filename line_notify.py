import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
line_api = config['LINE']['API']

headers = {
    "Authorization": "Bearer " + line_api,
    "Content-Type": "application/x-www-form-urlencoded"
}

params = {"message": "這是個通知測試"}

r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=params)