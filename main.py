from PyQt5 import QtWidgets
from UI import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox
import configparser
import requests

class myUI:
    def __init__(self, Ui_MainWindow):
        self.app = QtWidgets.QApplication([])
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()
    
    def checkTwitch(self, client_id, client_secret):
        body = {
            'client_id': client_id,
            'client_secret': client_secret,
            "grant_type": 'client_credentials'
        }
        r = requests.post('https://id.twitch.tv/oauth2/token', body)

        keys = r.json()
        try:
            keys['access_token']
            return True
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("錯誤")
            if keys['message'] == "invalid client":
                msg.setText("Client 輸入有誤")
            if keys['message'] == "invalid client secret":
                msg.setText("Secret 輸入有誤")
            msg.exec_()
            return False
    
    def checkLine(self, api):
        headers = {
            "Authorization": "Bearer " + api,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        params = {
            "message": "這是個通知測試"
        }
        r = requests.post(
            "https://notify-api.line.me/api/notify",
            headers = headers,
            params = params
        )

        if r.status_code == 200:
            return True
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("錯誤")
            msg.setText("Line API 有誤")
            msg.exec_()
            return False
        
    def confirmClick(self):
        client_id = self.ui.idEdit.text()
        client_secret = self.ui.secretEdit.text()
        streamer_name = self.ui.streamerEdit.text()
        line_api = self.ui.lineEdit.text()

        if self.checkTwitch(client_id, client_secret):
            config = configparser.ConfigParser()
            config['TWITCH'] = {
                'client_id': client_id,
                'client_secret': client_secret,
                'streamer_name': streamer_name,
            }
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        
        if self.checkLine(line_api):
            config = configparser.ConfigParser()
            config['LINE'] = {
                'api': line_api,
            }
            with open('config.ini', 'a+') as configfile:
                config.write(configfile)

    def ui_init(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        if 'TWITCH' in config:
            client_id = config['TWITCH']['client_id']
            client_secret = config['TWITCH']['client_secret']
            streamer_name = config['TWITCH']['streamer_name']
            self.ui.idEdit.setText(client_id)
            self.ui.secretEdit.setText(client_secret)
            self.ui.streamerEdit.setText(streamer_name)
        
        if 'LINE' in config:
            line_api = config['LINE']['API']
            self.ui.lineEdit.setText(line_api)
        
        self.ui.confirmBtn.clicked.connect(self.confirmClick)

    def app_exec(self):
        self.app.exec_()

if __name__ == "__main__":
    ui = myUI(Ui_MainWindow)
    ui.ui_init()
    ui.app_exec()
    